def format_error_message(errors):
    """Formats the Pydantic validation errors into a simple, user-friendly structure."""
    formatted_errors = []
    for error in errors:
        loc = error.get("loc", [])
        msg = error.get("msg", "")
        if loc and msg:
            field = loc[-1]
            formatted_errors.append({"field": field, "message": msg})
    return formatted_errors
