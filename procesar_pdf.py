import fitz
import re

def procesar_pdf_siga(ruta_pdf):
    patrones = {
      "fecha_prueba": r"FECHA DE LA PRUEBA:[\s\n]*([\d-]+)",
      "tipo_documento": r"TIPO DE DOCUMENTO:[\s\n]*([A-Z]+)",
      "identificacion": r"IDENTIFICACIÓN:[\s\n]*([\d,]+)",
      "nombres": r"NOMBRES:[\s\n]*([^\n]+)",
      "apellidos": r"APELLIDOS:[\s\n]*([^\n]+)",
      "edad": r"EDAD:[\s\n]*(\d+)"
    }
    pagina_resultado = {}
    doc = fitz.open(ruta_pdf)

    for page in doc:
        texto_crudo = page.get_text()

        if not texto_crudo:
            continue

        datos_estudiante = {}
        for clave, patron in patrones.items():
            match = re.search(patron, texto_crudo)
            if match:
                datos_estudiante[clave] = match.group(1).replace('"', '').strip()
            else:
                datos_estudiante[clave] = "No encontrado"

        match_perfil = re.search(r"Búsqueda autodirigida[\s\n\"\'_]+([A-Z]{3})", texto_crudo)
        if match_perfil:
            datos_estudiante["perfil_sds"] = match_perfil.group(1).strip()
        else:
            datos_estudiante["perfil_sds"] = "No encontrado"

        pagina_resultado[str(page.number)] = datos_estudiante

    doc.close()

    if not pagina_resultado:
        return {"error": "No se pudo extraer texto del PDF."}

    return pagina_resultado