from pypdf import PdfReader
import whisper


def load_pdf(file_path):
    """
    Reads a PDF file and returns full text
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def load_audio(file_path):
    """
    Converts audio to text using Whisper
    """
    model = whisper.load_model("base")
    result = model.transcribe(file_path)

    return result["text"]