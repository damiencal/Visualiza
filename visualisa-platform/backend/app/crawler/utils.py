"""
Crawler utilities: price parsing, URL normalization
"""
import re
from urllib.parse import urljoin


def parse_dop_price(text: str) -> float | None:
    """
    Parse Dominican Peso (DOP) price strings.
    Handles formats like: "RD$ 1,200.00", "$ 1.200,00", "1200", "1,200"
    """
    if not text:
        return None
    # Remove currency symbols and whitespace
    cleaned = re.sub(r"[RD$\s]", "", text).strip()
    # Handle period-as-thousands and comma-as-decimal (European format)
    if re.search(r"\d{1,3}(\.\d{3})+(,\d+)?$", cleaned):
        cleaned = cleaned.replace(".", "").replace(",", ".")
    else:
        # Standard format: comma as thousands separator
        cleaned = cleaned.replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def absolute_url(base: str, path: str) -> str:
    """Make a URL absolute given a base URL."""
    if not path:
        return ""
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return urljoin(base, path)
