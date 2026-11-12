from urllib.parse import urlsplit, urlunsplit

from hotglue_smoke_test.vcr.tap import VCRTapTestRunner


class Runner(VCRTapTestRunner):
    FILTER_HEADERS = [
        *VCRTapTestRunner.FILTER_HEADERS,
        "cookie",
        "cf-ray",
        "etag",
        "x-request-id",
        "x-s-info",
    ]
    PRESERVE_KEYS = {
        "page",  # Current page is incremented for the next request.
        "total_pages",  # Stops pagination after the last recorded page.
    }

    def module(self) -> str:
        return "tap_syncro.tap"

    def launch(self):
        from tap_syncro.tap import Tapsyncro

        Tapsyncro.cli()

    def scrub_uri(self, uri: str) -> str:
        parts = urlsplit(uri)
        return urlunsplit(parts._replace(netloc="example.syncromsp.com"))


if __name__ == "__main__":
    Runner.main()
