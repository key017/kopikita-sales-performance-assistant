import os
import pandas as pd


# ============================================================
# PATH DATA
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "sales_data.csv")


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"File data tidak ditemukan: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    return df


# ============================================================
# FORMAT
# ============================================================

def format_rupiah(value):
    return f"Rp {value:,.0f}"


def format_percent(value):
    return f"{value:.2f}%"


# ============================================================
# GENERATE BUSINESS CONTEXT
# ============================================================

def generate_business_context():

    df = load_data()

    # ========================================================
    # GENERAL KPI
    # ========================================================

    total_sales = df["total_sales"].sum()
    total_transactions = len(df)
    total_quantity = df["quantity"].sum()

    aov = total_sales / total_transactions
    asp = total_sales / total_quantity

    # ========================================================
    # TOP PRODUCTS
    # ========================================================

    product_sales = (
        df.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_5_products = product_sales.head(5)

    top_product = top_5_products.index[0]
    top_product_sales = top_5_products.iloc[0]

    top_product_contribution = (
        top_product_sales / total_sales * 100
    )

    # ========================================================
    # PRODUCT CONTRIBUTION
    # ========================================================

    product_contribution = (
        product_sales / total_sales * 100
    )

    # ========================================================
    # TOP OUTLET
    # ========================================================

    outlet_sales = (
        df.groupby("outlet")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_outlet = outlet_sales.index[0]
    top_outlet_sales = outlet_sales.iloc[0]

    # ========================================================
    # OUTLET PERFORMANCE
    # ========================================================

    outlet_performance = (
        df.groupby("outlet")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
        .sort_values("total_sales", ascending=False)
    )

    # ========================================================
    # CATEGORY PERFORMANCE
    # ========================================================

    category_performance = (
        df.groupby("category")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
        .sort_values("total_sales", ascending=False)
    )

    # ========================================================
    # TIME
    # ========================================================

    df["hour"] = pd.to_datetime(
        df["time"],
        format="%H:%M:%S",
        errors="coerce"
    ).dt.hour

    hourly_sales = (
        df.groupby("hour")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    peak_hour = hourly_sales.index[0]
    peak_hour_sales = hourly_sales.iloc[0]

    peak_3_hours = hourly_sales.head(3)

    # ========================================================
    # DAY PERFORMANCE
    # ========================================================

    day_performance = (
        df.groupby("day_of_week")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
    )

    # Urutan hari
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    day_performance = day_performance.reindex(day_order)

    # ========================================================
    # WEEKDAY VS WEEKEND
    # ========================================================

    day_type_performance = (
        df.groupby("day_type")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
    )

    day_type_performance["aov"] = (
        day_type_performance["total_sales"]
        / day_type_performance["transactions"]
    )

    # ========================================================
    # MONTHLY PERFORMANCE
    # ========================================================

    df["date_parsed"] = pd.to_datetime(
        df["date"],
        format="%Y-%m-%d",
        errors="coerce"
    )

    df["month"] = df["date_parsed"].dt.month

    monthly_sales = (
        df.groupby("month")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
    )

    month_names = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    monthly_sales["month_name"] = monthly_sales.index.map(
        month_names
    )

    monthly_average = monthly_sales["total_sales"].mean()

    lowest_month_number = monthly_sales["total_sales"].idxmin()

    lowest_month_sales = monthly_sales.loc[
        lowest_month_number,
        "total_sales"
    ]

    lowest_month_name = month_names[lowest_month_number]

    below_average = (
        (monthly_average - lowest_month_sales)
        / monthly_average
        * 100
    )

    # ========================================================
    # BUILD PRODUCT SECTION
    # ========================================================

    product_section = ""

    for product, sales in top_5_products.items():

        contribution = sales / total_sales * 100

        product_section += (
            f"- {product}: "
            f"{format_rupiah(sales)} "
            f"({format_percent(contribution)})\n"
        )

    # ========================================================
    # BUILD OUTLET SECTION
    # ========================================================

    outlet_section = ""

    for outlet, row in outlet_performance.iterrows():

        contribution = row["total_sales"] / total_sales * 100

        outlet_section += (
            f"- {outlet}: "
            f"{format_rupiah(row['total_sales'])} "
            f"({format_percent(contribution)}), "
            f"{int(row['transactions']):,} transaksi\n"
        )

    # ========================================================
    # BUILD CATEGORY SECTION
    # ========================================================

    category_section = ""

    for category, row in category_performance.iterrows():

        category_section += (
            f"- {category}: "
            f"{format_rupiah(row['total_sales'])}, "
            f"{int(row['transactions']):,} transaksi\n"
        )

    # ========================================================
    # BUILD PEAK HOURS
    # ========================================================

    peak_section = ""

    for hour, sales in peak_3_hours.items():

        peak_section += (
            f"- {hour:02d}:00: "
            f"{format_rupiah(sales)}\n"
        )

    # ========================================================
    # BUILD DAY PERFORMANCE
    # ========================================================

    day_section = ""

    for day, row in day_performance.iterrows():

        day_section += (
            f"- {day}: "
            f"{format_rupiah(row['total_sales'])}, "
            f"{int(row['transactions']):,} transaksi\n"
        )

    # ========================================================
    # BUILD WEEKDAY / WEEKEND
    # ========================================================

    day_type_section = ""

    for day_type, row in day_type_performance.iterrows():

        day_type_section += (
            f"- {day_type}: "
            f"{format_rupiah(row['total_sales'])}, "
            f"AOV {format_rupiah(row['aov'])}\n"
        )

    # ========================================================
    # BUILD MONTHLY PERFORMANCE
    # ========================================================

    monthly_section = ""

    for month, row in monthly_sales.iterrows():

        monthly_section += (
            f"- {row['month_name']}: "
            f"{format_rupiah(row['total_sales'])}, "
            f"{int(row['transactions']):,} transaksi\n"
        )

    # ========================================================
    # BUSINESS ALERTS
    # ========================================================

    alerts = []

    # Alert 1
    if below_average > 5:

        alerts.append(
            f"⚠️ {lowest_month_name} berada "
            f"{below_average:.2f}% di bawah rata-rata "
            f"sales bulanan."
        )

    # Alert 2
    if top_product_contribution >= 20:

        alerts.append(
            f"⚠️ {top_product} menyumbang "
            f"{top_product_contribution:.2f}% "
            f"dari total sales."
        )

    # Alert 3
    alerts.append(
        f"💡 Peak period berada pada "
        f"{peak_3_hours.index.min():02d}:00-"
        f"{peak_3_hours.index.max():02d}:00 "
        f"berdasarkan 3 jam dengan sales tertinggi."
    )

    alert_section = "\n".join(
        f"- {alert}"
        for alert in alerts
    )

    # ========================================================
    # FINAL BUSINESS CONTEXT
    # ========================================================

    business_context = f"""

GENERAL KPI

Total Sales       : {format_rupiah(total_sales)}
Transactions      : {total_transactions:,}
Total Quantity    : {total_quantity:,}
AOV               : {format_rupiah(aov)}
ASP               : {format_rupiah(asp)}


TOP 5 PRODUCTS

{product_section}


TOP OUTLET

Outlet            : {top_outlet}
Sales             : {format_rupiah(top_outlet_sales)}


OUTLET PERFORMANCE

{outlet_section}


CATEGORY PERFORMANCE

{category_section}


PEAK 3 HOURS

{peak_section}


PERFORMANCE PER DAY

{day_section}


WEEKDAY VS WEEKEND

{day_type_section}


MONTHLY PERFORMANCE

{monthly_section}


LOWEST SALES MONTH

Month             : {lowest_month_name}
Sales             : {format_rupiah(lowest_month_sales)}
Monthly Average   : {format_rupiah(monthly_average)}
Below Average     : {format_percent(below_average)}


BUSINESS ALERTS

{alert_section}
"""

    return business_context


# ============================================================
# BUSINESS CONTEXT
# ============================================================

BUSINESS_CONTEXT = generate_business_context()


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("BUSINESS CONTEXT FOR AI")
    print("=" * 60)

    print(BUSINESS_CONTEXT)


if __name__ == "__main__":
    main()