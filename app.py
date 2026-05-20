import streamlit as st
import tempfile
import zipfile
import io
import traceback
import os
from pathlib import Path
from main import ejecutar_sistema_completo

PASSWORD = os.environ.get("APP_PASSWORD", "")

st.set_page_config(page_title="Generador de Informes SDS", page_icon="📄")

if PASSWORD:
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False

    if not st.session_state.autenticado:
        st.title("Acceso Restringido")
        pwd = st.text_input("Contrasena", type="password")
        if st.button("Ingresar"):
            if pwd == PASSWORD:
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Contrasena incorrecta")
        st.stop()

st.title("Generador de Informes de Orientacion Vocacional (SDS)")

PLANTILLA_PATH = Path(__file__).parent / "data" / "plantilla_informe.docx"
MANUAL_DEFAULT = Path(__file__).parent / "data" / "PRUEBA SDS (5).docx"

st.markdown("### 1. Sube el PDF de resultados")
pdf_file = st.file_uploader("PDF con los resultados de los estudiantes", type=["pdf"])

st.markdown("### 2. Sube el manual de perfiles (opcional)")
manual_file = st.file_uploader(
    "Documento Word con la interpretacion de cada perfil (si no se sube, se usa el manual por defecto)",
    type=["docx"]
)

st.markdown("---")

if st.button("Generar Informes", type="primary", disabled=(pdf_file is None)):
    if not pdf_file:
        st.error("Debes subir el PDF de resultados.")
        st.stop()

    if not PLANTILLA_PATH.exists():
        st.error("No se encontro la plantilla de informe en el servidor.")
        st.stop()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Guardar PDF subido
        pdf_path = tmpdir / "resultados.pdf"
        pdf_path.write_bytes(pdf_file.read())

        # Guardar manual (subido o default)
        if manual_file:
            manual_path = tmpdir / "manual.docx"
            manual_path.write_bytes(manual_file.read())
        else:
            manual_path = MANUAL_DEFAULT

        output_dir = tmpdir / "informes"
        output_dir.mkdir()

        status = st.status("Procesando...", expanded=True)
        try:
            status.write("Procesando manual de orientacion...")
            ejecutar_sistema_completo(
                str(pdf_path),
                str(manual_path),
                str(PLANTILLA_PATH),
                str(output_dir)
            )

            # Crear ZIP solo con los PDFs generados
            pdfs = list(output_dir.glob("*.pdf"))
            if not pdfs:
                docs_fallback = list(output_dir.glob("*.docx"))
                archivos = docs_fallback
                tipo = "DOCX"
            else:
                archivos = pdfs
                tipo = "PDF"

            if not archivos:
                status.update(label="Error", state="error")
                st.error("No se genero ningun informe. Revisa el PDF o el manual.")
                st.stop()

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                for f in archivos:
                    zf.write(f, f.name)

            status.update(label="Completado!", state="complete")
            st.success(f"Se generaron {len(archivos)} informes {tipo}.")
            st.download_button(
                label="Descargar ZIP con todos los informes",
                data=zip_buffer.getvalue(),
                file_name="informes_sds.zip",
                mime="application/zip",
                type="primary"
            )

        except Exception as e:
            status.update(label="Error en el proceso", state="error")
            st.error(str(e))
            with st.expander("Detalles tecnicos (traceback)"):
                st.code(traceback.format_exc())
