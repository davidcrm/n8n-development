import re

def extract_titles(text: str) -> list[str]:
    """
    Extrae títulos y subtítulos de un texto en formato Markdown o similar.
    Se consideran títulos las líneas que comienzan con uno o más signos '#' o que están en MAYÚSCULAS.

    Recibe una cadena de texto y devuelve una lista con los títulos
    """
    lines = text.splitlines()
    titles = []

    for line in lines:
        stripped = line.strip()
        if re.match(r"^#{1,6}\s+", stripped):  # Markdown headers
            titles.append(stripped)
        elif stripped.isupper(): #Mayusculas
            titles.append(stripped)
    
    return titles
