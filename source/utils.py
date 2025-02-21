import json
from datetime import datetime


def pretty_print(data):
    """Print dictionary in a nicely formatted JSON-like structure."""
    try:
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except (TypeError, ValueError) as e:
        print(f"Error while printing data: {e}")


def get_default_date_format(date):
    date_obj = datetime.strptime(date, "%d.%m.%Y")
    return date_obj
