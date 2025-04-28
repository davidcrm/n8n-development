from utils import PdfService

if __name__ == "__main__":
    content = """Este es un documento de prueba para verificar que la clase PdfService funciona correctamente.

Incluye varias líneas de texto para comprobar el formato del PDF generado."""
    title = "Informe de prueba"

    pdf_path = PdfService.generate_pdf(content, title)
    print(f"✅ PDF generado correctamente en: {pdf_path}")
