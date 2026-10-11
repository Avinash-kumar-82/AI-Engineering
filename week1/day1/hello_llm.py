
import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load environment variables
load_dotenv()

# 2. Get API key from .env
groq_api_key = os.getenv("GROQ_API_KEY")
model = "openai/gpt-oss-20b"

if not groq_api_key:
    raise ValueError("GROQ API key not found")

# 3. Initialize Groq client
client = Groq(api_key=groq_api_key)

# 4. Create the user message
role = "user"
prompt = "Do you know  Virat?"

message = {
    "role": role,
    "content": prompt
}

# 5. Create the messages list
messages = [message]

# 6. Send request to the LLM
response = client.chat.completions.create(
    model=model,
    messages=messages
)

# 7. Print the generated answer
print(response.choices[0].message.content)
