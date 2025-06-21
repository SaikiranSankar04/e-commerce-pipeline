from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chart-data/category")
def chart_data_category():
    df = pd.read_csv("cleaned_orders.csv")
    grouped = df.groupby("category")["total_price"].sum().sort_values(ascending=False)
    return jsonify(
        {
            "labels": grouped.index.tolist(),
            "values": grouped.values.tolist(),
            "title": "Total Sales by Category",
        }
    )


@app.route("/api/chart-data/day")
def chart_data_day():
    df = pd.read_csv("cleaned_orders.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    grouped = df.groupby(df["order_date"].dt.date)["total_price"].sum()
    return jsonify(
        {
            "labels": [str(date) for date in grouped.index],
            "values": grouped.values.tolist(),
            "title": "Total Orders by Day",
        }
    )


@app.route("/api/chart-data/country")
def chart_data_country():
    df = pd.read_csv("cleaned_orders.csv")
    grouped = (
        df.groupby("country")["total_price"].sum().sort_values(ascending=False).head(10)
    )
    return jsonify(
        {
            "labels": grouped.index.tolist(),
            "values": grouped.values.tolist(),
            "title": "Revenue by Country",
        }
    )


@app.route("/orders")
def cleaned_orders_table():
    df = pd.read_csv("cleaned_orders.csv")
    return render_template(
        "orders_table.html",
        table=df.to_html(classes="table table-striped table-bordered", index=False),
    )


@app.route("/revenue-by-category")
def revenue_by_category():
    df = pd.read_csv("cleaned_orders.csv")
    df["total_price"] = df["price"] * df["quantity"]
    grouped = (
        df.groupby("category")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    return jsonify(grouped.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
