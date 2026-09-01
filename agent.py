import json
import os
import time

from google import genai

from weather_tool import get_weather


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set. "
        "Configure it as a GitHub Codespaces secret."
    )

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.6-flash"


WEATHER_TOOL = {
    "type": "function",
    "name": "get_weather",
    "description": (
        "Gets the current weather for a city. "
        "Use this tool when the user asks about current "
        "weather or temperature for a specific city."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The city name, for example Dubai or London.",
            }
        },
        "required": ["city"],
    },
}


SYSTEM_INSTRUCTION = """
You are a helpful weather assistant.

When the user asks for current weather information,
use the get_weather tool.

Never invent weather data.

If the weather tool returns an error, clearly explain
that the weather could not be retrieved.

Keep responses concise and easy to understand.
"""


def run_agent(user_request: str) -> str:
    """Run the Gemini weather agent."""

    if not user_request or not user_request.strip():
        return "Please enter a question."

    start_time = time.perf_counter()

    print("\n[REQUEST]")
    print(user_request)

    # First interaction: Gemini decides whether the weather
    # tool is needed.
    interaction = client.interactions.create(
        model=MODEL,
        input=user_request,
        tools=[WEATHER_TOOL],
        system_instruction=SYSTEM_INSTRUCTION,
    )

    function_calls = [
        step for step in interaction.steps
        if step.type == "function_call"
    ]

    # No tool call: Gemini answered directly.
    if not function_calls:
        latency = time.perf_counter() - start_time

        print("\n[TOOL SELECTED]")
        print("None")

        print(f"[LATENCY] {latency:.2f} seconds")

        return interaction.output_text

    # Execute each function call.
    for function_call in function_calls:

        print("\n[TOOL SELECTED]")
        print(function_call.name)

        if function_call.name != "get_weather":
            result = {
                "status": "error",
                "reason": "Unsupported tool requested.",
            }

        else:
            arguments = function_call.arguments or {}

            city = arguments.get("city", "")

            print("[TOOL INPUT]")
            print(json.dumps({"city": city}))

            try:
                result = get_weather(city)
            except Exception as exc:
                result = {
                    "status": "error",
                    "reason": f"Tool execution failed: {exc}",
                }

        print("[TOOL RESULT]")
        print(json.dumps(result))

        # Send the tool result back to Gemini.
        interaction = client.interactions.create(
    model=MODEL,
    previous_interaction_id=interaction.id,
    input=[
        {
            "type": "function_result",
            "name": function_call.name,
            "call_id": function_call.id,
            "result": [
                {
                    "type": "text",
                    "text": json.dumps(result),
                }
            ],
        }
    ],
    tools=[WEATHER_TOOL],
    system_instruction=SYSTEM_INSTRUCTION,
)

    latency = time.perf_counter() - start_time

    print("\n[FINAL ANSWER]")
    print(interaction.output_text)

    print(f"\n[LATENCY] {latency:.2f} seconds")

    return interaction.output_text
def main():
    print("Weather AI Agent")
    print("Type 'exit' to quit.")

    while True:
        user_request = input("\nYou: ")

        if user_request.strip().lower() == "exit":
            print("Goodbye!")
            break

        try:
            answer = run_agent(user_request)
            print(f"\nAgent: {answer}")

        except Exception as exc:
            print("\n[AGENT ERROR]")
            print(str(exc))
            print(
                "The agent could not complete the request. "
                "Please try again."
            )


if __name__ == "__main__":
    main()