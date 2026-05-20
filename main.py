import os
from cargar_json import *
from procesar_pdf import *
from generar_reportes import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", os.path.join(BASE_DIR, "output"))

def ejecutar_sistema_completo(ruta_pdf_resultados, ruta_docx_manual, ruta_plantilla, carpeta_salida):
    print("--- INICIANDO PROCESO INTEGRADO (SALIDA EN PDF) ---")

    os.makedirs(carpeta_salida, exist_ok=True)
    ruta_json_temp = os.path.join(carpeta_salida, "perfiles.json")

    try:
        print("\n[1/3] Procesando manual de orientacion y aplicando formato...")
        generar_json_perfiles(ruta_docx_manual, ruta_json_temp)

        print("\n[2/3] Extrayendo datos del PDF de resultados...")
        datos_estudiantes = procesar_pdf_siga(ruta_pdf_resultados)

        print(f"\n[3/3] Generando reportes y convirtiendo a PDF en: {carpeta_salida}...")
        generar_reportes(datos_estudiantes, ruta_json_temp, ruta_plantilla, carpeta_salida)

        print("\nPROCESO COMPLETADO EXITOSAMENTE!")

    except Exception as e:
        print(f"\nERROR DURANTE LA EJECUCION: {e}")
        raise


if __name__ == "__main__":
    from pathlib import Path
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    ejecutar_sistema_completo(
        os.path.join(DATA_DIR, "Resultados.pdf"),
        os.path.join(DATA_DIR, "PRUEBA SDS (5).docx"),
        os.path.join(DATA_DIR, "plantilla_informe.docx"),
        OUTPUT_DIR,
    )