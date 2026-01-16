# PDF to DOCX Converter

API REST para conversão de arquivos PDF para DOCX (Microsoft Word).

## ⚠️ Aviso de Licença (AGPL-3.0)

Este projeto utiliza a biblioteca **PyMuPDF** que é licenciada sob **AGPL-3.0** (GNU Affero General Public License v3.0).

### O que isso significa?

| Cenário | Precisa abrir o código? |
|---------|------------------------|
| Modificar ou redistribuir **este serviço** | ✅ **Sim** - o código modificado deve ser público |
| Sua aplicação faz **requisições HTTP** para este serviço | ❌ **Não** - consumir a API não exige código aberto |
| Incorporar PyMuPDF **diretamente** na sua aplicação | ✅ **Sim** - sua aplicação seria derivada |

### Importante

**Aplicações que apenas consomem esta API via HTTP não são afetadas pela licença AGPL.**

Fazer chamadas HTTP para este serviço **não é considerado** criação de trabalho derivado. Sua aplicação cliente é um sistema separado que apenas envia e recebe dados - ela pode usar qualquer licença, inclusive proprietária/fechada.

A obrigação de manter o código aberto se aplica **apenas a este microsserviço** (que contém o PyMuPDF), não aos sistemas que o consomem.

Para mais informações sobre a licença AGPL-3.0, consulte: https://www.gnu.org/licenses/agpl-3.0.html

---

## Funcionalidades

- ✅ Conversão de PDF para DOCX
- ✅ Preservação do tamanho da página original
- ✅ Detecção automática de margens
- ✅ API REST com documentação Swagger
- ✅ Health check endpoint

## Tecnologias

- **FastAPI** - Framework web
- **pdf2docx** - Biblioteca de conversão
- **PyMuPDF (fitz)** - Leitura e análise de PDFs
- **python-docx** - Manipulação de documentos Word

## Instalação

### Com uv (recomendado)

```bash
# Criar ambiente virtual
uv venv .venv

# Ativar ambiente virtual
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instalar dependências
uv pip install -r requirements.txt
```

### Com pip

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

## Execução

### Local

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Docker

```bash
docker compose up --build
```

## Uso da API

### Documentação Swagger

Acesse http://localhost:8000/docs para a documentação interativa.

### Endpoint de Conversão

```
POST /pdf-to-docx
Content-Type: multipart/form-data
```

**Parâmetros:**
- `pdf` (file): Arquivo PDF a ser convertido

**Resposta:**
- Arquivo DOCX convertido

### Exemplo com cURL

```bash
curl -X POST "http://localhost:8000/pdf-to-docx" \
  -H "accept: application/vnd.openxmlformats-officedocument.wordprocessingml.document" \
  -H "Content-Type: multipart/form-data" \
  -F "pdf=@documento.pdf" \
  --output documento.docx
```

### Exemplo com Python

```python
import requests

with open("documento.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/pdf-to-docx",
        files={"pdf": ("documento.pdf", f, "application/pdf")}
    )

with open("documento.docx", "wb") as f:
    f.write(response.content)
```

### Health Check

```bash
curl http://localhost:8000/health
# {"status": "healthy"}
```

## Estrutura do Projeto

```
src/
├── __init__.py
├── config.py           # Configurações da aplicação
├── constants.py        # Constantes (MIME types)
├── exceptions.py       # Exceções base
├── main.py             # Aplicação FastAPI
├── utils.py            # Utilitários
└── pdf_to_docx/
    ├── __init__.py
    ├── dependencies.py # Validação de upload
    ├── examples.py     # Exemplos para docs
    ├── exceptions.py   # Exceções específicas
    ├── router.py       # Endpoints da API
    └── service.py      # Lógica de conversão
```

## Licença

Este projeto está licenciado sob **AGPL-3.0** devido à dependência do PyMuPDF.

Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
