from typing import Dict, Union
import botocore

from utils.dynamodb.dynamodb_client import create_dynamodb_client
from utils.structure_logging.logger_config import logger


def fetch_data_from_dynamodb(table_name: str, query: Dict) -> Union[Dict, None]:
    """
    Fetches data from a DynamoDB table based on the provided table name and query. The connect
    and read timeout is set to 1.0 second. The total number of retries can be set by the user
    from the environment variable DYNAMODB_TOTAL_MAX_ATTEMPTS

    Args:
            table_name (str): Name of the DynamoDB table to query.
            query (Dict): Query parameters for the DynamoDB table.

    Returns:
            Union[Dict, None]: The fetched data as a dictionary or None if no data is found.
    """
    try:
        dynamodb_client = create_dynamodb_client()
        response = dynamodb_client.get_item(TableName=table_name, Key=query)
        return response.get("Item")
    except botocore.exceptions.ClientError as error:
        logger.exception(f"DynamoDB Client Error: {error.response['Error']['Message']}")
        return None
    except Exception:
        logger.exception("Error fetching data from DynamoDB")
        return None
