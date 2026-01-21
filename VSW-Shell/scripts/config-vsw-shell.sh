#!/usr/bin/env bash

echo "[vsw-info]: Iniciando script para configurar o ambiente da vsw-shell e seus comandos."

configurar_comandos() {

  echo "[vsw-config]: Configuração em andamento..."
  # Copiando arquivo compilado da shell para o devido diretorio.
  sudo cp -r ../src/out /usr/local/bin/vsw

  # Copiando scripts em bash para o devido diretorio.
  sudo cp -r src-sh/build.sh /usr/local/bin/build
  sudo cp -r src-sh/clean.sh /usr/local/bin/clean
  sudo cp -r src-sh/router.sh /usr/local/bin/roteador
  sudo cp -r src-sh/tvbox.sh /usr/local/bin/tvbox
  sudo cp -r src-sh/vsw-tools.sh /usr/local/bin/tools

  # Copiando scripts em python3 para o devido diretorio.
  chmod +x src-py/comparador.py && sudo cp -r src-py/comparador.py /usr/local/bin/comparador.py
  chmod +x src-py/autometro.py && sudo cp -r src-py/autometro.py /usr/local/bin/autometro.py
  chmod +x src-py/differ.py && sudo cp -r src-py/differ.py /usr/local/bin/differ.py
  chmod +x src-py/tablelo.py && sudo cp -r src-py/tablelo.py /usr/local/bin/tabela.py

  # Ajeitar nome dos scripts acima
  echo "Script finalizado com sucesso!"
} #faltam verificações e etc, mas farei isso depois!

instalar_dependencias() {
  echo "[vsw-install]: Criando ambiente virtual python e instalando dependências..."

  uv venv

  source .venv/bin/activate

  uv pip install -r src-py/requisitos.txt

}

main() {
  configurar_comandos
  instalar_dependencias
}

main "@$"
