from utils.common.formatters import format_error_message


def test_format_error_message():
    errors = [
        {
            "type": "missing",
            "loc": ("text",),
            "msg": "Field required",
            "input": {
                "text1": 21,
            },
            "url": "https://errors.pydantic.dev/2/v/missing",
        }
    ]
    formatted_errors = format_error_message(errors)

    assert formatted_errors == [{"field": "text", "message": "Field required"}]
