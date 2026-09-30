# Groq Brand Name Generator (System Prompt + Temperature Demo)

A small Python script that asks a Groq-hosted LLM to act as a **brand manager** and suggest a **single one-word name** for a food company. It also demonstrates how a **system prompt** shapes behavior and how **temperature** affects randomness.

---

## Table of Contents

1. [What this script does](#what-this-script-does)
2. [Prerequisites and setup](#prerequisites-and-setup)
3. [The full script](#the-full-script)
4. [Code walkthrough](#code-walkthrough)
5. [Key concepts](#key-concepts)
6. [Observations and issues in this version](#observations-and-issues-in-this-version)
7. [Improved version](#improved-version)
8. [Experiments to try](#experiments-to-try)
9. [Troubleshooting](#troubleshooting)
10. [Notes](#notes)

---

## What this script does

1. Loads `GROQ_API_KEY` from a `.env` file.
2. Creates a Groq client.
3. Sends a chat request with two messages:
   - a **system** message telling the model to be a brand manager who returns exactly one one-word name,
   - a **user** message asking for a name for a food company.
4. Prints the model's answer.
5. If the answer is empty, prints the full response object for debugging.

---

## Prerequisites and setup

- Python 3.8+
- A Groq API key

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install groq python-dotenv
```

Create a `.env` file next to the script:

```
GROQ_API_KEY=your_api_key_here
```

Add `.env` to `.gitignore` so the key is never committed.

---

## The full script

```python
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

# Create Groq client
client = Groq(api_key=groq_api_key)

# Model
model = "openai/gpt-oss-20b"

# User prompt
prompt = "I love you baby!"

messages = [
    {
        "role": "system",
        "content": "You are brand manager who suggests name for my food company.name should be in one word. suggest only one"
    },
    {
        "role": "user",
        "content": "Suggest a name for my food company"
    }
]

response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=2
)

print("###########################################################")

answer = response.choices[0].message.content

print("Answer:")
print(answer)

if not answer:
    print("\nFull response:")
    print(response)
```

---

## Code walkthrough

### Environment and client

```python
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env")
client = Groq(api_key=groq_api_key)
```

Loads the secret from `.env`, fails fast with a clear message if it is missing, then builds the client. This is the same pattern as the previous script.

### Model

```python
model = "openai/gpt-oss-20b"
```

The model identifier as Groq lists it. This is an open-weight **reasoning** model, which matters for the empty-answer issue described below. Model names change over time, so confirm this one is still listed in the Groq docs.

### Unused variable

```python
prompt = "I love you baby!"
```

This variable is **not used** in the active `messages`. It belongs to the commented-out block, which used a different persona. See the next section.

### The commented-out messages block

```python
# messages = [
#     {"role": "system", "content": "You are my strict Office colleague who is also my manager."},
#     {"role": "user", "content": prompt}
# ]
```

This was an earlier experiment: same user prompt, but a system message that makes the model reply as a strict manager. It is a good illustration that **the same user message produces very different replies depending on the system prompt**. Only one `messages` list is active at a time (the later assignment overwrites the earlier one).

### The active messages

```python
messages = [
    {"role": "system", "content": "You are brand manager who suggests name for my food company.name should be in one word. suggest only one"},
    {"role": "user", "content": "Suggest a name for my food company"}
]
```

- The **system** message sets the role and the output rules (one word, only one suggestion).
- The **user** message is the actual request.

### The API call

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=2
)
```

`temperature=2` is the notable setting. See Key concepts.

### Reading and printing the answer

```python
answer = response.choices[0].message.content
print(answer)
```

`choices` is a list (usually with one item); `.message.content` holds the assistant's text.

### Debug fallback

```python
if not answer:
    print("\nFull response:")
    print(response)
```

Prints the whole response object when the content is empty or `None`. Good instinct, since empty content is a real possibility with this configuration.

---

## Key concepts

### System prompt vs user prompt

| Role | Purpose |
|---|---|
| `system` | Sets persona, tone, and rules for the whole conversation |
| `user` | The actual request or question |
| `assistant` | Previous model replies (used when continuing a conversation) |

The system prompt is the best place for constraints like "one word only".

### Temperature

Temperature controls randomness in token selection.

| Value | Behavior |
|---|---|
| `0` to `0.3` | Focused, predictable, near-deterministic |
| `0.5` to `0.9` | Balanced, good default for creative tasks |
| `1.0` | The model's natural distribution |
| `1.5` to `2` | Very random, quality can drop sharply |

For a naming task, some randomness is useful because you want varied ideas. But `2` is at the extreme top of the range (Groq's documented maximum, as far as I know; verify in the API reference). At that level, output can become odd, off-instruction, or even malformed, which is likely why your script includes an empty-answer check.

### Reasoning models and empty content

`openai/gpt-oss-20b` is a reasoning model: it generates internal reasoning tokens before the final answer. If the token budget is consumed by reasoning, or the output degrades at very high temperature, `message.content` can come back **empty**, with `finish_reason` set to something like `"length"`. Checking `finish_reason` and any reasoning field on the message helps diagnose it.

---

## Observations and issues in this version

| # | Observation | Impact | Suggestion |
|---|---|---|---|
| 1 | `temperature=2` is extreme | Erratic or empty output, ignores "one word" rule more often | Try `0.8` to `1.2` |
| 2 | `prompt` variable is unused | Confusing leftover | Remove it, or use it in the user message |
| 3 | System prompt has typos: "You are brand manager", "company.name" | Slightly ambiguous instruction | Rewrite cleanly (see below) |
| 4 | "One word" is a request, not a guarantee | The model may return a phrase or extra text | Validate and post-process in code |
| 5 | The user message does not mention the type of food | Generic, repetitive names | Add cuisine, audience, and tone |
| 6 | No `max_completion_tokens` set | Can't control reasoning and output budget | Set a generous limit for reasoning models |
| 7 | No error handling around the API call | Network or auth errors crash the script | Wrap in `try/except` |

---

## Improved version

```python
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=groq_api_key)

model = "openai/gpt-oss-20b"

system_prompt = (
    "You are a brand manager who names food companies. "
    "Reply with exactly one brand name, in a single word, and nothing else. "
    "No punctuation, no explanation."
)

user_prompt = "Suggest a name for my food company. It sells healthy street food for college students."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

try:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1.0,
        max_completion_tokens=1024,   # leaves room for reasoning + answer
    )
except Exception as e:
    raise SystemExit(f"Request failed: {e}")

choice = response.choices[0]
answer = (choice.message.content or "").strip()

print("#" * 60)

if not answer:
    print("Empty answer. finish_reason:", choice.finish_reason)
    print(response)
else:
    # Enforce the one-word rule in code, since the model may not obey it
    name = answer.split()[0].strip(".,!\"'")
    print("Suggested name:", name)
```

Changes: cleaner system prompt, a more specific user request, lower temperature, a token limit, error handling, `finish_reason` in the debug output, and code that enforces the one-word constraint.

---

## Experiments to try

1. **Compare temperatures.** Run the same prompt at `0`, `0.7`, `1`, and `2` several times each. Notice how repeatable (or not) the answers are.
2. **Swap the persona.** Uncomment the "strict manager" system prompt and send "I love you baby!" to see how the system message changes the reply.
3. **Generate many names.** Change the system prompt to "suggest 10 one-word names as a numbered list" and see how the output format changes.
4. **Add constraints.** Ask for names under 8 characters, or names that are easy to pronounce.
5. **Loop for variety.** Call the API 5 times at a moderate temperature and collect the unique names.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `answer` is empty or `None` | Reasoning consumed the token budget, or output degraded at high temperature | Lower `temperature`, set `max_completion_tokens`, check `finish_reason` |
| Reply is more than one word | Model didn't follow the instruction | Tighten the system prompt and post-process in code |
| Gibberish or odd text | `temperature=2` | Use a value around `0.7` to `1.2` |
| Same name every time | Temperature too low, vague prompt | Raise temperature, add more context to the prompt |
| `401 Unauthorized` | Wrong or revoked key | Regenerate the key in the Groq Console |
| Model not found | Model renamed or retired | Check the current model list in the Groq docs |
| `429` errors | Rate limit | Wait and retry with backoff |

---

## Notes

- **Names are not checked for availability.** Before adopting a name, check trademarks, domain names, and social handles.
- **Parameter support varies by model.** Options such as `max_completion_tokens` or reasoning-effort settings may differ between models, so confirm against the current Groq API reference.
- **Keep secrets out of code.** Never commit `.env` or paste your API key anywhere public.
