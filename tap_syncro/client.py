"""REST client handling, including syncroStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Iterable
from typing import Optional, Any, Generator, Dict, Callable
import backoff
import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class syncroStream(RESTStream):
    """syncro stream class."""

   
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return f'https://{self.config.get("subdomain", "demo")}.syncromsp.com/api/v1'

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.meta.page"  # Or override `get_next_page_token`.
    max_page_token_jsonpath = "$.meta.total_pages"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="Authorization",
            value=self.config.get("auth_token", ""),
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        # If not using an authenticator, you may also provide inline auth headers:
        # headers["Private-Token"] = self.config.get("auth_token")
        return headers

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Any | None,
    ) -> Any | None:
        """Return a token for identifying next page or None if no more pages.

        Args:
            response: The HTTP ``requests.Response`` object.
            previous_token: The previous page token value.

        Returns:
            The next pagination token.
        """
        # TODO: If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            max_page_match = extract_jsonpath(
                self.max_page_token_jsonpath,response.json()
            )

            first_match = next(iter(all_matches), None)
            max_page_token = next(iter(max_page_match),None)
            if first_match is not None:
                next_page_candidate = int(first_match) + 1
                next_page_token = next_page_candidate if max_page_token >= next_page_candidate else None
            else:
                next_page_token = None

        else:
            next_page_token = response.headers.get("X-Next-Page", None)

        return next_page_token

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def backoff_wait_generator(self) -> Generator[float, None, None]:
        """The wait generator used by the backoff decorator on request failure.

        See for options:
        https://github.com/litl/backoff/blob/master/backoff/_wait_gen.py

        And see for examples: `Code Samples <../code_samples.html#custom-backoff>`_

        Returns:
            The wait generator
        """
        return backoff.constant(interval=60)

   

   
