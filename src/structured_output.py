import json


def create_structured_response(
    question,
    finding,
    analysis,
    recommendation,
    priority
):
    """
    Membuat format output terstruktur
    yang nantinya akan digunakan oleh AI.
    """

    response = {
        "question": question,
        "finding": finding,
        "analysis": analysis,
        "recommendation": recommendation,
        "priority": priority
    }

    return response


def validate_response(response):
    """
    Memastikan output AI memiliki struktur
    yang sesuai.
    """

    required_fields = [
        "question",
        "finding",
        "analysis",
        "recommendation",
        "priority"
    ]

    # Memeriksa field
    for field in required_fields:

        if field not in response:

            return False, (
                f"Field '{field}' tidak ditemukan."
            )

    # Memeriksa priority
    allowed_priority = [
        "LOW",
        "MEDIUM",
        "HIGH"
    ]

    if response["priority"] not in allowed_priority:

        return False, (
            "Priority harus LOW, MEDIUM, atau HIGH."
        )

    return True, "Output valid."


def main():

    question = (
        "Produk apa yang paling penting "
        "untuk diperhatikan?"
    )

    response = create_structured_response(

        question=question,

        finding=(
            "Kopi Susu Gula Aren merupakan "
            "produk dengan sales tertinggi."
        ),

        analysis=(
            "Produk tersebut menghasilkan "
            "Rp 65.181.000 dan menyumbang "
            "22,46% dari total sales."
        ),

        recommendation=(
            "Pastikan ketersediaan Kopi Susu "
            "Gula Aren terutama pada peak hour "
            "untuk mengurangi risiko kehilangan "
            "penjualan."
        ),

        priority="HIGH"
    )

    print("=" * 60)
    print("STRUCTURED AI RESPONSE")
    print("=" * 60)

    print(
        json.dumps(
            response,
            indent=4,
            ensure_ascii=False
        )
    )

    print("\n" + "=" * 60)
    print("VALIDATION")
    print("=" * 60)

    valid, message = validate_response(response)

    print(f"Valid : {valid}")
    print(f"Message : {message}")


if __name__ == "__main__":
    main()