import json
import logging
import os
from collections import defaultdict
from copy import deepcopy
from typing import Any, Dict, List, Union, Optional, Tuple
from lxml import etree as ET

import rich
import manifest

from guardrails.prompt_repo import Prompt
from guardrails.x_datatypes import DataType
from guardrails.x_datatypes import registry as types_registry
from guardrails.x_validators import ReAsk


logger = logging.getLogger(__name__)


class XSchema:
    def __init__(
        self,
        schema: Dict[str, DataType],
        base_prompt: Prompt,
        parsed_xml: ET.Element,
        num_reasks: int = 1,
    ):
        self.schema: Dict[str, DataType] = schema
        self.base_prompt = base_prompt
        self.parsed_xml = parsed_xml
        self.num_reasks = num_reasks

        self.openai_api_key = os.environ.get("OPENAI_API_KEY", None)
        self.client = manifest.Manifest(
            client_name="openai",
            client_connection=self.openai_api_key,
        )

    @classmethod
    def from_xml(cls, xml_file: str, base_prompt: Prompt) -> "XSchema":
        """Create an XSchema from an XML file."""

        with open(xml_file, "r") as f:
            xml = f.read()
        parser = ET.XMLParser(encoding="utf-8")
        parsed_xml = ET.fromstring(xml, parser=parser)

        schema = load_from_xml(parsed_xml, strict=False)

        base_prompt.append_to_prompt(cls.prompt_xml_prefix())
        base_prompt.append_to_prompt("\n{{response_prompt}}\n")
        base_prompt.append_to_prompt(cls.prompt_json_suffix())

        return cls(schema, base_prompt, parsed_xml)

    def llm_ask(self, prompt) -> str:
        return self.client.run(
            prompt,
            engine="text-davinci-003",
            temperature=0,
            max_tokens=2048,
        )

        # with open('response_as_dict.json', 'r') as f:
        #     text = f.read()

        # return text

    @staticmethod
    def prompt_json_suffix():
        return """\n\nReturn a valid JSON object that respects this XML format and extracts only the information requested in this document. Respect the types indicated in the XML -- the information you extract should be converted into the correct 'type'. Try to be as correct and concise as possible. Find all relevant information in the document. If you are unsure of the answer, enter 'None'. If you answer incorrectly, you will be asked again until you get it right which is expensive."""  # noqa: E501

    @staticmethod
    def prompt_xml_prefix():
        return """\n\nGiven below is XML that describes the information to extract from this document and the tags to extract it into.\n\n"""  # noqa: E501

    def ask_with_validation(self, text) -> str:
        """Ask a question, and validate the response."""

        parsed_xml_copy = deepcopy(self.parsed_xml)
        response_prompt = extract_prompt_from_xml(parsed_xml_copy)

        response, response_as_dict, validated_response = self.validation_inner_loop(
            text, response_prompt, 0
        )

        return response, response_as_dict, validated_response

    def validation_inner_loop(self, text: str, response_prompt: str, reask_ctr: int):
        prompt = self.base_prompt.format(document=text).format(
            response_prompt=response_prompt
        )

        response = self.llm_ask(prompt)

        try:
            response_as_dict = json.loads(response)
            validated_response, reasks = self.validate_response(response_as_dict)
        except json.decoder.JSONDecodeError:
            validated_response = None
            response_as_dict = None
            reasks = None

        rich.print(f"\n\n\nreasks: {reasks}")
        rich.print(f"\n\n\nreask_ctr: {reask_ctr}")

        if len(reasks) and reask_ctr < self.num_reasks:
            reask_prompt = self.get_reask_prompt(reasks)

            rich.print(f"\n\n\nreask_prompt: {reask_prompt}")

            return self.validation_inner_loop(text, reask_prompt, reask_ctr + 1)

        return response, response_as_dict, validated_response

    def gather_reasks(self, response: Dict) -> List[tuple]:
        """
        Traverse response and gather all ReAsk objects.
        Response is a nested dictionary, where values can also be lists or
        dictionaries.
        Make sure to also grab the corresponding paths (including list index),
        and return a list of tuples.
        """
        reasks = []

        def _gather_reasks(response: Union[list, dict], path: List[str] = []):
            if isinstance(response, dict):
                iterable = response.items()
            elif isinstance(response, list):
                iterable = enumerate(response)
            else:
                raise ValueError(f"Expected dict or list, got {type(response)}")
            for field, value in iterable:
                if isinstance(value, ReAsk):
                    reasks.append((path + [field], value))

                if isinstance(value, dict):
                    _gather_reasks(value, path + [field])

                if isinstance(value, list):
                    for idx, item in enumerate(value):
                        if isinstance(item, ReAsk):
                            reasks.append((path + [field, idx], item))
                        else:
                            _gather_reasks(item, path + [field, idx])

        _gather_reasks(response)
        return reasks

    def get_reasks_by_element(
        self,
        reasks: List[tuple],
        parsed_xml: ET._Element,
    ) -> Dict[ET._Element, List[tuple]]:

        reasks_by_element = defaultdict(list)

        for path, reask in reasks:
            # Make a find query for each path
            # - replace int values in path with '*'
            # TODO: does this work for all cases?
            query = "."
            for part in path:
                if isinstance(part, int):
                    query += "/*"
                else:
                    query += f"/*[@name='{part}']"

            # Find the element
            element = parsed_xml.find(query)

            reasks_by_element[element].append((path, reask))

        return reasks_by_element

    def get_pruned_tree(
        self,
        root: ET._Element,
        reask_elements: List[ET._Element] = None,
    ) -> str:
        """Prune tree of any elements that are not in `reasks`.

        Return the tree with only the elements that are keys of `reasks` and their
        parents. If `reasks` is None, return the entire tree. If an element is
        removed, remove all ancestors that have no children.

        Args:
            root: The XML tree.
            reasks: The elements that are to be reasked.

        Returns:
            The prompt.
        """
        if reask_elements is None:
            return root

        # Get all elements in `root`
        elements = root.findall(".//*")
        for element in elements:
            if (element not in reask_elements) and len(element) == 0:
                parent = element.getparent()
                parent.remove(element)

                # Remove all ancestors that have no children
                while len(parent) == 0:
                    grandparent = parent.getparent()
                    grandparent.remove(parent)
                    parent = grandparent

        return root

    def get_reask_prompt(self, reasks: List[tuple]) -> str:
        """Get the prompt for reasking.

        Args:
            reasks: The elements that are to be reasked.

        Returns:
            The prompt.
        """
        parsed_xml_copy = deepcopy(self.parsed_xml)
        reasks_by_element = self.get_reasks_by_element(
            reasks, parsed_xml=parsed_xml_copy
        )
        pruned_xml = self.get_pruned_tree(
            root=parsed_xml_copy, reask_elements=list(reasks_by_element.keys())
        )
        reask_prompt = extract_prompt_from_xml(pruned_xml, reasks_by_element)

        return reask_prompt

    def validate_response(
        self, response: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], List[tuple]]:
        """Validate a response against the schema.

        Args:
            response: The response to validate.

        Returns:
            Tuple, where the first element is the validated response, and the
            second element is a list of tuples, where each tuple contains the
            path to the reasked element, and the ReAsk object.
        """

        validated_response = deepcopy(response)

        for field, value in validated_response.items():
            if field not in self.schema:
                logger.debug(f"Field {field} not in schema.")
                continue

            validated_response = self.schema[field].validate(
                field, value, validated_response
            )

        reasks = self.gather_reasks(validated_response)

        return (validated_response, reasks)

    def __repr__(self):
        def _print_dict(d: Dict[str, Any], indent: int = 0) -> str:
            """Print a dictionary in a nice way."""

            s = ""
            for k, v in d.items():
                if isinstance(v, dict):
                    s += f"{k}:\n{_print_dict(v, indent=indent + 1)}"
                else:
                    s += f"{' ' * (indent * 4)}{k}: {v}\n"

            return s

        schema = _print_dict(self.schema)

        return f"XSchema({schema})"


