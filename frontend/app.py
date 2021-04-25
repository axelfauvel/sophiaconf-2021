from flask import Flask, render_template
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# APP_STATIC = os.path.join(APP_ROOT, "static")
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
    data = [
        {"time": 0, "device": "green", "value": 1.336},
        {"time": 1, "device": "green", "value": 6.522},
        {"time": 2, "device": "green", "value": 12.867},
        {"time": 3, "device": "green", "value": 17.821},
        {"time": 4, "device": "green", "value": 20.634},
        {"time": 5, "device": "green", "value": 25.68},
        {"time": 6, "device": "green", "value": 31.003},
        {"time": 7, "device": "green", "value": 39.009},
        {"time": 8, "device": "green", "value": 48.90601},
        {"time": 9, "device": "green", "value": 53.87401},
        {"time": 10, "device": "green", "value": 53.87401},
    ]

    labels = [label["time"] for label in data]
    green_values = [element["value"] for element in data]
    return render_template(
        "line-chart.js.j2", labels=labels, green_values=green_values
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
