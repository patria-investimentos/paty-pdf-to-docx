from src.pdf_to_docx.exceptions import (
    PdfNotProvided,
    PdfWithoutName,
    PdfNoneMimeType,
    InvalidPdfMimeType,
    PdfEmpty,
    ConversionError
)


def get_response_examples():
    return {
        200: {
            "description": "DOCX generated successfully",
            "content": {
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}
            }
        },
        400: {
            "description": "Validation error",
            "content": {
                "application/json": {
                    "examples": {
                        "pdf_not_provided": PdfNotProvided().get_example(),
                        "pdf_without_name": PdfWithoutName().get_example(),
                        "pdf_empty": PdfEmpty().get_example(),
                        "conversion_error": ConversionError().get_example(),
                    }
                }
            }
        },
        415: {
            "description": "Unsupported media type",
            "content": {
                "application/json": {
                    "examples": {
                        "pdf_none_mime": PdfNoneMimeType().get_example(),
                        "invalid_mime": InvalidPdfMimeType(content_type="text/plain").get_example(),
                    }
                }
            }
        }
    }

