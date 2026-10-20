import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("Api error")

Client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"


class Ticket(BaseModel):
    name: str
    date_time: str
    email: str
    issue: str


schema = Ticket.model_json_schema()

response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information strictly based on this schema {schema} and give me a json output
"""

# Take the complaint from the user
text = input("Please describe your complaint: ")

prompt = f""" This is a customer ticket. Please extract the personal information from this {text}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}

message = {
    "role": "user",
    "content": prompt
}

messages = [message_system, message]

response = Client.chat.completions.create(model=model, messages=messages, temperature=1, response_format=response_format)
answer = response.choices[0].message.content
print(answer)

# Read the JSON into the Ticket model
data_file = json.loads(answer)
ticket = Ticket(**data_file)

print("Name:", ticket.name)
print("Date/Time:", ticket.date_time)
print("Email:", ticket.email)
print("Issue:", ticket.issue)
