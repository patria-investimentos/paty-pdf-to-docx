from pdf2docx import Converter
from fastapi.concurrency import run_in_threadpool
from io import BytesIO
import tempfile
import os
from src.pdf_to_docx.exceptions import ConversionError


def _convert_pdf_to_docx_sync(pdf_bytes: bytes) -> BytesIO:
    """Synchronous conversion of PDF to DOCX using temporary files."""
    docx_buffer = BytesIO()
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_temp:
        pdf_temp.write(pdf_bytes)
        pdf_temp_path = pdf_temp.name
    
    docx_temp_path = pdf_temp_path.replace(".pdf", ".docx")
    
    try:
        cv = Converter(pdf_temp_path)
        cv.convert(docx_temp_path)
        cv.close()
        
        with open(docx_temp_path, "rb") as docx_file:
            docx_buffer.write(docx_file.read())
        
        docx_buffer.seek(0)
        return docx_buffer
    
    except Exception as e:
        raise ConversionError(f"Erro na conversão: {str(e)}")
    
    finally:
        if os.path.exists(pdf_temp_path):
            os.remove(pdf_temp_path)
        if os.path.exists(docx_temp_path):
            os.remove(docx_temp_path)


async def convert_pdf_to_docx(pdf_bytes: bytes) -> BytesIO:
    """Converte PDF para DOCX de forma assíncrona."""
    return await run_in_threadpool(_convert_pdf_to_docx_sync, pdf_bytes)
