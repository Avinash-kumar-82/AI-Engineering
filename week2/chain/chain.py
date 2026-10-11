import os
from dotenv import load_dotenv
from groq import Groq
from time import sleep
from pathlib import Path

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY");
if not my_api_key:
    raise ValueError("GROQ API Key not found")
client=Groq(api_key=my_api_key);
model="openai/gpt-oss-20b";
JD="""
we are hiring a python Backend Developer

Requirements:
-strong python
-FastAPI or Django
-PostgresSQL
-Docker
-AWS
-REST APIs
- 2+ years of experiences
"""

RESUME="""
Name:Avinash Kumar
Experience:
3 year as a software Developer

Skills:
python,FastAPI,MySQL , Docker, REST APIs, Git

Projects:
Build a food Delivery backend using FastAPI and MySQL
Deployed application using Docker
"""

def ask_llm(system_prompt,user_prompt):
   sys_msg={
        "role": "system",
        "content": system_prompt
    }

   user_msg={
       "role":"system",
       "content":user_prompt
   }

   messages=[sys_msg,user_msg]
   response=client.chat.completions.create(
       model=model,
       messages=messages
   )
   answer=response.choices[0].message.content
   return answer

def step1_res_extract(RESUME):
    print("STEP 1")
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this resume
    {RESUME}
    """
    return ask_llm(system_prompt, user_prompt)

def step2_JD_extract(JD):
    print("step2")
    system_prompt="""
    You are a professional HR assistant. Extract the skills from the Job description  provided.
    Only return the skills no other information. Do not invent any skills by yourself.
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt=f"""
    Extract the skills from this JD
    {JD}
    """
    return ask_llm(system_prompt, user_prompt)

def step3_match(candidate,jd):
    print("step3")
    system_prompt="""
    You are a professional HR assistant. compare the skills of candidate and the skills required in the JD and produce a final score between
    1 and 100. also produce a short verdict whther the candidate is a good fit for the role.
    """
    user_prompt=f"""
    Compare and match the skills
    JD:
    {jd}
    Candidate:
    {candidate}
    """
    return ask_llm(system_prompt, user_prompt)

candidate=step1_res_extract(RESUME)
print(candidate)
sleep(2)
jd=step2_JD_extract(JD)
print(jd)
sleep(2)
score=step3_match(candidate,jd)
print(score)