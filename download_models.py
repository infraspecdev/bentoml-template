import os
import boto3
import configparser


def load_config(config_file_path):
    config = configparser.ConfigParser()
    try:
        config.read(config_file_path)
        return config
    except PermissionError as e:
        raise PermissionError(f"Permission denied: {e}")
    except Exception as e:
        raise Exception(f"Error reading configuration from {config_file_path}: {e}")


def list_model_objects(s3_client, bucket, prefix):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
        return response.get("Contents", [])
    except Exception as e:
        raise Exception(
            f"Error listing objects in S3 bucket {bucket} with prefix {prefix}: {e}"
        )


def download_model(s3_client, bucket, file_path, dest_path):
    try:
        s3_client.download_file(bucket, file_path, dest_path)
        print(f"Downloaded {file_path} to {dest_path}")
    except Exception as e:
        raise Exception(f"Error downloading model from S3: {file_path}: {str(e)}")


def download_models():
    config_file_path = "./configs/config.ini"

    try:
        config = load_config(config_file_path)
        s3_bucket = config.get("S3", "bucket")
        s3_models_dir = config.get("S3", "dir")
        download_models_dest_dir = config.get("Model", "dest_dir")

        s3_client = boto3.client("s3")
        objects = list_model_objects(s3_client, s3_bucket, s3_models_dir)

        for obj in objects:
            file_path = obj["Key"]

            if not file_path.endswith(".pickle"):
                continue

            relative_path = os.path.relpath(file_path, s3_models_dir)
            dest_path = os.path.join(download_models_dest_dir, relative_path)

            print(f"File path: {file_path}, Dest path: {dest_path}")

            if not dest_path.strip():
                raise ValueError(
                    "Destination path is empty. Check the configuration and paths."
                )

            # Ensure the destination directory exists
            dest_dir = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)

            download_model(s3_client, s3_bucket, file_path, dest_path)

    except Exception as e:
        raise Exception(f"Failed to download models from S3: {e}")


if __name__ == "__main__":
    download_models()
