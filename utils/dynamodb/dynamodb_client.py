import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

CONNECT_TIMEOUT = os.getenv("DYNAMODB_CONNECT_TIMEOUT", 1)
READ_TIMEOUT = os.getenv("DYNAMODB_READ_TIMEOUT", 1)
TOTAL_MAX_ATTEMPTS = os.getenv("DYNAMODB_TOTAL_MAX_ATTEMPTS", 2)
MAX_POOL_CONNECTIONS = os.getenv("MAX_POOL_CONNECTIONS", 20)
DYNAMODB_ENDPOINT_URL = os.getenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "ap-south-1")


def create_dynamodb_client():
    config = Config(
        connect_timeout=int(CONNECT_TIMEOUT),
        read_timeout=int(READ_TIMEOUT),
        retries={"mode": "standard", "total_max_attempts": int(TOTAL_MAX_ATTEMPTS)},
        max_pool_connections=int(MAX_POOL_CONNECTIONS),
    )

    return boto3.client(
        "dynamodb",
        config=config,
        region_name=AWS_REGION_NAME,
        endpoint_url=DYNAMODB_ENDPOINT_URL,
    )
