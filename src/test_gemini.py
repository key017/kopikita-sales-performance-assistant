import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("=" * 60)
print("KOPIKITA AI - GEMINI API TEST")
print("=" * 60)

if not api_key:
    print("❌ GEMINI_API_KEY tidak ditemukan.")
    exit()

print("✅ API key ditemukan")
print("Prefix:", api_key[:8])

try:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Jawab singkat: Apa itu AOV dalam bisnis?"
    )

    print()
    print("✅ Koneksi Gemini berhasil!")
    print()
    print("Jawaban AI:")
    print(response.text)

except Exception as e:
    print()
    print("❌ Request gagal")
    print(type(e).__name__)
    print(e)