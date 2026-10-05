import pandas as pd


DATA_PATH = "data/sales_data.csv"


def load_data():
    """Membaca data transaksi."""

    df = pd.read_csv(DATA_PATH)

    df["date"] = pd.to_datetime(df["date"])

    return df


def get_basic_metrics(df):
    """Menghitung metrik dasar."""

    total_sales = df["total_sales"].sum()
    total_transactions = len(df)
    total_quantity = df["quantity"].sum()

    aov = total_sales / total_transactions

    return {
        "total_sales": total_sales,
        "total_transactions": total_transactions,
        "total_quantity": total_quantity,
        "aov": aov,
    }


def get_top_product(df):
    """Mencari produk dengan sales tertinggi."""

    product_sales = (
        df.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_sales.index[0]
    top_sales = product_sales.iloc[0]

    return top_product, top_sales


def get_top_outlet(df):
    """Mencari outlet dengan sales tertinggi."""

    outlet_sales = (
        df.groupby("outlet")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_outlet = outlet_sales.index[0]
    top_sales = outlet_sales.iloc[0]

    return top_outlet, top_sales


def get_peak_hour(df):
    """Mencari jam dengan sales tertinggi."""

    df["hour"] = pd.to_datetime(
        df["time"].astype(str),
        format="%H:%M:%S"
    ).dt.hour

    hourly_sales = (
        df.groupby("hour")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    peak_hour = hourly_sales.index[0]
    peak_sales = hourly_sales.iloc[0]

    return peak_hour, peak_sales


def get_top_product_contribution(df):
    """Menghitung kontribusi produk terlaris."""

    total_sales = df["total_sales"].sum()

    product_sales = (
        df.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    top_product = product_sales.index[0]
    top_product_sales = product_sales.iloc[0]

    contribution = (
        top_product_sales / total_sales * 100
    )

    return top_product, contribution


def main():

    print("=" * 60)
    print("BUSINESS INSIGHTS")
    print("=" * 60)

    # Membaca data
    df = load_data()

    # KPI dasar
    metrics = get_basic_metrics(df)

    # Analisis
    top_product, top_product_sales = get_top_product(df)

    top_outlet, top_outlet_sales = get_top_outlet(df)

    peak_hour, peak_hour_sales = get_peak_hour(df)

    product_name, product_contribution = (
        get_top_product_contribution(df)
    )

    # --------------------------------------------------------
    # INSIGHT 1
    # --------------------------------------------------------

    print("\nINSIGHT 1 - TOP PRODUCT")

    print(
        f"{product_name} merupakan produk "
        f"dengan sales tertinggi sebesar "
        f"Rp {top_product_sales:,.0f}."
    )

    print(
        f"Produk tersebut menyumbang "
        f"{product_contribution:.2f}% "
        f"dari total sales."
    )

    # --------------------------------------------------------
    # INSIGHT 2
    # --------------------------------------------------------

    print("\nINSIGHT 2 - TOP OUTLET")

    print(
        f"{top_outlet} merupakan outlet "
        f"dengan sales tertinggi sebesar "
        f"Rp {top_outlet_sales:,.0f}."
    )

    # --------------------------------------------------------
    # INSIGHT 3
    # --------------------------------------------------------

    print("\nINSIGHT 3 - PEAK HOUR")

    print(
        f"Jam {peak_hour:02d}:00 merupakan "
        f"peak hour dengan sales sebesar "
        f"Rp {peak_hour_sales:,.0f}."
    )

    # --------------------------------------------------------
    # INSIGHT 4
    # --------------------------------------------------------

    print("\nINSIGHT 4 - OVERALL PERFORMANCE")

    print(
        f"Total sales sebesar "
        f"Rp {metrics['total_sales']:,.0f} "
        f"dari {metrics['total_transactions']:,} transaksi."
    )

    print(
        f"Average Order Value (AOV) sebesar "
        f"Rp {metrics['aov']:,.0f}."
    )


if __name__ == "__main__":
    main()