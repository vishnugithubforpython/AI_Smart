from router import process_query

chat_history = []

while True:

    query = input("\nYou: ")

    if query.lower() == "exit":
        print("Goodbye!")
        break

    answer, results = process_query(
        query,
        chat_history
    )

    print("\nAssistant:")
    print(answer)

    chat_history.append({
        "user": query,
        "assistant": answer,
        "sources": results
    })