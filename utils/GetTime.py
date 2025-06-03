def check_response_time_from_server(response, type_request):
    response_time_ms = response.elapsed.total_seconds() * 1000
    if type_request == "get" or type_request == "delete":
        assert 100 <= response_time_ms <= 500, "The time of response is more than expected"
    elif type_request == "post" or type_request == "put":
        assert 200 <= response_time_ms <= 800, "The time of response is more than expected"
