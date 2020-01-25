import csv

from flask import Flask, redirect, render_template, request

CSV_FILENAME = 'survey.csv'

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    data = request.form.to_dict()

    with open(CSV_FILENAME, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data.values())

    return redirect("/form")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    data = []

    with open(CSV_FILENAME, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            data.append(row)

    return render_template("sheet.html", data=data)
