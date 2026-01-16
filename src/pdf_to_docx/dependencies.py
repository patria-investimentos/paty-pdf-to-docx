from fastapi import UploadFile
from src.constants import PDF_MIME_TYPE
import src.pdf_to_docx.exceptions as exceptions


async def pdf_dependency(pdf: UploadFile) -> dict[str, bytes | str]:
    if not pdf:
        raise exceptions.PdfNotProvided()
    
    if not pdf.filename:
        raise exceptions.PdfWithoutName()
    
    if not pdf.content_type:
        raise exceptions.PdfNoneMimeType()
    
    if pdf.content_type != PDF_MIME_TYPE:
        raise exceptions.InvalidPdfMimeType(content_type=pdf.content_type)

    pdf_bytes = await pdf.read()
    if not pdf_bytes:
        raise exceptions.PdfEmpty()
    
    return {
        "data": pdf_bytes,
        "filename": pdf.filename,
        "content_type": pdf.content_type
    }

