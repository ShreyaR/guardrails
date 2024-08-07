# Deploying Guardrails

This document is a guide on our preffered method to deploy Guardrails to production.  We will discuss the new client/server model and the benefits this approach gains us.  We'll also look at some patterns we find useful when deploying to a production environment as well as some practices to keep in mind when developing with this new pattern.

:::note
Read the quick start guide on using Guardrails on the server [here](https://www.guardrailsai.com/docs/getting_started/guardrails_server)
:::

## The Client/Server Model

### Guardrails As A Service
As part of the v0.5.0 release, we introduced the `guardrails-api`.  The Guardrails API offers a way to offload the tasks of initializing and executing Guards to a dedicated server.  As of the time of writing this document, this is a simple Flask application that uses the core Guardrails validation engine to interact with Guards over HTTP(S) via a RESTful pattern.  There are two main ways you can specify Guards for use on the server:
1. By writing a simple python config file for most use cases
2. By adding a PostgreSQL database for advanced use cases

We will focus on the first use case in this document.

### A Quick Demonstration of Using the Guardrails API as a Dev Server
0. *Optional:* We generally recommend utilizing virtual environments.  If you don't already have a preference, you can use python's built [venv](https://docs.python.org/3/library/venv.html) module for this.
1. Install Guardrails with the `api` extra:
    ```sh
    pip install "guardrails-ai[api]"
    ```

2. Install any validators you need from the hub:
    ```sh
    guardrails hub install hub://guardrails/regex_match
    ```

3. Write your Guards in a config.py file:
    ```py
    # config.py
    from guardrails import Guard
    from guardrails.hub import RegexMatch

    name_case = Guard(
        # This line is important since the Guard's name property will act as the primary key for lookup.
        name="name-case",
        description="Checks that a string is in Title Case format."
    ).use(
        RegexMatch(regex="^(?:[A-Z][^\\s]*\\s?)+$")
    )
    ```

4. Start the Guardrails API
    ```sh
    guardrails start --config=./config.py
    ```

5. Reference your Guard by name to use it in your application code:
    ```py
    from guardrails import Guard, settings

    settings.use_server = True

    name_guard = Guard(name="name-case")

    validation_outcome = name_guard.validate("John Doe")
    ```

### Why a Client/Server Model?
Moving the computational load of validation off of the client application and onto a dedicated server has many benefits.  Beyond enabling potential future enhancements such as proxy implementations and supporting other programming languages with client SDKs, it also solves many of the problems we've encountered ourselves when considering how to best put Guardrails in production.

Previously, if you were using Guardrails in your application you were also including all of the validators that were part of the core library as well as the models of any of those validators you utilized.  This added a lot of overhead to the storage required to run Guardrails on a production server.  Beyond this, you also had to account for the resources required to run these models effieciently as part of your production server.  As an extreme example, when setting up a server to facilitate the Guardrails Hub playground which included every public validator available for use, the resulting image was over 6GB which is clearly not sustainable.

In version 0.5.0 as part of the client/server model, all validators were removed from the main repo in favor of selecting only the ones you need from the Guardrails Hub.  With this new approach that removes the baggage of maintaining validators within the core Guardrails package, a Docker image of a client application built on python:3.12-slim with a `venv` environment comes in at ~350MB uncompressed.  This will continue to decrease as we introduce optimized install profiles for various use cases.

One last notable improvement we're making to help reduce the impact validator models have on your deployables is introducting remote validation for select validators.  With this feature, you can utilize certain validators _without_ downloading or running their underlying models on your hardware.  Instead, after a one time configuration, they can offload the heavy lifting to dedicated, remotely hosted models without the need to change the way you interact with the Guardrails package.  You can read more about this [here](/concepts/remote_validation_inference).

So far, we've talked a lot about reducing the resources necessary to run Guardrails in production.  Another important factor we considered when shifting to the new client/server paradigm is how this pattern enables better scaling practices.  Since the Guardrails API is now separate and distinct from your application code, you can scale both separately and according to their own needs.  This means that if your client application needs to scale it can do so without accounting for the additional resources required for validation.  Likewise, if the validation traffic is the limiting factor, you client application can stay small on fewer instances while the Guardrails API scales out to meet the demand.  You're also not limited to only one Guardrails API deployable giving you the option to scale more heavily utilized use-cases independently of those less frequently used.


## Considerations for Productionization
As previously mentioned, the Guardrails API is currently a simple Flask application.  This means you'll want a WSGI server to serve the application for a production environment.  There are many options out there and we do not particularly endorse one of another.  For demonstration purposes we will show using Gunicorn since it is a common choice in the industry.

Previously we showed how to start the Guardrails API as a dev server using the `guardrails start` command.  When launching the Guardrails API with a WSGI server, you will reference the underlying `guardrails_api` module instead.  For example, when we Dockerize the Guardrails API for internal use, our final line is:
```Dockerfile
CMD gunicorn --bind 0.0.0.0:8000 --timeout=90 --workers=4 'guardrails_api.app:create_app(None, "config.py")'
```

This line starts the Guardrails API Flask application with a gunicorn WSGI server.  It specifies what port to bind the server to, as well as the timeout for workers and the maximum number of worker threads for handling requests.  We typically use the `gthread` worker class with gunicorn because of compatibility issues between how some async workers try to monkeypatch dependencies and how some libraries specify optional imports.

The [Official Gunicorn Documentation](https://docs.gunicorn.org/en/latest/design.html#how-many-workers) recommends setting the number of threads/workers to (2 x num_cores) + 1, though this may prove to be too resource intensive, depending on the choice of models in validators.  Specifying `--threads=` instead of `--workers=` will cause gunicorn to use multithreading instead of multiprocessing.  Threads will be lighter weight, as they can share the models loaded at startup from `config.py`, but [risk hitting race conditions](https://github.com/guardrails-ai/guardrails/discussions/899) when manipulating history.  For cases that have several larger models, need longer to process requests, have square-wave-like traffic, or have sustained high traffic, `--threads` may prove to be a desirable tradeoff.     

For further reference, you can find a bare-bones example of Dockerizing the Guardrails API here: https://github.com/guardrails-ai/guardrails-lite-server


When selecting a deployment environment it is important to consider what types of validators you plan to use.  If most of the validators you require are static or LLM based, the Guardrails API can perform well in a serverless environment.  However if you make use of multiple ML based validators, the sheer memory footprint the underlying models bring and the need to load the models on init are good reasons to choose a more persistent hosting option.  When utilizing a containerized hosting option that allows for auto-scaling, we find that under load the tasks are generally more CPU bound than memory bound and therefore benefit more from scaling on CPU utilization or request queue depth.

## Patterns and Practices for Using the Client/Server Model
When considering what to put where when splitting your Guardrails implementation between your client application and the Guardrails API, it mostly comes down to shifting the heavy lifting to the server and keeping your implementation on the client side to a minimum.

For example, you should define your Guards in the `config.py` that is loaded onto the server, not in your client application.  Additionally validators from the Guardrails HUB should also be installed on the server since that is where they will be executed; no need to install these in the client application.  This also means that _generally_ any extras you need alongside Guardrails would also be installed server side; that is, you would only want to install `guardails-ai` in your application whereas you would install `guardrails-ai[api]` on the server.  This keeps additional dependencies where they belong.


## Next Steps

Go ahead and deploy your dockerized Guardrails server on any cloud! We have guides on how to deploy Guardrails on specific clouds.

- [Deploying Guardrails on AWS](https://www.guardrailsai.com/docs/how_to_guides/deploying_aws)