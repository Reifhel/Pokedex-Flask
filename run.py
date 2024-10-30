import subprocess
import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Quando for rodar, executar o script para gerar o web_assembly
    # LEMBRAR DE ATIVAR O EMSCRIPTEN NO TERMINAL QUE VOCÊ ESTÁ USANDO PQ SENÃO NÃO GERA O JS E WASM
    command = [
        "em++", "fib.cpp",
        "-s", "EXPORTED_FUNCTIONS=['_fibonacci']",
        "-s", "EXPORTED_RUNTIME_METHODS=['ccall', 'cwrap']",
        "-o", "../static/js/out_fibonacci.js"  # Especifica o arquivo de saída em JavaScript
    ]
    old_path = os.getcwd()
    library_dir = os.path.abspath("app/lib")
    os.chdir(library_dir)
    try:
        subprocess.run(command, check=True)
        print("Compilação bem-sucedida! Arquivo output.js gerado.")
    except subprocess.CalledProcessError as e:
        print("Erro na compilação:", e)
    finally:    
        os.chdir(old_path)
        app.run(debug=True)
