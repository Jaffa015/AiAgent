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

### LOAD CONFIG
args = docopt.docopt(__doc__)
user_prompt = args["<prompt>"]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

### SETUP ENVIRONMENT
client = genai.Client(api_key=api_key)

### FUNCTIONS

### SCRIPT
messages = [
    types.Content(role="User", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if args["--verbose"]:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

print("AI Response:\n" + response.text)