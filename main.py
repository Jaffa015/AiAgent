"""
AI Agent

Usage: main.py <prompt> [--verbose]

Options:
  -h, --help     Show this screen.
  --verbose      Print more text.
"""

### IMPORTS
import os
import docopt
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
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

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Error: Missing function return value")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print("AI Response:\n" + response.text)


if __name__ == "__main__":
    main()
