import os
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS

# IMPORTA AQUÍ TUS MÓDULOS DE ANTLR4
# from antlr4 import *
# from BazilioLexer import BazilioLexer
# from BazilioParser import BazilioParser

app = Flask(__name__)
CORS(app)

# Definir la ruta de la carpeta Practica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'Practica')
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# HTML y JavaScript embebidos directamente en Python
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Compilador Bazilio (ANTLR) en la Nube</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {
      background-color: #0d1117;
      color: #c9d1d9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-4">

  <div class="w-full max-w-sm space-y-4">
    <!-- Encabezado -->
    <header class="text-left space-y-2">
      <h1 class="text-3xl font-bold text-white leading-tight">
        Compilador Bazilio<br>(ANTLR) en la Nube
      </h1>
      <p class="text-xs text-gray-300 leading-normal">
        Escribe tu código en Bazilio y genera tus partituras y audios desde cualquier dispositivo.
      </p>
    </header>

    <!-- Editor de Código -->
    <div class="space-y-1">
      <label class="block text-xs font-medium text-gray-300">Código Bazilio:</label>
      <textarea id="codeEditor" rows="5" class="w-full bg-[#161b22] text-gray-200 p-3 rounded-lg border border-gray-700/60 font-mono text-xs focus:outline-none focus:border-red-500 resize-none">Main
|:
 (:) {E4 F3}
:|</textarea>
    </div>

    <!-- Botón -->
    <button id="btnCompile" onclick="compilarYGenerar()" class="w-full bg-[#e50914] hover:bg-red-700 text-white font-semibold py-2.5 rounded-lg text-xs tracking-wide transition-all shadow-md">
      Compilar y Generar
    </button>

    <!-- Mensajes de Estado -->
    <div id="successBox" class="hidden bg-[#0a271d] border border-emerald-800/60 text-emerald-300 p-3.5 rounded-lg text-xs font-medium">
      ¡Compilación y generación exitosa con ANTLR!
    </div>

    <div id="searchBox" class="hidden bg-[#0b1d33] border border-sky-800/60 text-sky-300 p-3.5 rounded-lg text-xs leading-relaxed">
      Buscando archivos de audio generados en la carpeta Practica...
    </div>

    <!-- REPRODUCTOR DE AUDIO DE PYTHON -->
    <div id="audioCard" class="hidden bg-[#161b22] border border-gray-700/80 rounded-xl p-4 space-y-3 shadow-lg">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold text-gray-200">Audio Generado</span>
        <span class="text-[10px] bg-red-950/80 text-red-400 border border-red-800/80 px-2 py-0.5 rounded font-mono">
          ANTLR v4
        </span>
      </div>

      <!-- Reproductor Nativo HTML5 -->
      <audio id="audioPlayer" controls class="w-full rounded-lg h-9 mt-1 accent-red-600">
        Tu navegador no soporta reproducción de audio.
      </audio>

      <div class="flex justify-end pt-1">
        <a id="downloadLink" href="#" download="audio_bazilio.wav" class="text-[11px] text-gray-400 hover:text-white underline transition">
          Descargar .wav
        </a>
      </div>
    </div>
  </div>

  <script>
    async function compilarYGenerar() {
      const code = document.getElementById('codeEditor').value;
      const btn = document.getElementById('btnCompile');
      
      const successBox = document.getElementById('successBox');
      const searchBox = document.getElementById('searchBox');
      const audioCard = document.getElementById('audioCard');
      const audioPlayer = document.getElementById('audioPlayer');
      const downloadLink = document.getElementById('downloadLink');

      btn.disabled = true;
      btn.innerText = "Procesando con ANTLR...";

      try {
        const response = await fetch('/compile', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code: code })
        });

        const data = await response.json();

        if (response.ok && data.status === 'success') {
          successBox.classList.remove('hidden');
          searchBox.classList.remove('hidden');

          // Asignar el nuevo audio
          audioPlayer.src = data.audio_url + '?t=' + new Date().getTime(); // Evitar caché
          downloadLink.href = data.audio_url;

          audioCard.classList.remove('hidden');

          // Intentar reproducir automáticamente
          audioPlayer.play().catch(e => console.log("Click en play para escuchar"));
        } else {
          alert("Error: " + data.message);
        }
      } catch (err) {
        alert("Error de conexión con el servidor Python.");
      } finally {
        btn.disabled = false;
        btn.innerText = "Compilar y Generar";
      }
    }
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    """ Sirve la vista web principal desde la variable HTML_TEMPLATE """
    return render_template_string(HTML_TEMPLATE)

@app.route('/compile', methods=['POST'])
def compile_bazilio():
    data = request.get_json()
    code = data.get('code', '')

    try:
        # 1. AQUÍ PROCESAS CON TU COMPILADOR ANTLR4
        # input_stream = InputStream(code)
        # lexer = BazilioLexer(input_stream)
        # stream = CommonTokenStream(lexer)
        # parser = BazilioParser(stream)
        # tree = parser.main()

        # 2. NOMBRE Y RUTA DEL ARCHIVO DENTRO DE Practica/
        filename = "resultado.wav"
        output_file_path = os.path.join(OUTPUT_FOLDER, filename)

        # 3. GENERA EL ARCHIVO AUDIO EN LA CARPETA Practica
        # (Llama aquí a tu método que crea/escribe el .wav)
        generar_audio_dummy(output_file_path)

        return jsonify({
            "status": "success",
            "message": "¡Compilación y generación exitosa con ANTLR!",
            "audio_url": f"/audio/{filename}"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/audio/<filename>')
def get_audio(filename):
    """ Servidor de archivos estáticos para entregar los audios de la carpeta Practica """
    return send_from_directory(OUTPUT_FOLDER, filename)

def generar_audio_dummy(path):
    """ 
    Función de prueba para crear un .wav básico si aún no se ha generado uno con ANTLR.
    Sustitúyela por tu lógica de audio en Python.
    """
    import wave, struct
    with wave.open(path, 'w') as wav_file:
        wav_file.setnchannels(1) # Monofónico
        wav_file.setsampwidth(2) # 16 bits
        wav_file.setframerate(44100) # 44.1kHz
        # Generar 1 segundo de silencio/tono simple
        for _ in range(44100):
            wav_file.writeframesraw(struct.pack('<h', 0))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
