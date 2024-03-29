import logging
import azure.functions as func
import json
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os

endpoint = os.environ['COSMOS_ENDPOINT']
credential = os.environ['COSMOS_KEY']
client = CosmosClient(endpoint, credential=credential)
database_name = 'cloud-definition'
database = client.get_database_client(database_name)
container_name = 'definitions'
container = database.get_container_client(container_name)



def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    word = req_body.get('word')
    definition = req_body.get('definition')
    
    if definition == "Not related." or definition == "Not related":
        return func.HttpResponse("Not related", status_code=200)
    else:
        data = {
            "id": word,
            "definition": definition
        }

        container.upsert_item(data)
        return func.HttpResponse("Definition created", status_code=200)