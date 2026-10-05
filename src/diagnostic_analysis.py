import os
import sys
import pandas as pd


# ============================================================
# PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sales_data.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    df = pd.read_csv(DATA_PATH)

    # Pastikan kolom tanggal menjadi datetime
    df["date"] = pd.to_datetime(df["date"])

    return df


# ============================================================
# MONTHLY ANALYSIS
# ============================================================

def analyze_monthly_sales(df):

    monthly = (
        df.groupby(df["date"].dt.month)
        .agg(
            total_sales=("total_sales", "sum"),
            transactions=("transaction_id", "count"),
            total_quantity=("quantity", "sum")
        )
        .reset_index()
    )

    monthly = monthly.rename(
        columns={"date": "month"}
    )

    monthly["month_name"] = monthly["month"].map({
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
    })

    return monthly


# ============================================================
# MONTH COMPARISON
# ============================================================

def compare_months(df, month_a, month_b):

    monthly = analyze_monthly_sales(df)

    data_a = monthly[monthly["date"] == month_a]
    data_b = monthly[monthly["date"] == month_b]

    if data_a.empty or data_b.empty:
        return None

    sales_a = data_a.iloc[0]["total_sales"]
    sales_b = data_b.iloc[0]["total_sales"]

    transaction_a = data_a.iloc[0]["transactions"]
    transaction_b = data_b.iloc[0]["transactions"]

    sales_change = (
        (sales_b - sales_a) / sales_a
    ) * 100

    transaction_change = (
        (transaction_b - transaction_a)
        / transaction_a
    ) * 100

    return {
        "month_a": month_a,
        "month_b": month_b,
        "sales_a": sales_a,
        "sales_b": sales_b,
        "sales_change_percent": sales_change,
        "transactions_a": transaction_a,
        "transactions_b": transaction_b,
        "transaction_change_percent": transaction_change
    }


# ============================================================
# PRODUCT PERFORMANCE BY MONTH
# ============================================================

def analyze_product_month(df, month):

    data = df[
        df["date"].dt.month == month
    ]

    result = (
        data.groupby("product")
        .agg(
            total_sales=("total_sales", "sum"),
            quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
        .reset_index()
    )

    return result


# ============================================================
# OUTLET PERFORMANCE BY MONTH
# ============================================================

def analyze_outlet_month(df, month):

    data = df[
        df["date"].dt.month == month
    ]

    result = (
        data.groupby("outlet")
        .agg(
            total_sales=("total_sales", "sum"),
            quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
        .reset_index()
    )

    return result


# ============================================================
# CATEGORY PERFORMANCE BY MONTH
# ============================================================

def analyze_category_month(df, month):

    data = df[
        df["date"].dt.month == month
    ]

    result = (
        data.groupby("category")
        .agg(
            total_sales=("total_sales", "sum"),
            quantity=("quantity", "sum"),
            transactions=("transaction_id", "count")
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
        .reset_index()
    )

    return result


# ============================================================
# DIAGNOSTIC ANALYSIS
# ============================================================

def diagnose_month(month):

    df = load_data()

    print("=" * 60)
    print("DIAGNOSTIC SALES ANALYSIS")
    print("=" * 60)

    print(f"\nAnalisis bulan: {month}")

    # --------------------------------------------------------
    # Current month
    # --------------------------------------------------------

    monthly = analyze_monthly_sales(df)

    current = monthly[
        monthly["date"] == month
    ]

    if current.empty:
        print("\n❌ Data bulan tidak ditemukan.")
        return

    current = current.iloc[0]

    print("\n" + "=" * 60)
    print("MONTH PERFORMANCE")
    print("=" * 60)

    print(
        f"Sales       : Rp {current['total_sales']:,.0f}"
    )

    print(
        f"Transactions: {current['transactions']:,}"
    )

    print(
        f"Quantity    : {current['total_quantity']:,}"
    )

    # --------------------------------------------------------
    # Previous month
    # --------------------------------------------------------

    previous_month = month - 1

    if previous_month >= 1:

        comparison = compare_months(
            df,
            previous_month,
            month
        )

        if comparison:

            print("\n" + "=" * 60)
            print("COMPARISON WITH PREVIOUS MONTH")
            print("=" * 60)

            print(
                f"Sales bulan sebelumnya : "
                f"Rp {comparison['sales_a']:,.0f}"
            )

            print(
                f"Sales bulan {month}     : "
                f"Rp {comparison['sales_b']:,.0f}"
            )

            print(
                f"Perubahan sales       : "
                f"{comparison['sales_change_percent']:.2f}%"
            )

            print(
                f"Perubahan transaksi   : "
                f"{comparison['transaction_change_percent']:.2f}%"
            )

    # --------------------------------------------------------
    # Product
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PRODUCT PERFORMANCE")
    print("=" * 60)

    products = analyze_product_month(
        df,
        month
    )

    print(
        products.head(10).to_string(index=False)
    )

    # --------------------------------------------------------
    # Outlet
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("OUTLET PERFORMANCE")
    print("=" * 60)

    outlets = analyze_outlet_month(
        df,
        month
    )

    print(
        outlets.to_string(index=False)
    )

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("CATEGORY PERFORMANCE")
    print("=" * 60)

    categories = analyze_category_month(
        df,
        month
    )

    print(
        categories.to_string(index=False)
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        month = int(
            input(
                "\nMasukkan nomor bulan (1-12): "
            )
        )

        if month < 1 or month > 12:
            raise ValueError

        diagnose_month(month)

    except ValueError:

        print(
            "\n❌ Masukkan nomor bulan yang valid "
            "(1-12)."
        )