import pytest
from test_helpers.utils import skip_if_no_google

from inspect_ai import Task, eval
from inspect_ai.dataset import Sample
from inspect_ai.model._providers.google import chat_tools
from inspect_ai.scorer import includes
from inspect_ai.tool import ToolInfo, ToolParam, ToolParams


@skip_if_no_google
def test_google_safety_settings():
    safety_settings = dict(
        dangerous_content="medium_and_above",
        hate_speech="low_and_above",
    )

    # note: the log doesn't currently have evidence
    # that the safety settings are successfully passed
    # to google, but to the extent we know they are,
    # this tests whether they are correctly mapped to
    # the requisite enum values and that the google
    # api accepts them without error
    eval(
        Task(
            dataset=[Sample(input="What is 1 + 1?", target=["2", "2.0", "Two"])],
            scorer=includes(),
        ),
        model="google/gemini-1.5-flash",
        model_args=dict(safety_settings=safety_settings),
    )


@pytest.mark.xfail
def test_chat_tools():
    chat_tools(
        tools=[
            ToolInfo(
                name="tool",
                description="tool",
                parameters=ToolParams(
                    type="object",
                    properties=dict(
                        a=ToolParam(type="number"),
                        b=ToolParam(type="string"),
                    ),
                ),
            )
        ]
    )
