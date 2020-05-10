
from collections import namedtuple
from datetime import datetime, time, timedelta


ResponseMock = namedtuple("response_mock", ["status_code", "ok", "json"])


def get_yesterday_start_time():
    start_of_day = datetime.combine(datetime.now(), time.min)
    start_time = start_of_day - timedelta(days=1)
    return start_time


def get_mock_table_data():
    table_header = ["Projects/Users", "Kumaran Rajendhiran"]
    table_rows = [
        ["Project X", "00:00:59"],
        ["Project Y", "00:59:00"],
        ["Project Z", "59:00:00"],
    ]
    return table_header, table_rows


def get_mock_users():
    return [
        {
            "email": "kumaranvpl@gmail.com",
            "id": 111,
            "last_activity": "2020-05-10T07:20:00Z",
            "name": "Kumaran Rajendhiran",
        },
        {
            "email": "pawel.polewicz@reef.pl",
            "id": 112,
            "last_activity": "2020-05-09T21:42:26Z",
            "name": "Pawel Polewicz",
        },
        {
            "email": "piotr.radaj@reef.pl",
            "id": 113,
            "last_activity": "2020-05-09T13:20:00Z",
            "name": "Piotr Radaj",
        },
    ]


def get_mock_projects():
    return [
        {
            "description": None,
            "id": 201,
            "last_activity": "2020-05-10T07:30:00Z",
            "name": "Project X",
            "status": "Active",
        },
        {
            "description": None,
            "id": 202,
            "last_activity": "2020-05-10T03:57:58Z",
            "name": "Project Y",
            "status": "Active",
        },
        {
            "description": None,
            "id": 203,
            "last_activity": None,
            "name": "Project Z",
            "status": "Active",
        },
    ]


def get_mock_activities():
    return [
        {
            "id": 1313689544,
            "keyboard": 130,
            "mouse": 130,
            "overall": 130,
            "paid": False,
            "project_id": 201,
            "starts_at": "2020-05-09T15:36:58Z",
            "task_id": None,
            "time_slot": "2020-05-09T15:30:00Z",
            "tracked": 182,
            "user_id": 111,
        },
        {
            "id": 1313694524,
            "keyboard": 435,
            "mouse": 435,
            "overall": 435,
            "paid": False,
            "project_id": 201,
            "starts_at": "2020-05-09T15:40:00Z",
            "task_id": None,
            "time_slot": "2020-05-09T15:40:00Z",
            "tracked": 600,
            "user_id": 111,
        },
        {
            "id": 1313699234,
            "keyboard": 435,
            "mouse": 435,
            "overall": 435,
            "paid": False,
            "project_id": 201,
            "starts_at": "2020-05-09T15:50:00Z",
            "task_id": None,
            "time_slot": "2020-05-09T15:50:00Z",
            "tracked": 600,
            "user_id": 111,
        },
    ]


def mock_requests_resp_with_200(*args, **kwargs):
    # Mock responses for hubstaff apis
    if "/v1/users" in args[0]:
        return ResponseMock(200, True, lambda: {"users": get_mock_users()})
    elif "/v1/projects" in args[0]:
        return ResponseMock(200, True, lambda: {"projects": get_mock_projects()})
    elif "/v1/activities" in args[0]:
        return ResponseMock(200, True, lambda: {"activities": get_mock_activities()})


def mock_return_none(*args, **kwargs):
    return None
