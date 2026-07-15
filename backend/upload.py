from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from ingest import ingest_document
from rag.loader import load_pdf

from db.document_crud import save_document

router = APIRouter(prefix="/upload", tags=["Upload"])

# Folder to store uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".pdf": "pdf",
    ".docx": "word",
    ".doc": "word",
    ".xlsx": "excel",
    ".xls": "excel",
    ".csv": "csv",
    ".pptx": "powerpoint",
    ".ppt": "powerpoint",
    ".txt": "text",
    ".md": "markdown",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
    ".mp3": "audio",
    ".wav": "audio",
    ".mp4": "video",
    ".avi": "video",
    ".mov": "video",
}


# -----------------------------
# Processor Functions
# -----------------------------

def process_pdf(path, document_id):
    print(f"Processing PDF: {path}")

    # Extract text from PDF
    text = load_pdf(str(path))

    print("=" * 50)
    print(f"Text Length: {len(text)}")
    print("=" * 50)

    # Index into vector store
    ingest_document(
        document_id=document_id,
        text=text,
        source=str(path)
    )


def process_word(path):
    print(f"Processing Word: {path}")
    # TODO:
    # text = load_docx(path)
    # ingest_document(text, str(path))


def process_excel(path):
    print(f"Processing Excel: {path}")
    # TODO:
    # text = load_excel(path)
    # ingest_document(text, str(path))


def process_csv(path):
    print(f"Processing CSV: {path}")
    # TODO


def process_powerpoint(path):
    print(f"Processing PowerPoint: {path}")
    # TODO


def process_text(path):
    print(f"Processing Text: {path}")
    # TODO


def process_markdown(path):
    print(f"Processing Markdown: {path}")
    # TODO


def process_image(path):
    print(f"Processing Image: {path}")
    # TODO:
    # OCR
    # ingest_document(text, str(path))


def process_audio(path):
    print(f"Processing Audio: {path}")
    # TODO:
    # Speech To Text
    # ingest_document(text, str(path))


def process_video(path):
    print(f"Processing Video: {path}")
    # TODO:
    # Extract Audio
    # Speech To Text
    # ingest_document(text, str(path))


# -----------------------------
# Upload Endpoint
# -----------------------------

@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    filename = file.filename
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    file_type = SUPPORTED_EXTENSIONS[extension]

    save_path = UPLOAD_DIR / filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    document_id = save_document(
    user_id=1,
    filename=filename,
    file_path=str(save_path),
    file_type=file_type)
    
    print(f"Document saved with ID: {document_id}")


    # Route file to processor
    if file_type == "pdf":
        process_pdf(save_path, document_id)

    elif file_type == "word":
        process_word(save_path)

    elif file_type == "excel":
        process_excel(save_path)

    elif file_type == "csv":
        process_csv(save_path)

    elif file_type == "powerpoint":
        process_powerpoint(save_path)

    elif file_type == "text":
        process_text(save_path)

    elif file_type == "markdown":
        process_markdown(save_path)

    elif file_type == "image":
        process_image(save_path)

    elif file_type == "audio":
        process_audio(save_path)

    elif file_type == "video":
        process_video(save_path)

    return {
        "status": "success",
        "filename": filename,
        "file_type": file_type,
        "saved_to": str(save_path),
        "message": f"{file_type.capitalize()} uploaded and processed successfully."
    }