import os
import subprocess
import sys

import streamlit as st

# Para que se puedan importar BazilioLexer, BazilioParser, etc. desde esta carpeta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Compilador Bazilio - ANTLR", page_icon="🎵")

st.title("Compilador Bazilio (ANTLR) en la Nube")
st.write(
    "Escribe tu código en Bazilio y genera tus partituras y audios desde"
    " cualquier dispositivo."
)

codigo_usuario = st.text_area(
    "Código Bazilio:", "Main\n|:\n  (:){E4 F3}\n:|\n", height=150
)

if st.button("Compilar y Generar", type="primary"):
  if not codigo_usuario.strip():
    st.warning("Por favor ingresa código.")
  else:
    try:
      os.makedirs("Practica", exist_ok=True)

      # bazilio.py se encarga de parsear, ejecutar y generar los archivos
      ruta_bzl = "temp_cloud.bzl"
      with open(ruta_bzl, "w", encoding="utf-8") as f:
        f.write(codigo_usuario)

      with st.spinner("Compilando y generando audio..."):
        res = subprocess.run(
            [sys.executable, "bazilio.py", ruta_bzl, "Main"],
            capture_output=True,
            text=True,
        )

      if res.returncode != 0:
        st.error(f"Error de sintaxis ANTLR / Ejecución:\n{res.stderr}")
      else:
        st.success("¡Compilación y generación exitosa con ANTLR!")

        # bazilio.py imprime en stderr: "Archivos generados: a, b, c"
        archivos = []
        for linea in res.stderr.splitlines():
          if linea.startswith("Archivos generados:"):
            nombres = linea.split(":", 1)[1].split(",")
            archivos = [os.path.join("Practica", n.strip()) for n in nombres]

        # Avisos (por ejemplo, si falta alguna herramienta externa)
        avisos = "\n".join(
            l for l in res.stderr.splitlines()
            if not l.startswith("Archivos generados:")
        )
        if avisos.strip():
          with st.expander("Avisos del compilador"):
            st.code(avisos)

        # Preferir MP3; si no existe, usar WAV
        audio = next((a for a in archivos if a.endswith(".mp3")), None) or next(
            (a for a in archivos if a.endswith(".wav")), None
        )
        if audio and os.path.exists(audio):
          formato = "audio/mp3" if audio.endswith(".mp3") else "audio/wav"
          st.audio(audio, format=formato)
        else:
          st.warning(
              "Compilación exitosa, pero no se generó ningún archivo de audio."
              " Revisa los avisos."
          )

        # Descargar la partitura en PDF
        pdf = next((a for a in archivos if a.endswith(".pdf")), None)
        if pdf and os.path.exists(pdf):
          with open(pdf, "rb") as f:
            st.download_button(
                "Descargar partitura (PDF)",
                f,
                file_name=os.path.basename(pdf),
                mime="application/pdf",
            )

    except Exception as e:
      st.error(f"Error: {e}")
