import pandas as pd
from pathlib import Path


# ============================================================
# 1. KONFIGURASI
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales_data.csv"


# ============================================================
# 2. MEMBACA DATA
# ============================================================

def load_data():
    """Membaca data penjualan dari file CSV."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    # Konversi tanggal dan waktu
    df["date"] = pd.to_datetime(df["date"])
    df["time"] = pd.to_datetime(
        df["time"],
        format="%H:%M:%S"
    ).dt.time

    return df


# ============================================================
# 3. KPI UTAMA
# ============================================================

def calculate_kpi(df):
    """Menghitung KPI utama penjualan."""

    total_sales = df["total_sales"].sum()
    total_transactions = len(df)
    total_quantity = df["quantity"].sum()

    average_transaction = (
        total_sales / total_transactions
        if total_transactions > 0
        else 0
    )

    average_quantity = (
        total_quantity / total_transactions
        if total_transactions > 0
        else 0
    )

    total_discount = df["discount"].sum()

    return {
        "total_sales": total_sales,
        "total_transactions": total_transactions,
        "total_quantity": total_quantity,
        "average_transaction": average_transaction,
        "average_quantity": average_quantity,
        "total_discount": total_discount,
    }

# ============================================================
# 3A. BUSINESS KPI
# ============================================================

def calculate_business_kpi(df):
    """Menghitung KPI bisnis tambahan."""

    total_sales = df["total_sales"].sum()
    total_quantity = df["quantity"].sum()
    total_transactions = len(df)

    # Average Order Value
    aov = (
        total_sales / total_transactions
        if total_transactions > 0
        else 0
    )

    # Average Selling Price
    asp = (
        total_sales / total_quantity
        if total_quantity > 0
        else 0
    )

    # Sales per transaction
    sales_per_transaction = (
        total_sales / total_transactions
        if total_transactions > 0
        else 0
    )

    return {
        "aov": aov,
        "asp": asp,
        "sales_per_transaction": sales_per_transaction,
    }

def analyze_product_contribution(df):
    """Menghitung kontribusi sales setiap produk."""

    total_sales = df["total_sales"].sum()

    result = (
        df.groupby("product")["total_sales"]
        .sum()
        .reset_index()
    )

    result["sales_contribution"] = (
        result["total_sales"] / total_sales * 100
    )

    result = result.sort_values(
        "total_sales",
        ascending=False
    )

    return result

def analyze_outlet_contribution(df):
    """Menghitung kontribusi sales setiap outlet."""

    total_sales = df["total_sales"].sum()

    result = (
        df.groupby("outlet")["total_sales"]
        .sum()
        .reset_index()
    )

    result["sales_contribution"] = (
        result["total_sales"] / total_sales * 100
    )

    result = result.sort_values(
        "total_sales",
        ascending=False
    )

    return result

def analyze_weekday_weekend_aov(df):
    """Membandingkan AOV weekday dan weekend."""

    result = (
        df.groupby("day_type")
        .agg(
            total_sales=("total_sales", "sum"),
            transactions=("transaction_id", "count"),
        )
    )

    result["aov"] = (
        result["total_sales"] /
        result["transactions"]
    )

    return result

def get_peak_hours(df, n=3):
    """Mengambil jam dengan sales tertinggi."""

    result = (
        df.groupby(
            pd.to_datetime(
                df["time"].astype(str),
                format="%H:%M:%S"
            ).dt.hour
        )["total_sales"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(n)
    )

    return result


# ============================================================
# 4. ANALISIS PRODUK
# ============================================================

def analyze_products(df):
    """Menganalisis performa setiap produk."""

    product_analysis = (
        df.groupby("product")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count"),
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    return product_analysis


# ============================================================
# 5. ANALISIS OUTLET
# ============================================================

def analyze_outlets(df):
    """Menganalisis performa setiap outlet."""

    outlet_analysis = (
        df.groupby("outlet")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count"),
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    return outlet_analysis


# ============================================================
# 6. ANALISIS KATEGORI
# ============================================================

def analyze_categories(df):
    """Menganalisis performa berdasarkan kategori."""

    category_analysis = (
        df.groupby("category")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count"),
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    return category_analysis


# ============================================================
# 7. ANALISIS HARI
# ============================================================

def analyze_days(df):
    """Menganalisis penjualan berdasarkan hari."""

    day_analysis = (
        df.groupby("day_of_week")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count"),
        )
    )

    # Urutan hari yang benar
    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    day_analysis = (
        day_analysis
        .reindex(day_order)
        .dropna()
    )

    return day_analysis


# ============================================================
# 8. ANALISIS WEEKDAY VS WEEKEND
# ============================================================

def analyze_day_type(df):
    """Membandingkan penjualan weekday dan weekend."""

    day_type_analysis = (
        df.groupby("day_type")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count"),
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    return day_type_analysis


# ============================================================
# 9. ANALISIS JAM
# ============================================================

def analyze_hours(df):
    """Menganalisis penjualan berdasarkan jam."""

    # Ambil jam dari kolom time
    df = df.copy()

    df["hour"] = pd.to_datetime(
        df["time"].astype(str),
        format="%H:%M:%S"
    ).dt.hour

    hour_analysis = (
        df.groupby("hour")
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count"),
        )
        .sort_values(
            "total_sales",
            ascending=False
        )
    )

    return hour_analysis


# ============================================================
# 10. ANALISIS BULAN
# ============================================================

def analyze_months(df):
    """Menganalisis penjualan berdasarkan bulan."""

    df = df.copy()

    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%B")

    month_analysis = (
        df.groupby(["month", "month_name"])
        .agg(
            total_sales=("total_sales", "sum"),
            total_quantity=("quantity", "sum"),
            transactions=("transaction_id", "count"),
        )
        .reset_index()
        .sort_values("month")
    )

    return month_analysis


# ============================================================
# 11. PRODUK TERLARIS
# ============================================================

def get_top_products(df, n=5):
    """Mengambil produk dengan penjualan tertinggi."""

    result = (
        df.groupby("product")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

    return result


# ============================================================
# 12. PRODUK BERDASARKAN QUANTITY
# ============================================================

def get_top_products_by_quantity(df, n=5):
    """Mengambil produk berdasarkan jumlah unit terjual."""

    result = (
        df.groupby("product")["quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

    return result


# ============================================================
# 13. PERIODE PENJUALAN TERTINGGI
# ============================================================

def get_best_hour(df):
    """Mencari jam dengan total penjualan tertinggi."""

    result = analyze_hours(df)

    best_hour = result["total_sales"].idxmax()
    best_sales = result.loc[
        best_hour,
        "total_sales"
    ]

    return best_hour, best_sales


# ============================================================
# 14. OUTLET TERBAIK
# ============================================================

def get_best_outlet(df):
    """Mencari outlet dengan penjualan tertinggi."""

    result = analyze_outlets(df)

    best_outlet = result.index[0]
    best_sales = result.iloc[0]["total_sales"]

    return best_outlet, best_sales


# ============================================================
# 15. MENJALANKAN ANALISIS
# ============================================================

def main():

    print("=" * 60)
    print("AI SALES PERFORMANCE ASSISTANT")
    print("=" * 60)

    # Load data
    df = load_data()

    print("\nData berhasil dibaca.")
    print(f"Jumlah transaksi : {len(df):,}")
    print(
        f"Periode          : "
        f"{df['date'].min().strftime('%d-%m-%Y')} "
        f"s/d "
        f"{df['date'].max().strftime('%d-%m-%Y')}"
    )

    # --------------------------------------------------------
    # KPI
    # --------------------------------------------------------

    kpi = calculate_kpi(df)

    print("\n" + "=" * 60)
    print("KPI UTAMA")
    print("=" * 60)

    print(
        f"Total Sales          : Rp {kpi['total_sales']:,.0f}"
    )

    print(
        f"Total Transactions   : {kpi['total_transactions']:,}"
    )

    print(
        f"Total Quantity       : {kpi['total_quantity']:,}"
    )

    print(
        f"Average Transaction  : "
        f"Rp {kpi['average_transaction']:,.0f}"
    )

    print(
        f"Average Quantity     : "
        f"{kpi['average_quantity']:.2f}"
    )

    print(
        f"Total Discount       : "
        f"Rp {kpi['total_discount']:,.0f}"
    )

    # --------------------------------------------------------
    # BUSINESS KPI
    # --------------------------------------------------------

    business_kpi = calculate_business_kpi(df)

    print("\n" + "=" * 60)
    print("BUSINESS KPI")
    print("=" * 60)

    print(
        f"AOV : Rp {business_kpi['aov']:,.0f}"
    )

    print(
        f"ASP : Rp {business_kpi['asp']:,.0f}"
    )


    # --------------------------------------------------------
    # TOP PRODUCTS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP 5 PRODUK BERDASARKAN SALES")
    print("=" * 60)

    print(
        get_top_products(df).to_string()
    )

    # --------------------------------------------------------
    # PRODUCT CONTRIBUTION
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PRODUCT SALES CONTRIBUTION")
    print("=" * 60)

    product_contribution = analyze_product_contribution(df)

    print(
        product_contribution.to_string(
            index=False,
            formatters={
                "total_sales": lambda x: f"Rp {x:,.0f}",
                "sales_contribution": lambda x: f"{x:.2f}%"
            }
        )
    )

    # --------------------------------------------------------
    # OUTLET CONTRIBUTION
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("OUTLET SALES CONTRIBUTION")
    print("=" * 60)

    outlet_contribution = analyze_outlet_contribution(df)

    print(
        outlet_contribution.to_string(
            index=False,
            formatters={
                "total_sales": lambda x: f"Rp {x:,.0f}",
                "sales_contribution": lambda x: f"{x:.2f}%"
            }
        )
    )

    # --------------------------------------------------------
    # WEEKDAY VS WEEKEND AOV
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("WEEKDAY VS WEEKEND AOV")
    print("=" * 60)

    weekday_weekend_aov = analyze_weekday_weekend_aov(df)

    print(
        weekday_weekend_aov.to_string()
    )

    # --------------------------------------------------------
    # PEAK HOURS
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PEAK 3 HOURS")
    print("=" * 60)

    peak_hours = get_peak_hours(df)

    for hour, sales in peak_hours.items():
        print(
            f"{hour:02d}:00 - "
            f"Rp {sales:,.0f}"
        )



    # --------------------------------------------------------
    # TOP PRODUCTS QUANTITY
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP 5 PRODUK BERDASARKAN QUANTITY")
    print("=" * 60)

    print(
        get_top_products_by_quantity(df).to_string()
    )

    # --------------------------------------------------------
    # OUTLET
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PERFORMA OUTLET")
    print("=" * 60)

    print(
        analyze_outlets(df).to_string()
    )

    # --------------------------------------------------------
    # KATEGORI
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PERFORMA KATEGORI")
    print("=" * 60)

    print(
        analyze_categories(df).to_string()
    )

    # --------------------------------------------------------
    # HARI
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PERFORMA PER HARI")
    print("=" * 60)

    print(
        analyze_days(df).to_string()
    )

    # --------------------------------------------------------
    # WEEKDAY VS WEEKEND
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("WEEKDAY VS WEEKEND")
    print("=" * 60)

    print(
        analyze_day_type(df).to_string()
    )

    # --------------------------------------------------------
    # JAM
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("TOP JAM BERDASARKAN SALES")
    print("=" * 60)

    print(
        analyze_hours(df).head(10).to_string()
    )

    # --------------------------------------------------------
    # BULAN
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("PERFORMA BULANAN")
    print("=" * 60)

    print(
        analyze_months(df).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # BEST OUTLET
    # --------------------------------------------------------

    best_outlet, best_outlet_sales = get_best_outlet(df)

    print("\n" + "=" * 60)
    print("INSIGHT UTAMA")
    print("=" * 60)

    print(
        f"Outlet terbaik : {best_outlet}"
    )

    print(
        f"Sales outlet  : Rp {best_outlet_sales:,.0f}"
    )

    # --------------------------------------------------------
    # BEST HOUR
    # --------------------------------------------------------

    best_hour, best_hour_sales = get_best_hour(df)

    print(
        f"Jam terbaik   : {best_hour:02d}:00"
    )

    print(
        f"Sales jam tersebut : "
        f"Rp {best_hour_sales:,.0f}"
    )

    print("\n" + "=" * 60)
    print("ANALISIS SELESAI")
    print("=" * 60)


# ============================================================
# PROGRAM UTAMA
# ============================================================

if __name__ == "__main__":
    main()