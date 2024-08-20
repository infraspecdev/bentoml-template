# DynamoDB Online Feature Store

## Local DynamoDB Setup with Python

To set up a local DynamoDB instance and interact with it using Python scripts.

1. **Install and Run DynamoDB locally:**

   Follow the official AWS documentation to download and set up DynamoDB
   locally. [Installation Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)

2. **Create and Populate a Table:**

   The script `utils/dynamodb/example_table.py` demonstrates how to:

    - Create a DynamoDB table named "songs-table" with relevant attributes.
    - Populate the table with sample data from `utils/dynamodb/data.json`.
    - Use the `fetch_data_from_dynamodb` function (located in `utils/dynamodb/fetch_data.py`) to retrieve data from the
      table.

   To run: `python -m utils.dynamodb.example_table`

3. **Script Breakdown:**

   The provided scripts offer functionalities for:

    - Dynamodb client creation (method `create_dynamodb_client` in `dynamodb_client.py`)
    - Table creation (method `create_dynamodb_table` in `example_table.py`)
    - Data loading (method `populate_sample_data` in `example_table.py`)
    - Data fetching (`fetch_data_from_dynamodb.py`)

4. **Additional Resources:**
    - Programming Amazon DynamoDB with Python and
      Boto3: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/programming-with-python.html (Provides
      in-depth guidance on using Boto3 to interact with DynamoDB)
    - Boto3 DynamoDB
      Documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html (Reference
      for Boto3's DynamoDB functionalities)

## Environment Variables

The following environment variables can be configured `(in .env file)` to update the dynamodb client configuration.

```bash
  DYNAMODB_CONNECT_TIMEOUT
  DYNAMODB_READ_TIMEOUT
  DYNAMODB_TOTAL_MAX_ATTEMPTS
  MAX_POOL_CONNECTIONS
  DYNAMODB_ENDPOINT_URL
  AWS_REGION_NAME
```
