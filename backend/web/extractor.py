import trafilatura


def extract_text(html):

    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=True,
        include_links=False
    )

    if text is None:
        return ""

    return text