def load_from_xml(tree: ET._Element, strict: bool = False) -> bool:
    """Validate parsed XML, create a prompt and a Schema object."""

    schema = {}

    for child in tree:
        if isinstance(child, ET._Comment):
            continue
        child_name = child.attrib["name"]
        child_data_type = child.tag
        child_data_type = types_registry[child_data_type]
        child_data = child_data_type.from_xml(child, strict=strict)
        schema[child_name] = child_data

    return schema


def get_correction_instruction(
    reasks: List[tuple]
) -> str:
    """Construct a correction instruction.

    Args:
        reasks: List of tuples, where each tuple contains the path to the
            reasked element, and the ReAsk object (which contains the error message describing why the
            reask is necessary).
        response: The response.

    Returns:
        The correction instruction.
    """

    correction_instruction = ""

    for reask in reasks:
        reask_path = reask[0]
        reask_element = reask[1]
        reask_error_message = reask_element.error_message
        reask_value = reask_element.incorrect_value

        # Create a helpful prompt that mentions why the reask value is incorrect.
        # The helpful prompt should have english language directions for the user.
        reask_prompt = f" '{reask_value}' is not a valid value for '{reask_path[-1]}' because {reask_error_message}"

        # Add the helpful prompt to the correction instruction.
        correction_instruction += f"{reask_prompt}"

    return correction_instruction


def extract_prompt_from_xml(
    tree: ET._Element,
    reasks: Optional[Dict[ET._Element, List[tuple]]] = None,
) -> str:
    """Extract the prompt from an XML tree.

    Args:
        tree: The XML tree.

    Returns:
        The prompt.
    """
    reasks = reasks or {}

    # From the element tree, remove any action attributes like 'on-fail-*'.
    # Filter any elements that are comments.
    for element in tree.iter():

        if isinstance(element, ET._Comment):
            continue

        for attr in list(element.attrib):
            if attr.startswith("on-fail-"):
                del element.attrib[attr]

        if element in reasks:

            correction_prompt = get_correction_instruction(
                reasks[element], 
            )
            element.attrib["previous_feedback"] = correction_prompt

    # Return the XML as a string.
    return ET.tostring(tree, encoding="unicode", method="xml")
