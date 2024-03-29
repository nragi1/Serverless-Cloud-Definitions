import requests
import json
import os
from openai import OpenAI

OpenAI.api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI()

def create_definition(word):
    system = {"role": "system", "content": "You're an AI Definition Bot, You're only response will be the definition of the word (20 words maximum) and nothing else. If the definition is not cloud computing related you will respond with 'Not related'."}
    history = []
    history.insert(0, system)
    history.append({"role": "user", "content": word})
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history,
            stream=False,
            max_tokens=100
        )
        completion = completion.choices[0].message.content
        return completion

    except Exception as e:
        print(e)
        return None
    

def main():
    word = input("Enter a cloud word: ")
    word = word.lower()
    function_url = os.environ.get('FUNCTION_URL')
    url = f"{function_url}/{word}"
    response = requests.get(url)
    if response.status_code == 404:
        create_definition(word)
        
    
    try:
        definition = response.json().get('definition')
        print("definition:", definition)
    except json.JSONDecodeError:
        print("Definition not found")

if __name__ == "__main__":
    word = input("Enter a cloud word: ")
    word = word.lower()
    definition = create_definition(word)
    print("definition: ", definition)