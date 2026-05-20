import os
import subprocess

def convertir_word_a_pdf_linux(entrada, salida_dir):
    """
    Convierte un archivo Word a PDF en Linux usando LibreOffice.
    :param entrada: Ruta del archivo .docx
    :param salida_dir: Carpeta donde guardar el PDF
    """
    try:
        if not os.path.isfile(entrada):
            raise FileNotFoundError(f"El archivo '{entrada}' no existe.")

        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", salida_dir, entrada
        ], check=True, capture_output=True, text=True)

        nombre_base = os.path.splitext(os.path.basename(entrada))[0]
        pdf_generado = os.path.join(salida_dir, f"{nombre_base}.pdf")
        ok = os.path.isfile(pdf_generado)
        if ok:
            print(f"PDF generado en: {pdf_generado}")
        return ok

    except Exception as e:
        print(f"Error: {e}")
        return False
