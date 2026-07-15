from pypdf import PdfReader
import whisper


def load_pdf(file_path):
    """
    Extract text from a PDF document.
    """

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def load_audio(file_path):
    """
    Convert audio to text using OpenAI Whisper.
    """

    model = whisper.load_model("base")

    result = model.transcribe(file_path)

    return result["text"]


# -------------------------------------------------
# Future Loaders (Placeholders)
# -------------------------------------------------

def load_word(file_path):
    """
    Extract text from Word document.
    """
    raise NotImplementedError("Word loader not implemented yet.")


def load_excel(file_path):
    """
    Extract text from Excel file.
    """
    raise NotImplementedError("Excel loader not implemented yet.")


def load_csv(file_path):
    """
    Extract text from CSV file.
    """
    raise NotImplementedError("CSV loader not implemented yet.")


def load_powerpoint(file_path):
    """
    Extract text from PowerPoint.
    """
    raise NotImplementedError("PowerPoint loader not implemented yet.")


def load_text(file_path):
    """
    Extract text from TXT file.
    """
    raise NotImplementedError("Text loader not implemented yet.")


def load_markdown(file_path):
    """
    Extract text from Markdown file.
    """
    raise NotImplementedError("Markdown loader not implemented yet.")


def load_image(file_path):
    """
    OCR image to text.
    """
    raise NotImplementedError("Image OCR not implemented yet.")


def load_video(file_path):
    """
    Extract speech/text from video.
    """
    raise NotImplementedError("Video loader not implemented yet.")