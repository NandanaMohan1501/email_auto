from app.llm import get_llm


def test_llm():
    llm = get_llm()

    response = llm.invoke(
        "Reply with exactly this JSON and nothing else:\n"
        '{"category":"General Inquiry","priority":"Low","summary":"Test successful"}'
    )

    print("===== LLM RESPONSE =====")
    print(response.content)


if __name__ == "__main__":
    test_llm()