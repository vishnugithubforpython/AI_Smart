from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from pathlib import Path
import shutil
import uuid

from auth.dependencies import get_current_user

from ingest import ingest_document
from rag.loader import load_pdf

from db.document_crud import save_document

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

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


# -------------------------------------------------
# Processor Functions
# -------------------------------------------------

def process_pdf(path, document_id):

    print(f"Processing PDF : {path}")

    text = load_pdf(str(path))

    print("=" * 50)
    print(f"Text Length : {len(text)}")
    print("=" * 50)

    ingest_document(
        document_id=document_id,
        text=text,
        source=str(path)
    )


def process_word(path):
    print(f"Processing Word : {path}")


def process_excel(path):
    print(f"Processing Excel : {path}")


def process_csv(path):
    print(f"Processing CSV : {path}")


def process_powerpoint(path):
    print(f"Processing PowerPoint : {path}")


def process_text(path):
    print(f"Processing Text : {path}")


def process_markdown(path):
    print(f"Processing Markdown : {path}")


def process_image(path):
    print(f"Processing Image : {path}")


def process_audio(path):
    print(f"Processing Audio : {path}")


def process_video(path):
    print(f"Processing Video : {path}")


# -------------------------------------------------
# Upload Endpoint
# -------------------------------------------------

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):

    filename = file.filename
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {extension}"
        )

    file_type = SUPPORTED_EXTENSIONS[extension]

    # --------------------------------------------
    # Create User Folder
    # --------------------------------------------

    user_folder = UPLOAD_DIR / f"user_{current_user.id}"
    user_folder.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------
    # Unique Filename
    # --------------------------------------------

    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    save_path = user_folder / unique_filename

    # --------------------------------------------
    # Save File
    # --------------------------------------------

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # --------------------------------------------
    # Save Document in Database
    # --------------------------------------------

    document_id = save_document(
        user_id=current_user.id,
        filename=filename,
        file_path=str(save_path),
        file_type=file_type
    )

    print("=" * 60)
    print(f"User ID          : {current_user.id}")
    print(f"Username         : {current_user.username}")
    print(f"Original File    : {filename}")
    print(f"Stored File      : {unique_filename}")
    print(f"Document ID      : {document_id}")
    print("=" * 60)

    # --------------------------------------------
    # Process File
    # --------------------------------------------

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
        "user_id": current_user.id,
        "username": current_user.username,
        "document_id": document_id,
        "original_filename": filename,
        "stored_filename": unique_filename,
        "file_type": file_type,
        "saved_to": str(save_path),
        "message": f"{file_type.capitalize()} uploaded and processed successfully."
    }