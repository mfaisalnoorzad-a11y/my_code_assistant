import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

from call_function import available_functions
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeError(
        "Missing GEMINI_API_KEY environment variable. Set it in your environment or "
        "in a .env file before running this script."
    )

client = genai.Client(api_key=api_key)


def main(args):
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError(
            "Missing usage metadata in the Gemini response. The API request may have failed."
        )
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    function_calls = getattr(response, "function_calls", None)
    if function_calls is None and response.candidates and response.candidates[0].content.parts:
        function_calls = [
            part.function_call
            for part in response.candidates[0].content.parts
            if getattr(part, "function_call", None)
        ]
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    elif response.text:
        print(response.text)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    main(args)
