"""Safe field locations and error codes from Pydantic validation failures."""

from pydantic import ValidationError


def validation_fields(error: ValidationError) -> str:
    return "; ".join(
        f"{'.'.join(str(part) for part in item['loc']) or 'root'} ({item['type']})"
        for item in error.errors(
            include_input=False, include_context=False, include_url=False
        )
    )
