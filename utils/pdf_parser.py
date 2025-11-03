import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """
    Extrage textul brut dintr-un fisier PDF.

    Args:
        pdf_path (str): Calea catre fisierul PDF.

    Returns:
        str: Textul extras sau un mesaj de eroare.
    """
    if not os.path.exists(pdf_path):
        return f"Eroare: Fisierul nu a fost gasit la calea: {pdf_path}"

    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Iteram prin fiecare pagina din PDF
            for page in pdf.pages:
                # Extragem textul de pe pagina
                text = page.extract_text()
                if text:
                    full_text += text + "\n"

        return full_text

    except Exception as e:
        return f"Eroare la procesarea PDF-ului: {e}"