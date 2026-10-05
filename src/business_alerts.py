import pandas as pd


DATA_PATH = "data/sales_data.csv"


def load_data():
    """Membaca data transaksi."""

    df = pd.read_csv(DATA_PATH)

    df["date"] = pd.to_datetime(df["date"])

    return df


def detect_lowest_sales_month(df):
    """Mendeteksi bulan dengan sales terendah."""

    monthly_sales = (
        df.groupby(df["date"].dt.month)["total_sales"]
        .sum()
        .sort_values()
    )

    lowest_month = monthly_sales.index[0]
    lowest_sales = monthly_sales.iloc[0]

    average_monthly_sales = monthly_sales.mean()

    difference_percent = (
        (average_monthly_sales - lowest_sales)
        / average_monthly_sales
        * 100
    )

    return (
        lowest_month,
        lowest_sales,
        average_monthly_sales,
        difference_percent,
    )


def detect_product_concentration(df):
    """Mendeteksi produk dengan kontribusi sales tinggi."""

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

    return (
        top_product,
        top_product_sales,
        contribution,
    )


def detect_peak_period(df):
    """Mendeteksi periode jam dengan sales tertinggi."""

    df["hour"] = pd.to_datetime(
        df["time"].astype(str),
        format="%H:%M:%S"
    ).dt.hour

    hourly_sales = (
        df.groupby("hour")["total_sales"]
        .sum()
        .sort_values(ascending=False)
    )

    peak_hours = hourly_sales.head(3)

    return peak_hours


def main():

    print("=" * 60)
    print("BUSINESS ALERT & RECOMMENDATION ENGINE")
    print("=" * 60)

    df = load_data()

    # ========================================================
    # ALERT 1 - LOWEST SALES MONTH
    # ========================================================

    (
        lowest_month,
        lowest_sales,
        average_monthly_sales,
        difference_percent,
    ) = detect_lowest_sales_month(df)

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
        12: "December",
    }

    print("\n⚠️ ALERT 1 - LOWEST SALES MONTH")

    print(
        f"{month_names[lowest_month]} merupakan bulan "
        f"dengan sales terendah."
    )

    print(
        f"Sales: Rp {lowest_sales:,.0f}"
    )

    print(
        f"Rata-rata sales bulanan: "
        f"Rp {average_monthly_sales:,.0f}"
    )

    print(
        f"Sales bulan tersebut sekitar "
        f"{difference_percent:.2f}% di bawah "
        f"rata-rata bulanan."
    )

    print("\nRECOMMENDATION")

    print(
        "Lakukan investigasi terhadap faktor yang "
        "mempengaruhi penurunan sales, terutama "
        "produk, outlet, dan jam transaksi."
    )

    # ========================================================
    # ALERT 2 - PRODUCT CONCENTRATION
    # ========================================================

    (
        top_product,
        top_product_sales,
        contribution,
    ) = detect_product_concentration(df)

    print("\n⚠️ ALERT 2 - PRODUCT CONCENTRATION")

    print(
        f"{top_product} menyumbang "
        f"{contribution:.2f}% dari total sales."
    )

    if contribution >= 20:

        print(
            "Kontribusi produk tergolong tinggi."
        )

        print("\nRECOMMENDATION")

        print(
            "Pastikan ketersediaan produk tersebut "
            "terutama pada periode peak hour."
        )

    # ========================================================
    # ALERT 3 - PEAK PERIOD
    # ========================================================

    peak_hours = detect_peak_period(df)

    print("\n💡 ALERT 3 - PEAK PERIOD")

    print(
        "Tiga jam dengan sales tertinggi:"
    )

    for hour, sales in peak_hours.items():

        print(
            f"{hour:02d}:00 - "
            f"Rp {sales:,.0f}"
        )

    print("\nRECOMMENDATION")

    print(
        "Pastikan kapasitas operasional, "
        "ketersediaan produk, dan kesiapan "
        "staff mencukupi selama periode peak."
    )


if __name__ == "__main__":
    main()