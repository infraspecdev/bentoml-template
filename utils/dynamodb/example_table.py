import json
import os
from botocore.exceptions import ClientError

from utils.dynamodb.dynamodb_client import create_dynamodb_client
from utils.dynamodb.fetch_data import fetch_data_from_dynamodb


def create_dynamodb_table(dynamodb_client, TABLE_NAME):
    """
    Creates a DynamoDB table if it doesn't already exist.

    Args:
            dynamodb_client (boto3.client): A boto3 client for DynamoDB.
            TABLE_NAME (str): The name of the table to create.
    """

    try:
        dynamodb_client.create_table(
            TableName=TABLE_NAME,
            AttributeDefinitions=[
                {"AttributeName": "artist", "AttributeType": "S"},
                {"AttributeName": "song", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "artist", "KeyType": "HASH"},
                {"AttributeName": "song", "KeyType": "RANGE"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
        )
        print(f"Table '{TABLE_NAME}' created successfully.")
    except ClientError as error:
        if error.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Table '{TABLE_NAME}' already exists. Skipping creation.")
        else:
            raise error


def populate_sample_data(dynamodb_client, TABLE_NAME):
    data_file_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_file_path, "r") as datafile:
        records = json.load(datafile)
    for record in records:
        item = {
            "artist": {"S": record["artist"]},
            "song": {"S": record["song"]},
            "publisher": {"S": record["publisher"]},
        }
        dynamodb_client.put_item(TableName=TABLE_NAME, Item=item)


if __name__ == "__main__":
    client = create_dynamodb_client()
    TABLE_NAME = "music"
    create_dynamodb_table(client, TABLE_NAME)
    populate_sample_data(client, TABLE_NAME)

    query = {"song": {"S": "song-1"}, "artist": {"S": "artist-1"}}
    data = fetch_data_from_dynamodb(TABLE_NAME=TABLE_NAME, query=query)
    print(f"Data: {data}")
