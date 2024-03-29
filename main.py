import requests
import json
import os
from openai import OpenAI

OpenAI.api_key = os.environ.get('OPENAI_API_KEY')
client = OpenAI()

def create_definition(word):
    system = {"role": "system", "content": "Provide a concise definition (20 words maximum) related to cloud computing or cloud platforms for the following term. Use only necessary punctuation. If the term is not related to cloud computing, respond with 'Not related'."}
    history = []
    history.insert(0, system)
    history.append({"role": "user", "content": f"Term: {word}"})
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=history,
            stream=False,
            max_tokens=100
        )
        definition = completion.choices[0].message.content
        
        data = {
            "word": word,
            "definition": definition
        }
        
        function_url = os.environ.get('CREATE_FUNCTION_URL')
        requests.post(function_url, json=data)
        
        if definition == "Not related":
            return None
        else:
            return definition
        
        

    except Exception as e:
        print(e)
        return None
    

def main():
    while True:
        word = input("Enter a cloud word: ")
        if word.lower() == "exit":
            break
        word = word.lower()
        function_url = os.environ.get('FUNCTION_URL')
        url = f"{function_url}/{word}"
        response = requests.get(url)
        if response.status_code == 404:
            print("Definition not found, creating definition...")
            if create_definition(word) is None:
                print("Not related")
                return
            else:
                definition = create_definition(word)
                print("definition:", definition)

        elif response.status_code == 200:
            definition = response.json().get('definition')
            if definition == "Not related." or definition == "Not related":
                print("Not related")
                return
            else:
                print("definition:", definition)

        else:
            print("An error occurred")
            return

if __name__ == "__main__":
    main()