"""syncro tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
import inspect

# TODO: Import your custom stream types here:
from tap_syncro import streams


class Tapsyncro(Tap):
    """syncro tap class."""

    name = "tap-syncro"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "subdomain",
            th.StringType
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.syncroStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
           cls(self) for name, cls in inspect.getmembers(streams,inspect.isclass) if cls.__module__ == 'tap_syncro.streams'
        ]

if __name__ == "__main__":
    Tapsyncro.cli()
