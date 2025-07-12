from flask import Flask, render_template, jsonify, send_file
import pandas as pd
import plotly.express as px
import plotly.io as pio
import io
from fpdf import FPDF

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


@app.route("/export/csv/<source>")
def export_csv(source):
    df = get_dataframe_by_source(source)
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        download_name=f"{source}.csv",
        as_attachment=True,
    )


@app.route("/export/pdf/<source>")
def export_pdf(source):
    df = get_dataframe_by_source(source)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(
        200, 10, txt=f"{source.replace('_', ' ').title()} Report", ln=True, align="C"
    )

    col_width = pdf.w / (len(df.columns) + 1)
    row_height = pdf.font_size * 1.5

    for col in df.columns:
        pdf.cell(col_width, row_height, txt=str(col), border=1)
    pdf.ln(row_height)

    for i in df.values.tolist():
        for item in i:
            pdf.cell(col_width, row_height, txt=str(item), border=1)
        pdf.ln(row_height)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)

    return send_file(
        buf,
        mimetype="application/pdf",
        download_name=f"{source}.pdf",
        as_attachment=True,
    )


def get_dataframe_by_source(source):
    df = pd.read_csv("cleaned_orders.csv")
    if source == "sales_by_category":
        return df.groupby("category")["total_price"].sum().reset_index()
    elif source == "sales_by_country":
        return df.groupby("country")["total_price"].sum().reset_index()
    elif source == "sales_by_date":
        df["order_date"] = pd.to_datetime(df["order_date"])
        return df.groupby(df["order_date"].dt.date)["total_price"].sum().reset_index()
    else:
        return df.head(20)


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
        "order_table.html",
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


@app.route("/data/category")
def data_category():
    df = pd.read_csv("cleaned_orders.csv")
    result = df.groupby("category")["total_price"].sum().reset_index()
    return render_template("table.html", title="Sales by Category", data=result)


@app.route("/data/country")
def data_country():
    df = pd.read_csv("cleaned_orders.csv")
    result = df.groupby("country")["total_price"].sum().reset_index()
    return render_template("table.html", title="Sales by Country", data=result)


@app.route("/data/date")
def data_date():
    df = pd.read_csv("cleaned_orders.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    result = df.groupby(df["order_date"].dt.date)["total_price"].sum().reset_index()
    return render_template("table.html", title="Sales by Date", data=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
