from db.database import get_connection

def save_document(user_id, filename, file_path, file_type):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO documents
        (user_id, filename, file_path, file_type)
        VALUES (%s,%s,%s,%s)
        RETURNING id;
        """,
        (user_id, filename, file_path, file_type)
    )

    document_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return document_id