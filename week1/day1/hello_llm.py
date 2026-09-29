import os;
from pathlib import Path;
from dotenv import load_dotenv;
from groq import Groq;

# first thing we have to load env file
load_dotenv();

# # get api key from env
grok_api_key=os.getenv("GROK_API_KEY");

if not grok_api_key:
    raise ValueError("GROK api key not found");

client=Groq(api_key=grok_api_key);

role="user";
prompt="Do you know Padho with Pratyush";

message={
    "role":role,
    "content":prompt
};

messages=[message];

response=client.chat.completions.create(model=model,messages=message);
print(response)