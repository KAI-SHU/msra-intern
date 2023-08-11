import os

import openai

openai.api_type = "azure"

openai.api_base = "https://gcrgpt4aoai5.openai.azure.com/"

openai.api_version = "2023-03-15-preview"

openai.api_key = "653880d85b6e4a209206c263d7c3cc7a"

 

response = openai.ChatCompletion.create(

  engine="gpt-4",

  messages = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":"Test input"}],

  temperature=0.5,

  max_tokens=800,

  top_p=0.95,

  frequency_penalty=0,

  presence_penalty=0,

  stop=None)

print(response)