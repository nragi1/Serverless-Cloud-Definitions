import requests
import json
import os

def main():
    definition = input("Enter a cloud word: ")
    definition = definition.lower()
    function_url = os.environ.get('FUNCTION_URL')
    url = f"{function_url}/{definition}"
    response = requests.get(url)
    
    try:
        definition = response.json().get('definition')
        print("definition:", definition)
    except json.JSONDecodeError:
        print("Definition not found")

if __name__ == "__main__":
    main()