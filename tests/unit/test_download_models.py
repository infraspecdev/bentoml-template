import configparser
from botocore.exceptions import ClientError
import pytest
from unittest.mock import Mock, patch, MagicMock, call

from download_models import (
    load_config,
    list_model_objects,
    download_model,
    download_models,
)


@pytest.fixture
def mock_config():
    config = configparser.ConfigParser()
    config["S3"] = {"bucket": "test-bucket", "dir": "test-dir"}
    config["Model"] = {"dest_dir": "test-dest-dir"}
    return config


@pytest.fixture
def mock_s3_client():
    return Mock()


def test_load_config(tmp_path, mock_config):
    config_file_path = tmp_path / "test_config.ini"
    with open(config_file_path, "w") as f:
        mock_config.write(f)

    loaded_config = load_config(config_file_path)
    assert loaded_config["S3"]["bucket"] == "test-bucket"
    assert loaded_config["S3"]["dir"] == "test-dir"
    assert loaded_config["Model"]["dest_dir"] == "test-dest-dir"


def test_load_config_exception():
    config_file_path = "/path/to/non/existent/config.ini"

    with patch.object(
        configparser.ConfigParser, "read", side_effect=Exception("Test error")
    ):
        with pytest.raises(Exception) as exc_info:
            load_config(config_file_path)

    expected_error_message = (
        f"Error reading configuration from {config_file_path}: Test error"
    )
    assert str(exc_info.value) == expected_error_message


def test_load_config_permission_exception(tmp_path, mock_config):
    config_file_path = tmp_path / "test_config.ini"

    with patch.object(
        configparser.ConfigParser, "read", side_effect=PermissionError("Test error")
    ):
        with pytest.raises(PermissionError) as exc_info:
            load_config(config_file_path)

    expected_error_message = f"Permission denied: Test error"
    assert str(exc_info.value) == expected_error_message


def test_list_model_objects(mock_s3_client):
    bucket = "test-bucket"
    prefix = "test-prefix"

    mock_s3_client.list_objects_v2.return_value = {
        "Contents": [{"Key": "test-prefix/file1.pickle"}]
    }
    objects = list_model_objects(mock_s3_client, bucket, prefix)

    assert len(objects) == 1
    assert objects[0]["Key"] == "test-prefix/file1.pickle"


def test_list_model_objects_with_no_contents(mock_s3_client):
    bucket = "test-bucket"
    prefix = "test-prefix"

    mock_s3_client.list_objects_v2.return_value = {"Contents": []}
    objects = list_model_objects(mock_s3_client, bucket, prefix)
    assert len(objects) == 0


def test_list_model_objects_exception_handling(mock_s3_client):
    bucket = "test-bucket"
    prefix = "test-prefix"

    mock_s3_client.list_objects_v2.side_effect = ClientError(
        {"Error": {"Code": "TestException"}}, "list_objects_v2"
    )

    with pytest.raises(Exception) as exc_info:
        list_model_objects(mock_s3_client, bucket, prefix)

    assert str(exc_info.value) == (
        f"Error listing objects in S3 bucket {bucket} with prefix {prefix}: "
        f"An error occurred (TestException) when calling the list_objects_v2 operation: Unknown"
    )


def test_download_model():
    s3_client_mock = MagicMock()

    bucket = "test-bucket"
    file_path = "test-path/model.pickle"
    dest_path = "/Models/model.pickle"

    download_model(s3_client_mock, bucket, file_path, dest_path)

    s3_client_mock.download_file.assert_called_once_with(bucket, file_path, dest_path)


def test_download_model_exception():
    s3_client_mock = MagicMock()

    bucket = "test-bucket"
    file_path = "test-path/model.pickle"
    dest_path = "/Models/model.pickle"

    with patch.object(
        s3_client_mock, "download_file", side_effect=Exception("Test exception")
    ):
        with pytest.raises(Exception) as exc_info:
            download_model(s3_client_mock, bucket, file_path, dest_path)

    assert (
        str(exc_info.value)
        == f"Error downloading model from S3: {file_path}: Test exception"
    )


@patch("os.makedirs")
@patch("download_models.load_config")
@patch("download_models.list_model_objects")
@patch("download_models.download_model")
def test_download_models(
    mock_download_model, mock_list_model_objects, mock_load_config, mock_makedirs
):
    mock_config = MagicMock()
    mock_config.get.return_value = "test"
    mock_load_config.return_value = mock_config

    mock_list_model_objects.return_value = [{"Key": "test-prefix/file1.pickle"}]

    download_models()

    mock_makedirs.assert_called_once_with("test/../test-prefix", exist_ok=True)

    mock_load_config.assert_called_once()
    mock_config.get.assert_has_calls(
        [call("S3", "bucket"), call("S3", "dir"), call("Model", "dest_dir")]
    )
    mock_list_model_objects.assert_called_once()
    mock_download_model.assert_called_once()


def test_list_model_objects_with_large_number_of_objects(mock_s3_client):
    bucket = "test-bucket"
    prefix = "test-prefix"
    mock_s3_client.list_objects_v2.return_value = {
        "Contents": [{"Key": f"test-prefix/file{i}.pickle"} for i in range(1000)]
    }
    objects = list_model_objects(mock_s3_client, bucket, prefix)
    assert len(objects) == 1000


def test_download_model_with_invalid_bucket():
    s3_client_mock = MagicMock()
    bucket = "invalid-bucket"
    file_path = "test-path/model.pickle"
    dest_path = "/Models/model.pickle"

    # Simulate a ClientError when download_file is called
    s3_client_mock.download_file.side_effect = ClientError(
        {
            "Error": {
                "Code": "NoSuchBucket",
                "Message": "The specified bucket does not exist",
            }
        },
        "download_file",
    )

    with pytest.raises(Exception) as exc_info:
        download_model(s3_client_mock, bucket, file_path, dest_path)
    assert "Error downloading model from S3" in str(exc_info.value)


@patch("os.makedirs")
@patch("download_models.load_config")
@patch("download_models.list_model_objects")
@patch("download_models.download_model")
def test_download_models_with_multiple_files(
    mock_download_model, mock_list_model_objects, mock_load_config, mock_makedirs
):
    mock_config = MagicMock()
    mock_config.get.return_value = "test"
    mock_load_config.return_value = mock_config
    mock_list_model_objects.return_value = [
        {"Key": f"test-prefix/file{i}.pickle"} for i in range(10)
    ]
    download_models()
    assert mock_download_model.call_count == 10
