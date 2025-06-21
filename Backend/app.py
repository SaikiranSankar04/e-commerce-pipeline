from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)


@app.route("/")
def dashboard():
    df = pd.read_csv("cleaned_orders.csv")

    # Example Plot: Total Sales by Category
    df["total_price"] = df["price"] * df["quantity"]
    cat_sales = df.groupby("category")["total_price"].sum().reset_index()
    fig = px.bar(
        cat_sales, x="category", y="total_price", title="Total Sales by Category"
    )
    fig_html = pio.to_html(fig, full_html=False)

    return render_template(
        "dashboard.html", table=df.to_html(classes="table table-striped"), plot=fig_html
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
