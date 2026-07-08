MAX_CHARS_PER_ARTICLE = 3000


def build_context(documents):

    if not documents:
        return ""

    context_parts = []

    for i, doc in enumerate(documents, start=1):

        title = doc.get("title", "Unknown Title")
        url = doc.get("url", "")
        text = doc.get("text", "")

        # Skip empty documents
        if not text.strip():
            continue

        # Limit article size
        text = text[:MAX_CHARS_PER_ARTICLE]

        context_parts.append(
            f"""
========================================
Source {i}

Title:
{title}

URL:
{url}

Content:
{text}
"""
        )

    return "\n".join(context_parts)