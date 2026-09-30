# Groq Chat Completion: Basic Starter Script

A minimal Python script that loads an API key from a `.env` file, connects to the **Groq** API, sends a single user prompt to an LLM, and prints the response.

The example prompt is: *"Do you know Padho with Pratyush"*.

---

## Table of Contents

1. [What this project does](#what-this-project-does)
2. [Prerequisites](#prerequisites)
3. [Project structure](#project-structure)
4. [Setup](#setup)
5. [Code walkthrough](#code-walkthrough)
6. [Bugs in the original code and fixes](#bugs-in-the-original-code-and-fixes)
7. [Corrected code](#corrected-code)
8. [Running the script](#running-the-script)
9. [Understanding the response object](#understanding-the-response-object)
10. [Extending the script](#extending-the-script)
11. [Troubleshooting](#troubleshooting)
12. [Notes and caveats](#notes-and-caveats)

---

## What this project does

1. Reads a secret API key from a `.env` file (so it never sits in your source code).
2. Creates a Groq client with that key.
3. Builds a chat message list in the format the API expects.
4. Calls the chat completions endpoint with a chosen model.
5. Prints the result.

---

## Prerequisites

- Python 3.8 or newer
- A Groq account and API key (create one in the Groq Console)
- `pip` for installing packages

---

## Project structure

```
project/
├── main.py          # the script
├── .env             # your secret key (never commit this)
├── .gitignore       # should list .env
├── requirements.txt # dependencies
└── README.md
```

**requirements.txt**

```
groq
python-dotenv
```

**.gitignore**

```
.env
__pycache__/
venv/
```

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt
```

**Create a `.env` file** in the same folder as `main.py`:

```
GROQ_API_KEY=your_api_key_here
```

> Note: your original code used `GROK_API_KEY`. That name is fine as long as it matches in both the `.env` file and the code, but be careful: **Grok** (xAI's model) and **Groq** (the inference company you're actually using here) are different things. The name `GROQ_API_KEY` avoids confusion, and it is also the variable the Groq SDK looks for by default.

---

## Code walkthrough

### 1. Imports

```python
import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
```

| Import | Purpose |
|---|---|
| `os` | Reads environment variables via `os.getenv()` |
| `Path` | Not used in your script. Safe to remove unless you plan to work with file paths |
| `load_dotenv` | Loads variables from `.env` into the process environment |
| `Groq` | The official Groq client class |

### 2. Loading the environment

```python
load_dotenv()
```

This must run **before** you call `os.getenv()`. It reads `.env` and makes its keys available as environment variables.

### 3. Reading and validating the key

```python
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ API key not found")
```

`os.getenv` returns `None` if the variable is missing. Failing early with a clear error is better than getting a confusing authentication error later.

### 4. Creating the client

```python
client = Groq(api_key=groq_api_key)
```

The client object holds your credentials and exposes the API methods.

### 5. Building the message

```python
role = "user"
prompt = "Do you know Padho with Pratyush"

message = {"role": role, "content": prompt}
messages = [message]
```

Chat APIs take a **list** of message dictionaries. Each has:

- `role`: `"system"`, `"user"`, or `"assistant"`
- `content`: the text

Here there is just one message from the user.

### 6. Sending the request

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
)
```

- `model`: which LLM to use (must be defined, see the bugs section)
- `messages`: the full conversation so far

### 7. Printing the result

```python
print(response)
```

This prints the entire response object. To print only the model's text reply, use `response.choices[0].message.content`.

---

## Bugs in the original code and fixes

| # | Problem | Why it fails | Fix |
|---|---|---|---|
| 1 | `model` is never defined | `NameError: name 'model' is not defined` | Define `model = "..."` before the API call |
| 2 | `messages=message` | Passes a single dict instead of a list, so the API rejects it | Use `messages=messages` |
| 3 | Trailing semicolons (`;`) | Legal in Python but unnecessary and non-idiomatic | Remove them |
| 4 | Variable named `grok_api_key` / env var `GROK_API_KEY` | Works if consistent, but confusing (Grok is a different product from Groq) | Rename to `groq_api_key` / `GROQ_API_KEY` |
| 5 | `from pathlib import Path` is unused | Harmless, but clutters the file | Remove it |
| 6 | `print(response)` prints the whole object | Output is noisy | Print `response.choices[0].message.content` |
| 7 | The comment `# # get api key from env` has a doubled `#` | Cosmetic only | Clean up the comment |

The two errors that actually stop the script are **#1** and **#2**.

---

## Corrected code

```python
import os
from dotenv import load_dotenv
from groq import Groq

# Load variables from the .env file first
load_dotenv()

# Read the API key from the environment
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

# Create the client
client = Groq(api_key=groq_api_key)

# Pick a model. Check the Groq docs/console for the current list of models,
# since available models change over time.
model = "llama-3.3-70b-versatile"

# Build the conversation
prompt = "Do you know Padho with Pratyush"
messages = [
    {"role": "user", "content": prompt}
]

# Call the API
response = client.chat.completions.create(
    model=model,
    messages=messages,
)

# Print only the assistant's reply
print(response.choices[0].message.content)
```

---

## Running the script

```bash
python main.py
```

You should see the model's text reply printed to the terminal.

---

## Understanding the response object

`client.chat.completions.create(...)` returns an object shaped roughly like this:

```
response
├── id
├── model
├── choices                     # list, usually length 1
│   └── [0]
│       ├── index
│       ├── finish_reason       # e.g. "stop" or "length"
│       └── message
│           ├── role            # "assistant"
│           └── content         # the actual reply text
└── usage
    ├── prompt_tokens
    ├── completion_tokens
    └── total_tokens
```

Useful accessors:

```python
reply = response.choices[0].message.content
tokens_used = response.usage.total_tokens
finish = response.choices[0].finish_reason
```

---

## Extending the script

### Add a system prompt (controls tone and behavior)

```python
messages = [
    {"role": "system", "content": "You are a helpful assistant. Answer concisely."},
    {"role": "user", "content": prompt},
]
```

### Tune generation

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=0.7,   # lower = more deterministic, higher = more creative
    max_tokens=500,    # cap the length of the reply
)
```

### Stream the response token by token

```python
stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

for chunk in stream:
    piece = chunk.choices[0].delta.content
    if piece:
        print(piece, end="", flush=True)
print()
```

### Build a simple multi-turn chat loop

```python
messages = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(model=model, messages=messages)
    reply = response.choices[0].message.content

    print("AI:", reply)
    messages.append({"role": "assistant", "content": reply})
```

The key idea: the API is **stateless**, so you must resend the whole conversation history each time.

### Wrap the call in error handling

```python
try:
    response = client.chat.completions.create(model=model, messages=messages)
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Request failed: {e}")
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ValueError: ... key not found` | `.env` missing, wrong location, or variable name mismatch | Put `.env` next to `main.py`; make sure the name matches exactly |
| `NameError: name 'model' is not defined` | Model variable never set | Add `model = "..."` |
| `400 Bad Request` / messages error | Passed a dict instead of a list | Use `messages=[{...}]` |
| `401 Unauthorized` | Invalid or expired API key | Regenerate the key in the Groq Console |
| `404` / model not found / decommissioned | Model name is wrong or has been retired | Check the Groq docs for currently available models |
| `429 Too Many Requests` | Rate limit reached | Wait and retry, or add retry logic with backoff |
| `ModuleNotFoundError: dotenv` | Wrong package installed | Install `python-dotenv` (not `dotenv`) |
| `ModuleNotFoundError: groq` | SDK not installed | `pip install groq` |
| `.env` values not loading | Running from a different working directory | Run from the project folder, or use `load_dotenv(Path(__file__).parent / ".env")` |

---

## Notes and caveats

- **Never commit `.env`** or paste your API key into source code or screenshots. If a key leaks, revoke and regenerate it.
- **Model availability changes.** Groq adds and retires models regularly, so verify the model name against their documentation.
- **About the sample prompt.** "Padho with Pratyush" appears to be an education channel or brand. A general-purpose LLM may not have reliable knowledge of it and can produce a confident-sounding but incorrect answer (a hallucination). Treat answers about niche people or channels with skepticism, and verify with a real source.
- **Naming.** Groq (`groq`, the API and SDK used here) and Grok (xAI's chatbot) are unrelated. Using `GROQ_API_KEY` keeps this clear.
