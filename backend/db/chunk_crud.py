from db.database import get_connection


def save_chunks(document_id, chunks):

    conn = get_connection()
    cur = conn.cursor()

    for index, chunk in enumerate(chunks):

        cur.execute(
            """
            INSERT INTO document_chunks
            (document_id, chunk_index, chunk_text)
            VALUES (%s,%s,%s)
            """,
            (
                document_id,
                index,
                chunk
            )
        )

    conn.commit()

    cur.close()
    conn.close()