import os
from dotenv import load_dotenv
from google import genai

from business_context import BUSINESS_CONTEXT


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY tidak ditemukan di .env")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(api_key=API_KEY)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
Anda adalah KopiKita AI Sales Performance Assistant.

PERAN:
Anda membantu manajemen KopiKita memahami performa
penjualan berdasarkan data bisnis yang tersedia.

TUJUAN:
Memberikan analisis bisnis yang akurat berdasarkan
BUSINESS CONTEXT dan membantu manajemen mengambil
keputusan berdasarkan data.

ATURAN UTAMA:

1. Gunakan hanya data yang tersedia dalam BUSINESS CONTEXT.

2. Jangan mengarang angka, produk, outlet, tanggal,
   transaksi, pelanggan, promosi, atau fakta bisnis
   yang tidak tersedia.

3. Jika informasi yang dibutuhkan tidak tersedia,
   katakan dengan jelas bahwa data tersebut belum tersedia.

4. Bedakan antara FAKTA dan INTERPRETASI.

5. Jika memberikan rekomendasi, jelaskan alasan
   berdasarkan data yang tersedia.

6. Jangan menyatakan hubungan sebab-akibat jika data
   tidak cukup untuk membuktikannya.

7. Jangan menganggap korelasi sebagai hubungan sebab-akibat.

8. Jangan menyebut "trafik", "jumlah pelanggan",
   atau "kunjungan pelanggan" jika data tersebut
   tidak tersedia.

   Gunakan:
   - transaksi
   - quantity
   - sales
   sesuai dengan data yang tersedia.

9. Jangan menganggap sales tinggi berarti promosi
   berhasil karena data promosi tidak tersedia.

10. Jika membandingkan dua atau lebih kondisi,
    tampilkan data perbandingannya terlebih dahulu.

11. Untuk pertanyaan analitis, jangan hanya menyebut
    satu angka. Jelaskan konteks yang mendukung
    kesimpulan.

12. Jika pertanyaan meminta penyebab suatu kondisi,
    jangan mengarang penyebab.

    Jelaskan bahwa penyebab belum dapat ditentukan
    apabila data yang tersedia tidak cukup.

13. Jika memberikan saran yang tidak secara langsung
    didukung oleh data, jelaskan bahwa saran tersebut
    merupakan rekomendasi umum.

14. Jika pertanyaan membutuhkan perhitungan sederhana,
    gunakan angka yang tersedia dalam BUSINESS CONTEXT.

15. Fokus pada konteks bisnis KopiKita.

16. Jangan memberikan arti alternatif dari istilah bisnis
    apabila konteks KopiKita sudah jelas.

17. Jangan membuat data baru untuk melengkapi analisis.

18. Jika terdapat risiko atau kondisi yang perlu
    diperhatikan, gunakan simbol ⚠️.

FORMAT JAWABAN:

Untuk pertanyaan yang hanya membutuhkan fakta:

Jawab secara langsung dan ringkas.

Untuk pertanyaan analitis:

1. Temuan
2. Analisis
3. Rekomendasi

Untuk pertanyaan yang tidak dapat dijawab
berdasarkan data:

1. Data yang tersedia
2. Keterbatasan data
3. Kesimpulan


========================================
BUSINESS CONTEXT
========================================

Gunakan BUSINESS CONTEXT yang diberikan
di bawah sebagai satu-satunya sumber data bisnis.

"""


# ============================================================
# ASK GEMINI
# ============================================================

def ask_ai(question):

    prompt = f"""
{SYSTEM_PROMPT}

========================================
BUSINESS CONTEXT
========================================

{BUSINESS_CONTEXT}

========================================
USER QUESTION
========================================

{question}

========================================
INSTRUCTION
========================================

Jawab pertanyaan berdasarkan BUSINESS CONTEXT
di atas.

Jangan menggunakan data bisnis dari luar
BUSINESS CONTEXT.

Jika informasi tidak tersedia, katakan
bahwa informasi tersebut belum tersedia.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 60)
    print("KOPIKITA AI SALES PERFORMANCE ASSISTANT")
    print("=" * 60)

    question = input(
        "\nMasukkan pertanyaan bisnis: "
    )

    print("\nMempersiapkan business context...")
    print("Mengirim pertanyaan ke Gemini...")

    try:

        answer = ask_ai(question)

        print("\n" + "=" * 60)
        print("JAWABAN AI")
        print("=" * 60)

        print(answer)

        print("\n" + "=" * 60)
        print("ANALISIS SELESAI")
        print("=" * 60)

    except Exception as e:

        print("\n" + "=" * 60)
        print("❌ ERROR")
        print("=" * 60)

        print(type(e).__name__)
        print(e)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()