from flask import Flask, render_template
import os
from data import get_device_data

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_TPL = os.path.join(APP_ROOT, "templates")

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("charts.html")


@app.route("/bar-chart.js")
def bar_chart_js():

    return render_template("bar-chart.js")


@app.route("/line-chart.js")
def line_chart_js():
    data = get_device_data("green")
    labels = [label["time"] for label in data]
    green_values = [element["value"] for element in data]
    return render_template(
        "line-chart.js.j2", labels=labels, green_values=green_values
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
