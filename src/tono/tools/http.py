# A function that sends a HTTP request to a server and returns the response.

from typing import Optional, Literal
import httpx


def http_request(
    url,
    method=Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    headers=Optional[dict],
    data: Optional[dict] = None,
):
    """Send a HTTP request to a server and return the response.
    :param url: The URL of the server.
    :param method: The HTTP method to use. Default is GET.
    :param headers: The headers to send with the request.
    :param data: The data to send with the request.

    :return: The response from the server.
    
    """
    try:
        response = httpx.request(method, url, headers=headers, data=data)
        return response
    except Exception as e:
        return e
