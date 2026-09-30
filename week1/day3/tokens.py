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
role="user"
# Model
model = "openai/gpt-oss-20b"

# 3 prompts
prompt1 = "Hi!"
prompt2="Explain time travel in Detail"
prompt3="Write a 1000 word essay on Machine learning"

# now put all prompts on list

prompts=[prompt1,prompt2,prompt3]

for pmt in prompts:
    msg={
        "role":role,
        "content":pmt,
    }
    messages=[msg]
    response=client.chat.completions.create(
        model=model,
        messages=messages
    )
    # response=client.chat.completions.create(
    #     model=model,
    #     messages=messages,
    #     max_tokens=50
    # )

    usage=response.usage

    print("#########################################")
    print(f"Prompt: {pmt}\nyour tokens: {usage.prompt_tokens} \ncompletion_tokens: {usage.completion_tokens} \ntotal tokens: {usage.total_tokens}  \nFinish Reason: {response.choices[0].finish_reason}")


    # we have a response.choices[0].finish_reason it says 
