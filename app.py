import pandas as pd
import streamlit as st

st.set_page_config(page_title="RetailPulse", layout="wide")
st.title("RetailPulse: Retail Analytics Dashboard")


@st.cache_data
def load(name, **kw):
    return pd.read_csv(f"data/{name}", **kw)


sales = load("sales_monthly.csv", parse_dates=["month"])
weekly = load("weekly_history.csv", parse_dates=["date"])
fc = load("forecast_weekly.csv", parse_dates=["ds"])
bt = load("backtest_summary.csv")
seg = load("customer_segments.csv")
inv = load("inventory_overstock.csv")

tab1, tab2, tab3, tab4 = st.tabs(["Sales", "Forecast", "Inventory", "Customers"])

# ---------------- Sales ----------------
with tab1:
    c1, c2 = st.columns(2)
    cats = c1.multiselect("Category", sorted(sales["category"].unique()))
    chans = c2.multiselect("Channel", sorted(sales["channel"].unique()))
    s = sales
    if cats:
        s = s[s["category"].isin(cats)]
    if chans:
        s = s[s["channel"].isin(chans)]

    k1, k2, k3 = st.columns(3)
    k1.metric("Total sales", f"{s['sales'].sum():,.0f}")
    k2.metric("Total profit", f"{s['profit'].sum():,.0f}")
    k3.metric("Units sold", f"{s['units'].sum():,.0f}")

    st.subheader("Monthly sales and profit")
    st.line_chart(s.groupby("month")[["sales", "profit"]].sum())
    a, b = st.columns(2)
    a.subheader("Sales by category")
    a.bar_chart(s.groupby("category")["sales"].sum().sort_values(ascending=False))
    b.subheader("Sales by city")
    b.bar_chart(s.groupby("store_city")["sales"].sum().sort_values(ascending=False))

# ---------------- Forecast ----------------
with tab2:
    pid = st.selectbox("Product", sorted(fc["product_id"].unique()))
    hist = weekly[weekly["product_id"] == pid].set_index("date")["total_quantity"].tail(26)
    f = fc[fc["product_id"] == pid].set_index("ds")
    chart = pd.concat(
        [hist.rename("actual"), f["yhat"].rename("forecast"),
         f["yhat_lower"].rename("lower"), f["yhat_upper"].rename("upper")],
        axis=1,
    )
    st.subheader("Weekly demand: last 26 weeks + next 4 weeks")
    st.line_chart(chart)
    st.subheader("Backtest error (WAPE %, lower is better)")
    st.dataframe(bt[bt["product_id"] == pid].sort_values("WAPE%"), hide_index=True)

# ---------------- Inventory ----------------
with tab3:
    below = (inv["stock_on_hand"] < inv["reorder_point"]).sum()
    k1, k2, k3 = st.columns(3)
    k1.metric("Total stock value", f"{inv['stock_value'].sum():,.0f}")
    k2.metric("Excess stock value", f"{inv['excess_value'].sum():,.0f}")
    k3.metric("Rows below reorder point", f"{below:,}")
    st.subheader("Excess stock value by category")
    st.bar_chart(inv.groupby("category")["excess_value"].sum().sort_values(ascending=False))
    st.subheader("Items with no sales in the last 52 weeks")
    st.dataframe(inv[inv["avg_weekly_units"] == 0].head(200), hide_index=True)

# ---------------- Customers ----------------
with tab4:
    k1, k2 = st.columns(2)
    k1.metric("Customers segmented", f"{len(seg):,}")
    k2.metric("Segments", seg["segment"].nunique())
    profile = seg.groupby("segment").agg(
        customers=("customer_id", "size"),
        recency=("recency", "mean"),
        frequency=("frequency", "mean"),
        monetary=("monetary", "mean"),
    ).round(1)
    st.subheader("Segment profile")
    st.dataframe(profile)
    a, b = st.columns(2)
    a.subheader("Customers per segment")
    a.bar_chart(profile["customers"])
    b.subheader("Segment vs loyalty tier")
    b.bar_chart(pd.crosstab(seg["segment"], seg["loyalty_segment"]))
