"""Currency utilities for Dominican Republic peso (DOP)."""

from decimal import Decimal, ROUND_HALF_UP


ITBIS_RATE = Decimal("0.18")  # 18 % VAT
DOP_SYMBOL = "RD$"


def apply_itbis(amount: Decimal) -> Decimal:
    """Return *amount* with ITBIS (18 %) added."""
    return (amount * (1 + ITBIS_RATE)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def itbis_amount(amount: Decimal) -> Decimal:
    """Return only the ITBIS portion of *amount* (amount already ex-tax)."""
    return (amount * ITBIS_RATE).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def format_dop(amount: Decimal | float | int) -> str:
    """Format a numeric value as a DOP currency string, e.g. 'RD$ 1,234.56'."""
    value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    # Thousands separator
    integer_part, decimal_part = f"{value:f}".split(".")
    # Build thousands-separated integer
    sign = ""
    if integer_part.startswith("-"):
        sign = "-"
        integer_part = integer_part[1:]
    chunks: list[str] = []
    while len(integer_part) > 3:
        chunks.append(integer_part[-3:])
        integer_part = integer_part[:-3]
    chunks.append(integer_part)
    thousands = ",".join(reversed(chunks))
    return f"{DOP_SYMBOL} {sign}{thousands}.{decimal_part}"
