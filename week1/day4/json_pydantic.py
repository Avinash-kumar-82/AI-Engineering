import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
import json
load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY");
if not groq_api_key:
    raise ValueError("API key not found ")

# Create Groq client
client = Groq(api_key=groq_api_key)
role="user"
# Model
model = "openai/gpt-oss-20b";


# structure it
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}

system_prompt=f"""Extract the personal infromation from the ticket strictly based on this schema and give a json output {schema}"""

message_system={
    "role":"system",
    "content":system_prompt
}
text="Hello My name is Avinash.My mother is kavi.I have an iphone which is not working at all. My address is delhi My email is abc@gmail.com.My contact number is 93543434323"
prompt=f"""
This is a customer ticket.Please extract the personal information from this {text}
"""

message={
    "role":role,
    "content":prompt
}
msg=[message_system,message]

response=client.chat.completions.create(
    model=model,
    messages=msg,
    temperature=2,
    response_format=response_format
)
print("#######################################")

answer=response.choices[0].message.content;
print(answer)

raw_json=answer
data_file=json.loads(raw_json)

ticket=Ticket(**data_file)

print(f" name:{ticket.name}\n email:{ticket.email}\n issue:{ticket.issue}")