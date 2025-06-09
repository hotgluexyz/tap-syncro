"""REST client handling, including syncroStream base class."""

from __future__ import annotations
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Any, Callable, Iterable
from typing import Optional, Any, Generator, Dict, Callable
import backoff
import logging
from backoff.types import Details
from http import HTTPStatus
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError

import requests
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class syncroStream(RESTStream):
    """syncro stream class."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = self.config.get("page_size")

   
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return f'https://{self.config.get("subdomain", "demo")}.syncromsp.com/api/v1'

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.meta.page"  # Or override `get_next_page_token`.
    max_page_token_jsonpath = "$.meta.total_pages"
    ignore_statuses = [401]

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
        #Add this user_agent per request of Syncro
        headers["User-Agent"] = self.config.get("user_agent", "hotglue (support@hotglue.xyz)")
        return headers

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        if row.get("id"):
            row['id'] = str(row['id'])
        
        if row.get('customer') and row.get('customer').get('id'):
            if row['customer'].get('contacts'):
                for i,r in enumerate(row['customer'].get('contacts')):
                    row['customer']['contacts'][i]['id'] = str(row['customer']['contacts'][i]['id'])
            
            row['customer']['id'] = str(row['customer']['id'])
        

        if row.get('contacts') and len(row.get("contacts")) > 0:
            for i,r in enumerate(row.get('contacts')):
                row['contacts'][i]['id'] = str(row['contacts'][i]['id'])


        return row

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

        if self.page_size:
            params["per_page"] = self.page_size
        return params
    

    def backoff_handler(self, details: Details) -> None:
        super().backoff_handler(details)
        # Update page size on retries
        prepared_request = details.get("args")[0]
        if self.page_size:
            parsed_url = urlparse(prepared_request.url)
            current_params = parse_qs(parsed_url.query)
            current_params["per_page"] = self.page_size
            prepared_request.prepare_url(parsed_url.geturl(), params=current_params)

    def backoff_wait_generator(self) -> Generator[float, None, None]:
        """The wait generator used by the backoff decorator on request failure.

        See for options:
        https://github.com/litl/backoff/blob/master/backoff/_wait_gen.py

        And see for examples: `Code Samples <../code_samples.html#custom-backoff>`_

        Returns:
            The wait generator
        """

        """
        Example:
            - 1st retry: 20 seconds
            - 2nd retry: 40 seconds
            - 3rd retry: 80 seconds
            - 4th retry: 160 seconds
            - 5th retry: 320 seconds
            - 5th retry: 640 seconds (capped at 10 minutes)
        """
        return backoff.expo(base=2, factor=20, max_value=640)

    def validate_response(self, response: requests.Response) -> None:
        x_header = None
        if "X-Request-Id" in response.headers:
            x_header = response.headers["X-Request-Id"]
            x_header = f" X-Request_Id: {x_header} "
        if response.status_code in self.ignore_statuses:
            pass
        elif (
            response.status_code in self.extra_retry_statuses
            or HTTPStatus.INTERNAL_SERVER_ERROR
            <= response.status_code
            <= max(HTTPStatus)
        ):      
            self.logger.warn(f"Failed with status code: {response.status_code} {x_header} with response: {response.text} for URl: {response.request.url}")

            if response.status_code == 504 and "gateway time-out" in response.text.lower():
                self.logger.warn(f"Gateway time-out for URL: {response.request.url}")
                if not self.page_size or (self.page_size and self.page_size > 1):
                    self.page_size = self.page_size // 2 if self.page_size else 16
                    self.logger.warn(f"Decreasing page size to {self.page_size}")
                    

            msg = self.response_error_message(response)
            raise RetriableAPIError(msg, response)

        elif (
            HTTPStatus.BAD_REQUEST
            <= response.status_code
            < HTTPStatus.INTERNAL_SERVER_ERROR
        ):
            msg = self.response_error_message(response)
            self.logger.warn(f"Failed with status code: {response.status_code} {x_header} with response: {response.text} for URl: {response.request.url}")
            raise FatalAPIError(msg)

    def backoff_max_tries(self) -> int:
        """The number of attempts before giving up when retrying requests.

        Returns:
            Number of max retries.
        """
        return 7 # 7 means 6 retries after first unsuccessful attempt
