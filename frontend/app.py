from flask import Flask, render_template
import os
from data import get_device_data
from copy import deepcopy

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_TPL = os.path.join(APP_ROOT, "templates")
CHARTS = [
    {"color": "green", "code": "51, 255, 51", "data": []},
    {"color": "blue", "code": "92, 173, 255", "data": []},
    {"color": "red", "code": "204, 0, 0", "data": []},
    {"color": "yellow", "code": "255, 255, 51", "data": []},
    {"color": "black", "code": "0, 0, 0", "data": []},
    {"color": "orange", "code": "249, 128, 0", "data": []},
]

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("charts.html")


@app.route("/bar-chart.js")
def bar_chart_js():

    return render_template("bar-chart.js")


@app.route("/line-chart.js")
def line_chart_js():
    charts = deepcopy(CHARTS)
    for idx, chart in enumerate(charts):
        result = get_device_data(chart["color"])
        if result:
            labels = [element["time"] for element in result]
            chart["data"] = [element["value"] for element in result]
        else:
            charts.pop(idx)

    return render_template("line-chart.js.j2", labels=labels, charts=charts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
