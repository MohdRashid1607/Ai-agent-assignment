import json

import agent


class FakeFunctionCall:
    def __init__(self, name, arguments, call_id="test-call-1"):
        self.type = "function_call"
        self.name = name
        self.arguments = arguments
        self.id = call_id


class FakeInteraction:
    def __init__(self, interaction_id, steps=None, output_text=""):
        self.id = interaction_id
        self.steps = steps or []
        self.output_text = output_text


class FakeInteractions:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self.responses.pop(0)


class FakeClient:
    def __init__(self, responses):
        self.interactions = FakeInteractions(responses)


def test_successful_weather_request(monkeypatch):
    """The agent should call the weather tool and return the final answer."""

    function_call = FakeFunctionCall(
        name="get_weather",
        arguments={"city": "Dubai"},
    )

    first_response = FakeInteraction(
        interaction_id="interaction-1",
        steps=[function_call],
    )

    final_response = FakeInteraction(
        interaction_id="interaction-2",
        output_text="Dubai is currently 33.6°C with clear skies.",
    )

    fake_client = FakeClient(
        [first_response, final_response]
    )

    monkeypatch.setattr(agent, "client", fake_client)

    monkeypatch.setattr(
        agent,
        "get_weather",
        lambda city: {
            "status": "ok",
            "city": city,
            "temperature_c": 33.6,
            "windspeed_kmh": 1.5,
            "weathercode": 0,
        },
    )

    result = agent.run_agent(
        "What's the current weather in Dubai?"
    )

    assert "33.6" in result
    assert len(fake_client.interactions.calls) == 2

    first_call = fake_client.interactions.calls[0]

    assert first_call["model"] == agent.MODEL
    assert first_call["tools"] == agent.TOOLS


def test_weather_tool_error(monkeypatch):
    """The agent should handle a weather-tool error without crashing."""

    function_call = FakeFunctionCall(
        name="get_weather",
        arguments={"city": "xyzabc123"},
    )

    first_response = FakeInteraction(
        interaction_id="interaction-error-1",
        steps=[function_call],
    )

    final_response = FakeInteraction(
        interaction_id="interaction-error-2",
        output_text=(
            "I could not retrieve the weather because "
            "the location was not found."
        ),
    )

    fake_client = FakeClient(
        [first_response, final_response]
    )

    monkeypatch.setattr(agent, "client", fake_client)

    monkeypatch.setattr(
        agent,
        "get_weather",
        lambda city: {
            "status": "error",
            "reason": f"No location found for '{city}'.",
        },
    )

    result = agent.run_agent(
        "What's the current weather in xyzabc123?"
    )

    assert "could not retrieve" in result.lower()
    assert len(fake_client.interactions.calls) == 2

    second_call = fake_client.interactions.calls[1]

    function_result = second_call["input"][0]

    assert function_result["type"] == "function_result"
    assert function_result["name"] == "get_weather"
    assert function_result["call_id"] == "test-call-1"

    returned_result = json.loads(
        function_result["result"][0]["text"]
    )

    assert returned_result["status"] == "error"


def test_non_weather_question_does_not_use_tool(monkeypatch):
    """The agent should answer a non-weather question without using the tool."""

    first_response = FakeInteraction(
        interaction_id="interaction-no-tool",
        steps=[],
        output_text="25 multiplied by 48 is 1,200.",
    )

    fake_client = FakeClient(
        [first_response]
    )

    monkeypatch.setattr(agent, "client", fake_client)

    weather_called = False

    def fake_weather(city):
        nonlocal weather_called
        weather_called = True
        return {
            "status": "ok",
            "city": city,
        }

    monkeypatch.setattr(
        agent,
        "get_weather",
        fake_weather,
    )

    result = agent.run_agent(
        "What is 25 multiplied by 48?"
    )

    assert result == "25 multiplied by 48 is 1,200."
    assert weather_called is False
    assert len(fake_client.interactions.calls) == 1

    assert fake_client.interactions.calls[0]["input"] == (
        "What is 25 multiplied by 48?"
    )
