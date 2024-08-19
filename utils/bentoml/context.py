def extract_request_info(request):
    request_headers = request.headers
    http_method = request.get("method")
    api_endpoint = request.get("path")
    host = request_headers.get("host")

    return {http_method: http_method, api_endpoint: api_endpoint, host: host}
