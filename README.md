Created a Command-line AI agent using Gemini API for coding assistant, this was a learning project to understand APIs, agents, and to understand functional programming in python.
## Features

- **CLI chatbot using Gemini**
  - Sends your prompt to `gemini-2.5-flash` via the `google-genai` SDK.
  - Optional `--verbose` flag to show token usage and tool call results.

- **Safe tool calling**
  - All tools accept a `working_directory` and validate that paths never escape it.
  - All tools return **strings**, including errors prefixed with `Error:`, so the LLM can handle failures gracefully.

- **Implemented tools**

  - `get_files_info(working_directory, directory=".")`  
    List files and directories, with size and `is_dir` flag.

  - `get_file_content(working_directory, file_path)`  
    Read file contents (up to `MAX_CHARS`), appending a truncation note if the file is too large.

  - `write_file(working_directory, file_path, content)`  
    Write or overwrite files, creating parent directories as needed.

  - `run_python_file(working_directory, file_path, args=None)`  
    Execute a Python file with optional arguments via `subprocess.run`, capturing stdout/stderr and exit code.

- **Function declarations (tool schemas)**
  - Each tool has a `types.FunctionDeclaration` schema describing its parameters and types.
  - All declarations are bundled into a single `types.Tool` (`available_functions`) and passed into Gemini so it knows how to call them.

- **Central dispatcher**
  - `call_function(function_call, verbose=False)` in `call_function.py`:
    - Maps function names (`get_files_info`, `get_file_content`, etc.) to the actual Python functions.
    - Injects `working_directory="./calculator"` into every call.
    - Wraps the string result into a `types.Content` + `function_response` object for the model to consume.

---

## How it works

1. **CLI entrypoint**: `main.py`
   - Parses:
     - `user_prompt` (positional argument)
     - `--verbose` (flag)
   - Builds a `types.Content` user message and calls:

     client.models.generate_content(
         model="gemini-2.5-flash",
         contents=messages,
         config=types.GenerateContentConfig(
             tools=[available_functions],
             system_instruction=system_prompt,
         ),
     )
     
