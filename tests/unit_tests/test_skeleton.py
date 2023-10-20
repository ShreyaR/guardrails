import lxml.etree as ET
import pytest

from guardrails.datatypes import Object
from guardrails.utils.json_utils import verify_schema_against_json


@pytest.mark.parametrize(
    "xml, generated_json, result",
    [
        (
            """
<root>
<list name="my_list">
    <object>
        <string name="my_string" />
    </object>
</list>
<integer name="my_integer" />
<string name="my_string" />
<object name="my_dict">
    <string name="my_string" />
</object>
<object name="my_dict2">
    <list name="my_list">
        <float />
    </list>
</object>
<list name="my_list2">
    <string />
</list>
</root>
            """,
            {
                "my_list": [{"my_string": "string"}],
                "my_integer": 1,
                "my_string": "string",
                "my_dict": {"my_string": "string"},
                "my_dict2": {
                    "my_list": [
                        1.0,
                        2.0,
                    ]
                },
                "my_list2": [],
            },
            True,
        ),
        (
            """
<root>
<list name="my_list">
    <object>
        <string name="my_string" />
    </object>
</list>
<integer name="my_integer" />
<string name="my_string" />
<object name="my_dict">
    <string name="my_string" />
</object>
<object name="my_dict2">
    <list name="my_list">
        <float />
    </list>
</object>
<list name="my_list2">
    <string />
</list>
</root>
            """,
            {
                "my_list": [{"my_string": "string"}],
                "my_integer": 1,
                "my_string": "string",
                "my_dict": {"my_string": "string"},
                "my_list2": [],
            },
            False,
        ),
        (
            """
<root>
<choice name="action" discriminator="action_type" on-fail-choice="exception">
    <case name="fight">
        <string
            name="fight_move"
            format="valid-choices: {['punch','kick','headbutt']}"
            on-fail-valid-choices="exception"
        />
    </case>
    <case name="flight">
        <string
            name="flight_direction"
            format="valid-choices: {['north','south','east','west']}"
            on-fail-valid-choices="exception"
        />
        <integer
            name="flight_speed"
            format="valid-choices: {[1,2,3,4]}"
            on-fail-valid-choices="exception"
        />
    </case>
</choice>
</root>
            """,
            {
                "action": {
                    "action_type": "fight",
                    "fight_move": "punch",
                }
            },
            True,
        ),
        (
            """
<root>
<list name="my_list3">
    <choice discriminator="action_type" on-fail-choice="exception">
        <case name="fight">
            <list name="fight">
                <string
                    format="valid-choices: {['punch','kick','headbutt']}"
                    on-fail-valid-choices="exception"
                />
            </list>
        </case>
        <case name="flight">
            <string
                name="flight_direction"
                format="valid-choices: {['north','south','east','west']}"
                on-fail-valid-choices="exception"
            />
            <integer
                name="flight_speed"
                format="valid-choices: {[1,2,3,4]}"
                on-fail-valid-choices="exception"
            />
        </case>
    </choice>
</list>
</root>
""",
            {
                "my_list3": [
                    {
                        "action_type": "fight",
                        "fight": ["punch", "kick"],
                    },
                    {
                        "action_type": "flight",
                        "flight_direction": "north",
                        "flight_speed": 1,
                    },
                ],
            },
            True,
        ),
        (
            """
<root>
<object name="mychoices">
    <string name="some random thing"/>
    <choice name="action" discriminator="action_type" on-fail-choice="exception">
        <case name="fight">
            <string
                name="fight_move"
                format="valid-choices: {['punch','kick','headbutt']}"
                on-fail-valid-choices="exception"
            />
        </case>
        <case name="flight">
            <object name="flight">
                <string
                    name="flight_direction"
                    format="valid-choices: {['north','south','east','west']}"
                    on-fail-valid-choices="exception"
                />
                <integer
                    name="flight_speed"
                    format="valid-choices: {[1,2,3,4]}"
                    on-fail-valid-choices="exception"
                />
            </object>
        </case>
    </choice>
</object>
</root>
""",
            {
                "mychoices": {
                    "some random thing": "string",
                    "action": {
                        "action_type": "fight",
                        "fight_move": "punch",
                    },
                },
            },
            True,
        ),
        (
            """
<root>
<string
    name="my_string"
    required="false"
/>
</root>
            """,
            {
                "my_string": None,
            },
            True,
        ),
        (
            """
<root>
<string
    name="my_string"
    required="false"
/>
</root>
            """,
            {
                # "my_string": None,
            },
            True,
        ),
        (
            """
<root>
<list
    name="my_list"
>
</list>
</root>
            """,
            {
                "my_list": ["e"],
            },
            True,
        ),
    ],
)
def test_skeleton(xml, generated_json, result):
    xml_schema = ET.fromstring(xml)
    datatype = Object.from_xml(xml_schema)
    assert verify_schema_against_json(datatype, generated_json) is result
