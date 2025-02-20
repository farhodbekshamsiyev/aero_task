import json


def pretty_print(data):
    """Print dictionary in a nicely formatted JSON-like structure."""
    try:
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except (TypeError, ValueError) as e:
        print(f"Error while printing data: {e}")
