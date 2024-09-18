from django.utils import timezone

def custom_response(status_code, message, data=None):
    """
    Generates a standardized API response.

    :param status_code: HTTP status code for the response
    :param message: Custom message for the response
    :param data: Actual data to include in the response (default is None)
    :return: Dictionary with standardized format
    """
    response_data = {
        "status": "success" if status_code < 400 else "error",
        "code": status_code,
        "message": message,
        "timestamp": timezone.now().isoformat(),
        "data": data
    }
    return response_data
