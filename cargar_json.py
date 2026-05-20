import json
import re
from docx import Document

def generar_json_perfiles(ruta_docx, ruta_json):
    """
    Lee el manual de orientación en Word y lo convierte en un JSON estructurado.
    Aplica negrita a los nombres de los componentes/subtemas en la interpretación.
    """
    doc = Document(ruta_docx)
    perfiles = {}
    perfil_actual = None
    seccion_actual = None

    for para in doc.paragraphs:
        texto = para.text
        if texto:
            texto = texto.encode('utf-8', errors='replace').decode('utf-8')
        texto = texto.strip()
        if not texto:
            continue

        match_perfil = re.match(r'^([A-Z]{3})\b', texto)
        if match_perfil and "General" not in texto:
            perfil_actual = match_perfil.group(1)
            perfiles[perfil_actual] = {
                "resultado_general": "",
                "interpretacion": "",
                "areas_afines": "",
                "concepto_evaluador": ""
            }
            seccion_actual = None
            continue

        if not perfil_actual:
            continue

        texto_lower = texto.lower()

        if "resultado general" in texto_lower:
            seccion_actual = "resultado_general"
            texto = re.sub(r'(?i)resultado general:?\s*', '', texto)
        elif "interpretación del perfil" in texto_lower or "interpretacion del perfil" in texto_lower:
            seccion_actual = "interpretacion"
            continue
        elif "áreas académicas" in texto_lower or "areas académicas" in texto_lower or "profesionales afines" in texto_lower:
            seccion_actual = "areas_afines"
            continue
        elif "concepto del evaluador" in texto_lower or "concepto orientador" in texto_lower:
            seccion_actual = "concepto_evaluador"
            texto = re.sub(r'(?i)concepto (del evaluador|orientador):?\s*', '', texto)

        if seccion_actual and texto:
            perfiles[perfil_actual][seccion_actual] += texto + "\n"

    for p in perfiles:
        for s in perfiles[p]:
            perfiles[p][s] = perfiles[p][s].strip()

    with open(ruta_json, 'w', encoding='utf-8', errors='replace') as f:
        json.dump(perfiles, f, ensure_ascii=False, indent=4)

    print(f"¡Éxito! JSON creado con {len(perfiles)} perfiles.")