import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

from call_function import available_functions, call_function
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
    for i in range(20):
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
            if i == 0:
                print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Add model output candidates to conversation history.
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)

        # Collect any function calls the model wants to make.
        function_calls = getattr(response, "function_calls", None)
        if function_calls is None and response.candidates and response.candidates[0].content.parts:
            function_calls = [
                part.function_call
                for part in response.candidates[0].content.parts
                if getattr(part, "function_call", None)
            ]

        function_results: list[types.Part] = []

        if function_calls:
            for function_call_obj in function_calls:
                # Call the function via our dispatcher.
                function_call_result = call_function(function_call_obj, verbose=args.verbose)

                if not function_call_result.parts:
                    raise RuntimeError("Tool call returned Content with no parts.")

                first_part = function_call_result.parts[0]
                if first_part.function_response is None:
                    raise RuntimeError("Tool call part is missing function_response.")

                func_resp = first_part.function_response
                if func_resp.response is None:
                    raise RuntimeError("Tool function_response is missing response payload.")

                function_results.append(first_part)

                if args.verbose:
                    print(f"-> {func_resp.response}")

            messages.append(types.Content(role="user", parts=function_results))
            continue

        # No tool calls means this should be the final model response.
        if response.text:
            print("Final response:")
            print(response.text)
        else:
            print("Final response was empty.")
        return

    print("Reached max iterations (20) without a final response.")
    sys.exit(1)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    main(args)
