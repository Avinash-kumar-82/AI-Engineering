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

# Messages
# messages = [
#     {
#         "role": "system",
#         "content": "You are my strict Office colleague who is also my manager."
#     },
#     {
#         "role": "user",
#         "content": prompt
#     }
# ]

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

# Send request to Groq
response = client.chat.completions.create(
    model=model,
    messages=messages,
    temperature=2
)

# Print separator
print("###########################################################")

# Get the assistant's response
answer = response.choices[0].message.content

print("Answer:")
# print(repr(answer))
print(answer)

# If content is empty, show the complete response for debugging
if not answer:
    print("\nFull response:")
    print(response)
