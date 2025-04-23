import re

def extract_titles(text: str) -> list[str]:
    """
    Extrae títulos y subtítulos de un texto en formato Markdown o similar.
    Se consideran títulos las líneas que comienzan con uno o más signos '#' o que están en MAYÚSCULAS.

    Args:
        text (str): Contenido del archivo como texto plano.

    Returns:
        list[str]: Lista de líneas que representan títulos y subtítulos.
    """
    lines = text.splitlines()
    titles = []

    for line in lines:
        stripped = line.strip()
        if re.match(r"^#{1,6}\s+", stripped):  # Markdown headers
            titles.append(stripped)
        elif stripped.isupper() and len(stripped) > 3:  # Mayúsculas estilo títulos
            titles.append(stripped)
    
    return titles
