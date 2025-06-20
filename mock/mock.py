from flask import Request
from werkzeug.test import EnvironBuilder


def create_mock_request(method="GET", path="/", query_string=None, data=None, json=None, headers=None):
    builder = EnvironBuilder(
        method=method,
        path=path,
        query_string=query_string,
        data=data,
        json=json,
        headers=headers
    )
    env = builder.get_environ()
    builder.close()

    return Request(env)

mock_request = create_mock_request(
    method="POST",
    path="/example",
    json={
        "tickets": ["B5P211.SA", ],
        "start": '2025-06-01',
        "end": '2025-06-19',
    },
    headers={"Content-Type": "application/json"}
)
