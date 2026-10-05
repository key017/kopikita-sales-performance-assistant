import random
from datetime import datetime, date, timedelta
import pandas as pd


# ============================================================
# 1. DATA MASTER PRODUK
# ============================================================

products = [
    {
        "name": "Kopi Susu Gula Aren",
        "category": "Coffee",
        "price": 18000,
        "popularity": 25
    },
    {
        "name": "Americano",
        "category": "Coffee",
        "price": 16000,
        "popularity": 15
    },
    {
        "name": "Café Latte",
        "category": "Coffee",
        "price": 20000,
        "popularity": 12
    },
    {
        "name": "Cappuccino",
        "category": "Coffee",
        "price": 20000,
        "popularity": 8
    },
    {
        "name": "Caramel Macchiato",
        "category": "Coffee",
        "price": 22000,
        "popularity": 7
    },
    {
        "name": "Mocha",
        "category": "Coffee",
        "price": 22000,
        "popularity": 6
    },
    {
        "name": "Espresso",
        "category": "Coffee",
        "price": 14000,
        "popularity": 3
    },
    {
        "name": "Matcha Latte",
        "category": "Non-Coffee",
        "price": 22000,
        "popularity": 8
    },
    {
        "name": "Chocolate",
        "category": "Non-Coffee",
        "price": 20000,
        "popularity": 5
    },
    {
        "name": "Taro Latte",
        "category": "Non-Coffee",
        "price": 20000,
        "popularity": 3
    },
    {
        "name": "Lemon Tea",
        "category": "Tea",
        "price": 16000,
        "popularity": 4
    },
    {
        "name": "Lychee Tea",
        "category": "Tea",
        "price": 18000,
        "popularity": 4
    },
    {
        "name": "French Fries",
        "category": "Food",
        "price": 18000,
        "popularity": 4
    },
    {
        "name": "Croissant",
        "category": "Food",
        "price": 20000,
        "popularity": 3
    },
    {
        "name": "Banana Cake",
        "category": "Food",
        "price": 18000,
        "popularity": 3
    },
]


# ============================================================
# 2. DATA MASTER OUTLET
# ============================================================

outlets = [
    "KopiKita Solo",
    "KopiKita Manahan",
    "KopiKita Klewer",
    "KopiKita UNS",
]


# ============================================================
# 3. METODE PEMBAYARAN
# ============================================================

payment_methods = [
    "QRIS",
    "Cash",
    "Debit Card",
    "E-Wallet",
]


# ============================================================
# 4. FUNGSI MEMBUAT SATU TRANSAKSI
# ============================================================

def generate_transaction(transaction_number):

    # Pilih produk berdasarkan tingkat popularitas
    product = random.choices(
        products,
        weights=[product["popularity"] for product in products],
        k=1
    )[0]

    # Pilih outlet secara acak
    outlet = random.choice(outlets)

    # Jumlah produk yang dibeli
    quantity = random.choices(
        [1, 2, 3, 4],
        weights=[60, 25, 10, 5]
    )[0]

    # Harga satuan
    unit_price = product["price"]

    # Diskon secara acak
    discount = random.choices(
        [0, 1000, 2000, 3000, 5000],
        weights=[60, 15, 10, 10, 5]
    )[0]

    # Hitung total sebelum diskon
    subtotal = quantity * unit_price

    # Hitung total setelah diskon
    total_sales = subtotal - discount

    # Metode pembayaran
    payment_method = random.choice(payment_methods)

    # Tanggal transaksi
    start_date = datetime(2026, 1, 1)
    random_days = random.randint(0, 272)
    transaction_date = start_date + timedelta(days=random_days)

    day_of_week = transaction_date.strftime("%A")

    if transaction_date.weekday() >= 5:
        day_type = "Weekend"
    else:
        day_type = "Weekday"

    # Jam transaksi berdasarkan pola keramaian
    hour = random.choices(
        [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
        weights=[
            3, 4, 5, 6, 7,
            8, 8, 7, 6, 6,
            9, 11, 13, 12, 8
        ],
        k=1
    )[0]

    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    transaction_time = (
        f"{hour:02d}:{minute:02d}:{second:02d}"
    )

    # Membuat satu data transaksi
    transaction = {
        "transaction_id": f"TRX{transaction_number:05d}",
        "date": transaction_date.strftime("%Y-%m-%d"),
        "day_of_week": day_of_week,
        "day_type": day_type,
        "time": transaction_time,
        "outlet": outlet,
        "product": product["name"],
        "category": product["category"],
        "quantity": quantity,
        "unit_price": unit_price,
        "discount": discount,
        "payment_method": payment_method,
        "total_sales": total_sales,
}

    return transaction


# ============================================================
# 5. MEMBUAT 10.000 TRANSAKSI
# ============================================================

transactions = []

for i in range(1, 10001):
    transaction = generate_transaction(i)
    transactions.append(transaction)


# ============================================================
# 6. MENGUBAH DATA MENJADI DATAFRAME
# ============================================================

df = pd.DataFrame(transactions)


# ============================================================
# 7. MENYIMPAN DATA KE CSV
# ============================================================

output_path = "data/sales_data.csv"

df.to_csv(
    output_path,
    index=False
)


# ============================================================
# 8. INFORMASI HASIL GENERASI DATA
# ============================================================

print("Data transaksi berhasil dibuat!")
print(f"Jumlah transaksi : {len(df)}")
print(f"File             : {output_path}")
print()
print("5 transaksi pertama:")
print(df.head())

print()
print("Jumlah penjualan per produk:")
print(df["product"].value_counts())

print()
print("Jumlah transaksi per jam:")

hour_counts = (
    pd.to_datetime(df["time"], format="%H:%M:%S")
    .dt.hour
    .value_counts()
    .sort_index()
)

print(hour_counts)