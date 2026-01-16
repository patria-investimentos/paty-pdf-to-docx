from src.exceptions import MyHttpException, UnsupportedMediaType, BadRequest


class PdfNotProvided(BadRequest):
    def __init__(self):
        super().__init__(detail="Arquivo PDF não fornecido")


class PdfWithoutName(BadRequest):
    def __init__(self):
        super().__init__(detail="Arquivo PDF sem nome")


class PdfNoneMimeType(UnsupportedMediaType):
    def __init__(self):
        super().__init__(detail="Tipo de mídia do PDF não identificado")


class InvalidPdfMimeType(UnsupportedMediaType):
    def __init__(self, content_type: str):
        super().__init__(detail=f"Tipo de mídia inválido: {content_type}. Esperado: application/pdf")


class PdfEmpty(BadRequest):
    def __init__(self):
        super().__init__(detail="Arquivo PDF vazio")


class ConversionError(BadRequest):
    def __init__(self, message: str = "Erro ao converter PDF para DOCX"):
        super().__init__(detail=message)

