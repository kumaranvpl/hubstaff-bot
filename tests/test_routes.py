import io
import json

import pandas as pd
import requests
from flask_mail import Mail

from utils_for_tests import (
    mock_requests_resp_with_200,
    mock_return_none,
    get_yesterday_start_time,
    get_mock_users,
    get_mock_projects,
)


def test_populate_data_successul(client, monkeypatch):
    start_time = get_yesterday_start_time()
    # Monkeypatch/mock the request to hubstaff api
    monkeypatch.setattr(requests, "get", mock_requests_resp_with_200)
    resp = client.get("/")
    assert resp.status_code == 200

    resp_data = str(resp.data)
    assert "html" in resp_data
    assert start_time.isoformat() in resp_data

    users = get_mock_users()
    for user in users:
        assert user["name"] in resp_data

    projects = get_mock_projects()
    for project in projects:
        assert project["name"] in resp_data


def test_populate_data_again_to_retrieve_from_cache(client, monkeypatch):
    # Calling the route again with same date will fetch from cache instead of api
    start_time = get_yesterday_start_time()
    monkeypatch.setattr(requests, "get", mock_requests_resp_with_200)
    # Sending date as url query parameter
    resp = client.get(f"/?start_time={start_time.isoformat()}")
    assert resp.status_code == 200

    resp_data = str(resp.data)
    assert "html" in resp_data
    assert start_time.isoformat() in resp_data

    users = get_mock_users()
    for user in users:
        assert user["name"] in resp_data

    projects = get_mock_projects()
    for project in projects:
        assert project["name"] in resp_data


def test_download_json(client, monkeypatch):
    start_time = get_yesterday_start_time()
    monkeypatch.setattr(requests, "get", mock_requests_resp_with_200)
    resp = client.get(f"/download/json?start_time={start_time.isoformat()}")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json"

    resp_data = json.loads(resp.data)

    users = get_mock_users()
    for user in users:
        assert user["name"] in resp_data[0]

    resp_projects = [row[0] for row in resp_data]
    projects = get_mock_projects()
    for project in projects:
        assert project["name"] in resp_projects


def test_download_csv(client, monkeypatch):
    start_time = get_yesterday_start_time()
    monkeypatch.setattr(requests, "get", mock_requests_resp_with_200)
    resp = client.get(f"/download/csv?start_time={start_time.isoformat()}")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "text/csv"

    df = pd.read_csv(io.StringIO(resp.data.decode("utf8")))

    users = get_mock_users()
    df_columns = list(df.columns.values)
    for user in users:
        assert user["name"] in df_columns

    projects = get_mock_projects()
    df_projects = df["Projects/Users"].values
    for project in projects:
        assert project["name"] in df_projects


def test_download_route_with_unknows_extension(client, monkeypatch):
    start_time = get_yesterday_start_time()
    monkeypatch.setattr(requests, "get", mock_requests_resp_with_200)
    resp = client.get(f"/download/mp4?start_time={start_time.isoformat()}")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/json"

    resp_data = json.loads(resp.data)
    assert "msg" in resp_data
    assert resp_data["msg"] == "unknown extension"


def test_send_mail_successful(client, monkeypatch):
    start_time = get_yesterday_start_time()
    monkeypatch.setattr(requests, "get", mock_requests_resp_with_200)
    monkeypatch.setattr(Mail, "send", mock_return_none)
    resp = client.get(f"/send?start_time={start_time.isoformat()}")
    assert resp.status_code == 200

    resp_data = str(resp.data)
    assert "html" in resp_data
    assert start_time.isoformat() in resp_data

    users = get_mock_users()
    for user in users:
        assert user["name"] in resp_data

    projects = get_mock_projects()
    for project in projects:
        assert project["name"] in resp_data


def test_redirection_by_calling_non_existing_route(client, monkeypatch):
    start_time = get_yesterday_start_time()
    monkeypatch.setattr(requests, "get", mock_requests_resp_with_200)
    # Below route does not exists
    resp = client.get("/something", follow_redirects=True)
    assert resp.status_code == 200

    resp_data = str(resp.data)
    assert "html" in resp_data
    assert start_time.isoformat() in resp_data

    users = get_mock_users()
    for user in users:
        assert user["name"] in resp_data

    projects = get_mock_projects()
    for project in projects:
        assert project["name"] in resp_data


def test_favicon_route(client):
    resp = client.get("/favicon.ico")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "image/png"
