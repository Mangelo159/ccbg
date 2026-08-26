import os

_EXTENSIONES_TEXTO_PLANO = ('.txt', '.md', '.csv')


def extraer_texto(nombre, archivo):
    """Extrae el texto de un archivo subido (PDF, DOCX o texto plano).

    Se usa para poblar `Documento.contenido_texto`, que alimenta el contexto
    del chatbot de KMDB. Si el tipo no está soportado o falla la extracción,
    devuelve '' en vez de interrumpir el guardado del documento.
    """
    extension = os.path.splitext(nombre or '')[1].lower()
    archivo.seek(0)
    try:
        if extension == '.pdf':
            texto = _extraer_pdf(archivo)
        elif extension == '.docx':
            texto = _extraer_docx(archivo)
        elif extension in _EXTENSIONES_TEXTO_PLANO:
            texto = _extraer_texto_plano(archivo)
        else:
            texto = ''
    except Exception:
        texto = ''
    finally:
        archivo.seek(0)
    return texto.strip()


def _extraer_pdf(archivo):
    from pypdf import PdfReader
    reader = PdfReader(archivo)
    return '\n'.join(pagina.extract_text() or '' for pagina in reader.pages)


def _extraer_docx(archivo):
    import docx
    documento = docx.Document(archivo)
    return '\n'.join(parrafo.text for parrafo in documento.paragraphs)


def _extraer_texto_plano(archivo):
    contenido = archivo.read()
    if isinstance(contenido, bytes):
        return contenido.decode('utf-8', errors='ignore')
    return contenido
