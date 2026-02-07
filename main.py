import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

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
        contents=messages
    )
    if response.usage_metadata is None:
        raise RuntimeError(
            "Missing usage metadata in the Gemini response. The API request may have failed."
        )
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    main(args)
