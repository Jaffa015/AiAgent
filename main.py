"""
AI Agent

Usage: main.py <prompt> [--verbose]

Options:
  -h, --help     Show this screen.
  --verbose      Print more text.
"""

### IMPORTS
import os
import sys
import docopt
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from config import MAX_ITTERATIONS
from functions.call_function import call_function, available_functions


def main():
    ### LOAD CONFIG
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    args = docopt.docopt(__doc__)
    user_prompt = args["<prompt>"]
    verbose = args["--verbose"]

    ### SETUP ENVIRONMENT
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="User", parts=[types.Part(text=user_prompt)]),
    ]

    iterations = 0
    for i in range(MAX_ITTERATIONS):
        iterations += 1
        if iterations > MAX_ITTERATIONS:
            print(f"Maximum iterations ({MAX_ITTERATIONS}) reached.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f"Final response:\n{final_response}")
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(client, messages: list, verbose):
    # client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response.response
        ):
            raise Exception("Error: empty function call response")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception(f"Error, no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
