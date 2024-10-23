from typing import Optional, Literal
from tono.lib import logger
from bs4 import BeautifulSoup
import httpx


class THTTPRequest:
    url: str
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"] = "GET"
    headers: Optional[dict] = None
    data: Optional[dict] = None


def http_request(**kwargs: THTTPRequest):
    """Send a HTTP request to a server and return the response.
    :param url: The URL of the server.
    :param method: The HTTP method to use. Default is GET.
    :param headers: The headers to send with the request.
    :param data: The data to send with the request.

    :return: The response from the server.

    """
    url = kwargs.get("url")
    method = kwargs.get("method", "GET")
    headers = kwargs.get(
        "headers",
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"  # noqa
        },
    )
    data = kwargs.get("data", {})

    try:
        r = httpx.request(method, url, headers=headers, data=data)
        # use beautiful soup to extract the body only
        soup = BeautifulSoup(r.content, "html.parser")

        # delete all the script tags
        for script in soup.find_all("script"):
            script.extract()

        content = str(soup)
        return content
    except Exception as e:
        return e
