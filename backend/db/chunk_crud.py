from db.database import get_connection


def save_chunks(document_id, chunks):
    """
    Save all chunks of a document into PostgreSQL.
    """

    conn = get_connection()
    cur = conn.cursor()

    for index, chunk in enumerate(chunks):

        cur.execute(
            """
            INSERT INTO document_chunks
            (document_id, chunk_index, chunk_text)
            VALUES (%s, %s, %s)
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


def get_chunks_by_user(user_id):
    """
    Load all chunks belonging to a specific user.

    Returns:
        [
            {
                "text": "...",
                "source": "filename.pdf"
            }
        ]
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            dc.chunk_text,
            d.filename
        FROM document_chunks dc
        JOIN documents d
            ON dc.document_id = d.id
        WHERE d.user_id = %s
        ORDER BY
            dc.document_id,
            dc.chunk_index
        """,
        (user_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    metadata = []

    for chunk_text, filename in rows:

        metadata.append(
            {
                "text": chunk_text,
                "source": filename
            }
        )

    return metadata