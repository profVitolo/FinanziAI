from collections.abc import Iterable


def join_lines(lines: Iterable[str]) -> str:
    return "\n".join(line for line in lines if line)

def format_money(value: float, currency: str) -> str:
    return f"{value:.2f} {currency}"

def format_percent(value: float) -> str:
    return f"{value:.2f}%"

def format_optional_number(value: float | None, decimals: int = 2,) -> str:
    if value is None:
        return "N/A"
    return f"{value:.{decimals}f}"

def format_date(value) -> str:
    return value.isoformat() if hasattr(value, "isoformat") else str(value)