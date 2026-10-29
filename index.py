import hashlib
import os
import shutil
import subprocess
import sys

# Agregar la ruta actual para que importe sin problema tus archivos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Compilador Bazilio - ANTLR", page_icon="🎵")

st.title("Compilador Bazilio (ANTLR) en la Nube")
st.write(
    "Escribe tu código en Bazilio y genera tus partituras y audios desde"
    " cualquier dispositivo."
)

# Texto predeterminado actualizado según tu código funcional
codigo_usuario = st.text_area(
    "Código Bazilio:", "Main\n|:\n  (:){E4 F3}\n:|\n", height=150
)

if st.button("Compilar y Generar", type="primary"):
  if not codigo_usuario.strip():
    st.warning("Por favor ingresa código.")
  else:
    try:
      # Asegurar que la librería de ANTLR esté instalada en la nube antes de importar
      try:
        import antlr4
      except ImportError:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "antlr4-python3-runtime",
        ])
        import antlr4

      # Importaciones de ANTLR de forma segura dentro del evento
      from BazilioLexer import BazilioLexer
      from BazilioParser import BazilioParser
      from antlr4 import *
      from bazilio import BazilioVisitor

      os.makedirs("Practica", exist_ok=True)

      # 1. Procesar con ANTLR
      input_stream = InputStream(codigo_usuario)
      lexer = BazilioLexer(input_stream)
      stream = CommonTokenStream(lexer)
      parser = BazilioParser(stream)
      tree = parser.programa()

      # 2. Ejecutar tu Visitor/Listener o lógica que genera el .ly / audio
      base = os.path.join(
          "Practica",
          f"partitura_{hashlib.md5(codigo_usuario.encode()).hexdigest()[:6]}",
      )

      ruta_bzl = "temp_cloud.bzl"
      with open(ruta_bzl, "w", encoding="utf-8") as f:
        f.write(codigo_usuario)

      res = subprocess.run(
          ["python3", "bazilio.py", ruta_bzl, "Main"],
          capture_output=True,
          text=True,
      )

      if res.returncode != 0:
        st.error(f"Error de sintaxis ANTLR / Ejecución:\n{res.stderr}")
      else:
        st.success("¡Compilación y generación exitosa con ANTLR!")

        # 3. Mostrar el reproductor de audio si el archivo existe
        # (Asegúrate de cambiar "audio.mp3" por la ruta real si tu script lo guarda con otro nombre o carpeta)
        ruta_audio = "audio.mp3"  # Cambia esto si tu script genera el mp3 en otra ruta, ej: os.path.join(base, "audio.mp3")

        if os.path.exists(ruta_audio):
          st.audio(ruta_audio, format="audio/mp3")
        else:
          # Buscamos de forma general por si se guardó en la carpeta Practica
          st.info(
              "Buscando archivos de audio generados en la carpeta Practica..."
          )
          for archivo in os.listdir("Practica"):
            if archivo.endswith(".mp3"):
              path_encontrado = os.path.join("Practica", archivo)
              st.audio(path_encontrado, format="audio/mp3")

    except Exception as e:
      st.error(f"Error: {e}")