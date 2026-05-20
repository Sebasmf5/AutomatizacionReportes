import json
import os
from docxtpl import DocxTemplate
from utilidades import convertir_word_a_pdf_linux

def generar_reportes(datos_estudiantes, ruta_json_perfiles, ruta_plantilla, carpeta_salida):
    with open(ruta_json_perfiles, 'r', encoding='utf-8', errors='replace') as f:
        perfiles_conocimiento = json.load(f)

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    total = len(datos_estudiantes)
    generados = 0
    print(f"Iniciando generacion de {total} informes...")

    for id_est, estudiante in datos_estudiantes.items():
        if "error" in estudiante or estudiante.get("nombres") == "No encontrado":
            continue

        perfil_codigo = estudiante.get("perfil_sds")
        if perfil_codigo not in perfiles_conocimiento:
            print(f"Perfil '{perfil_codigo}' no encontrado para {estudiante.get('nombres')}")
            continue

        datos_perfil = perfiles_conocimiento[perfil_codigo]
        try:
            doc = DocxTemplate(ruta_plantilla)

            contexto = {
                "nombres": estudiante["nombres"],
                "apellidos": estudiante["apellidos"],
                "tipo_documento": estudiante["tipo_documento"],
                "identificacion": estudiante["identificacion"],
                "fecha_prueba": estudiante.get("fecha_prueba", ""),
                "resultado_general": str(datos_perfil.get("resultado_general", "")),
                "interpretacion":    str(datos_perfil.get("interpretacion", "")),
                "areas_afines":      str(datos_perfil.get("areas_afines", "")),
                "concepto_evaluador": str(datos_perfil.get("concepto_evaluador", "")),
            }

            doc.render(contexto)
            nombre_est = estudiante['nombres'].replace(' ', '_').strip()
            nombre_base = f"Informe_{nombre_est}"
            ruta_docx = os.path.join(carpeta_salida, f"{nombre_base}.docx")
            doc.save(ruta_docx)

            if convertir_word_a_pdf_linux(ruta_docx, carpeta_salida):
                os.remove(ruta_docx)
                generados += 1
                print(f"  [{generados}/{total}] {nombre_base}.pdf")
            else:
                print(f"  Fallo conversion PDF, se conserva DOCX: {nombre_base}.docx")

        except Exception as e:
            print(f"Error procesando a {estudiante.get('nombres')}: {e}")

    print(f"Se generaron {generados} informes en: {carpeta_salida}")