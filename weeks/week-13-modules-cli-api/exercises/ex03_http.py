"""Exercise 03: inspect an offline HTTP fixture."""

from bot_course.http_foundation import parse_json_response

fixture = b'{"lesson": 13}'


def main() -> None:
    """Check a successful fixture and observe a non-success status."""
    response = parse_json_response(200, fixture)
    assert response["lesson"] == 13
    print(f"Successful response: {response}")

    try:
        parse_json_response(500, b'{"error": "server error"}')
    except ValueError as error:
        print(f"Expected HTTP error: {error}")
    else:
        raise AssertionError("HTTP status 500 should raise ValueError")


if __name__ == "__main__":
    main()
