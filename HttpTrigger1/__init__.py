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
    definition = req.route_params.get('definition')
    logging.info(f"Definition: {definition}")
    
    response = container.read_item(item=definition, partition_key=definition)
    item = response.get('definition')
    
    if not item:
        return func.HttpResponse("Definition not found", status_code=404)
    
    return func.HttpResponse(json.dumps({"definition": item}), mimetype="application/json")
