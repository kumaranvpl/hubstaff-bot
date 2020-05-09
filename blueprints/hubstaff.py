from datetime import datetime, time, timedelta

import pandas as pd
import requests
from flask import Blueprint
from flask import current_app as app
from flask import jsonify, make_response, render_template, request
from flask_mail import Mail, Message


hubstaff_blueprint = Blueprint("hubstaff_blueprint", __name__)


def get_user_time_spent_in_project(user_ids, project_ids, activities):
    time_data = {}
    for user_id in user_ids:
        time_data[user_id] = {}
        for project_id in project_ids:
            time_data[user_id][project_id] = 0

    for activity in activities:
        time_data[activity["user_id"]][activity["project_id"]] += activity["tracked"]

    return time_data


def get_data_from_hubstaff(start_time=None, stop_time=None):
    if not start_time:
        # Using .now() instead of .utcnow()
        start_of_day = datetime.combine(datetime.now(), time.min)
        start_time = start_of_day - timedelta(days=1)

    # This is to get day's starting time of user supplemented datetime
    start_time = datetime.combine(start_time, time.min)

    if not stop_time:
        stop_time = start_time + timedelta(days=1)

    headers = {
        "App-Token": "GZQk6jIePM5JkFcz0j-3ZguSb2qm8Z4RQXamFV9NjQI",
        "Auth-Token": "-BI-txT5DJ3xOclZkajXi6DqvXpSZCWF2CQnmT40WAM",
    }
    base_url = app.config["HUBSTAFF_API"]

    resp = requests.get(f"{base_url}/users", headers=headers)
    resp_json = resp.json()
    table_header = ["Projects/Users"]
    users = {user["id"]: user for user in resp_json["users"]}
    for _, user in users.items():
        table_header.append(user["name"])

    resp = requests.get(f"{base_url}/projects", headers=headers)
    resp_json = resp.json()
    projects = {project["id"]: project for project in resp_json["projects"]}

    params = {"start_time": start_time.isoformat(), "stop_time": stop_time.isoformat()}
    resp = requests.get(f"{base_url}/activities", params=params, headers=headers)
    activities = resp.json()["activities"]

    time_data = get_user_time_spent_in_project(
        user_ids=users.keys(), project_ids=projects.keys(), activities=activities
    )
    table_rows = []

    for project_id, project in projects.items():
        row = [project["name"]]
        for user_id, user in users.items():
            row.append(str(timedelta(seconds=time_data[user_id][project_id])))
        table_rows.append(row)

    return table_header, table_rows, start_time.isoformat(), stop_time.isoformat()


@hubstaff_blueprint.route("/", methods=["GET"])
def populate_table():
    start_time = (
        datetime.strptime(request.args.get("start_time"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("start_time")
        else None
    )
    stop_time = (
        datetime.strptime(request.args.get("stop_time"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("stop_time")
        else None
    )
    table_header, table_rows, start, stop = get_data_from_hubstaff(
        start_time, stop_time
    )

    return render_template(
        "index.html",
        table_header=table_header,
        table_rows=table_rows,
        start=start,
        stop=stop,
        actions=True,
        start_time=start,
        stop_time=stop,
    )


@hubstaff_blueprint.route("/download/<file_type>", methods=["GET"])
def download_data(file_type):
    start_time = (
        datetime.strptime(request.args.get("start_time"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("start_time")
        else None
    )
    stop_time = (
        datetime.strptime(request.args.get("stop_time"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("stop_time")
        else None
    )
    table_header, table_rows, start, stop = get_data_from_hubstaff(
        start_time, stop_time
    )

    if file_type == "json":
        data = [table_header]
        data.extend(table_rows)
        resp = jsonify(data)
        resp.headers[
            "Content-Disposition"
        ] = f"attachment;filename=data-from-{start}-to-{stop}.json"
        return resp
    elif file_type == "csv":
        df = pd.DataFrame(table_rows, columns=table_header)
        resp = make_response(df.to_csv(index=False))
        resp.headers[
            "Content-Disposition"
        ] = f"attachment; filename=data-from-{start}-to-{stop}.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp

    return jsonify({"msg": "unknown extension"})


@hubstaff_blueprint.route("/send", methods=["GET"])
def send_mail():
    start_time = (
        datetime.strptime(request.args.get("start_time"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("start_time")
        else None
    )
    stop_time = (
        datetime.strptime(request.args.get("stop_time"), "%Y-%m-%dT%H:%M:%S")
        if request.args.get("stop_time")
        else None
    )
    table_header, table_rows, start, stop = get_data_from_hubstaff(
        start_time, stop_time
    )

    mail = Mail()
    mail.init_app(app)

    msg = Message(
        f"Hubstaff Bot Data from {start} to {stop}",
        sender="kumaranvpl@gmail.com",
        recipients=app.config["MAIL_RECIPIENTS"],
    )
    # Not adding msg.body
    msg.html = render_template(
        "index.html",
        table_header=table_header,
        table_rows=table_rows,
        start=start,
        stop=stop,
        actions=False,
        start_time=start,
        stop_time=stop,
    )
    mail.send(msg)

    # Hacky solution. Ideally should use ajax or frontend frameworks to call this.
    return render_template(
        "index.html",
        table_header=table_header,
        table_rows=table_rows,
        start=start,
        stop=stop,
        actions=True,
        start_time=start,
        stop_time=stop,
    )
