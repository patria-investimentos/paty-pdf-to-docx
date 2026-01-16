from pdf2docx import Converter
from fastapi.concurrency import run_in_threadpool
from io import BytesIO
import tempfile
import os
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Pt
from src.pdf_to_docx.exceptions import ConversionError


def _get_pdf_page_info(pdf_bytes: bytes) -> dict:
    """Extrai informações da página do PDF (tamanho e margens estimadas)."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    page = doc[0]
    
    # Page size in points (1 pt = 1/72 inch)
    rect = page.rect
    width = rect.width
    height = rect.height
    
    # Try to detect the content area to estimate margins
    text_dict = page.get_text("dict")
    blocks = text_dict.get("blocks", [])
    
    if blocks:
        # Find the content boundaries
        min_x = min(b["bbox"][0] for b in blocks if "bbox" in b)
        min_y = min(b["bbox"][1] for b in blocks if "bbox" in b)
        max_x = max(b["bbox"][2] for b in blocks if "bbox" in b)
        max_y = max(b["bbox"][3] for b in blocks if "bbox" in b)
        
        left_margin = max(min_x, 36)  # Minimum of 0.5 inch
        top_margin = max(min_y, 36)
        right_margin = max(width - max_x, 36)
        bottom_margin = max(height - max_y, 36)
    else:
        # Default margins if not detected
        left_margin = 72  # 1 polegada
        top_margin = 72
        right_margin = 72
        bottom_margin = 72
    
    doc.close()
    
    return {
        "width": width,
        "height": height,
        "left_margin": left_margin,
        "top_margin": top_margin,
        "right_margin": right_margin,
        "bottom_margin": bottom_margin,
    }


def _apply_page_settings(docx_path: str, page_info: dict) -> None:
    """Apply the PDF page settings to the DOCX."""
    doc = Document(docx_path)
    
    for section in doc.sections:
        # Apply page size
        section.page_width = Pt(page_info["width"])
        section.page_height = Pt(page_info["height"])
        
        # Apply margins
        section.left_margin = Pt(page_info["left_margin"])
        section.right_margin = Pt(page_info["right_margin"])
        section.top_margin = Pt(page_info["top_margin"])
        section.bottom_margin = Pt(page_info["bottom_margin"])
    
    doc.save(docx_path)


def _convert_pdf_to_docx_sync(pdf_bytes: bytes) -> BytesIO:
    """Synchronous conversion of PDF to DOCX using temporary files."""
    docx_buffer = BytesIO()
    
    # Extract page information from the PDF
    page_info = _get_pdf_page_info(pdf_bytes)
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_temp:
        pdf_temp.write(pdf_bytes)
        pdf_temp_path = pdf_temp.name
    
    docx_temp_path = pdf_temp_path.replace(".pdf", ".docx")
    
    try:
        cv = Converter(pdf_temp_path)
        cv.convert(docx_temp_path)
        cv.close()
        
        # Apply the PDF page settings to the DOCX
        _apply_page_settings(docx_temp_path, page_info)
        
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
