import os

from datetime import datetime

from fpdf import FPDF

class PdfService:

    @staticmethod
    def ensure_output_dir() -> str:
        """Se asegura de que existe la ruta de salida y la devuelve"""
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    @staticmethod
    def generate_pdf(content: str, title: str = "Report") -> str:
        """
        Genera un pdf de una string de texto
        """
        output_dir = PdfService.ensure_output_dir()
        filename = f"{title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(output_dir, filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, content)
        pdf.output(filepath)

        return filepath
