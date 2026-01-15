#!/usr/bin/env bash
# |----|LABELO/VSW|----|@author:FelipeArnt|----|
# vsw-tv – Script para Ensaios Funcionais em TV-BOX via ADB

set -euo pipefail

# Configurações
OUTPUT_DIR="coleta_tvbox"
LOGFILE="${OUTPUT_DIR}/_exec.log"

die() {
  echo "[ERRO] $*" | tee -a "$LOGFILE"
  exit 1
}
log() { echo "[INFO] $*" | tee -a "$LOGFILE"; }

uso() {
  cat <<EOF
Uso: $0 [-h] [-c]

  -h  Mostra esta ajuda
  -c  Limpa coletas anteriores (${OUTPUT_DIR}) antes de rodar
EOF
  exit 0
}

# Validações
while getopts "hc" opt; do
  case $opt in
  h) uso ;;
  c) rm -rf "$OUTPUT_DIR" ;;
  *) uso ;;
  esac
done

init_ensaio() {

  command -v adb >/dev/null 2>&1 || die "ADB não encontrado. Instale o Android SDK Platform-Tools."

  mkdir -p "$OUTPUT_DIR" || die "Não consegui criar ${OUTPUT_DIR}"
  # Entradas
  read -rp "Digite o protocolo da amostra: " PROTOCOLO
  [[ -z "$PROTOCOLO" ]] && die "Protocolo não pode ser vazio."
  read -rp "Digite o orçamento da amostra: " ORCAMENTO
  [[ -z "$ORCAMENTO" ]] && die "Orçamento não pode ser vazio."

  PREFIX="${ORCAMENTO// /_}"

  # Dispositivo
  log "Verificando dispositivo ADB..."
  adb wait-for-device || die "Nenhum dispositivo detectado. Verifique o cabo/USB-debug."
  SERIAL=$(adb get-serialno)
  log "Dispositivo detectado: ${SERIAL}"
}

exec_ensaio() {
  # Coleta
  log "Iniciando ensaios funcionais no dispositivo..."
  # 1) Pacotes simplificados (nomes apenas)
  adb shell pm list packages -s >"${OUTPUT_DIR}/${PREFIX}_pkgs_sistema.txt"
  adb shell pm list packages -3 >"${OUTPUT_DIR}/${PREFIX}_pkgs_terceiros.txt"

  # 2) Apenas propriedades essenciais
  {
    echo "kernel_version: $(adb shell uname -r)"
    echo "Versao Android: $(adb shell getprop ro.build.version.release)"
    echo "Modelo: $(adb shell getprop ro.product.model)"
    echo "Patch de segurança: $(adb shell getprop ro.build.version.security_patch)"
    echo "Modo root: $(adb shell getprop ro.debuggable)"
    echo "Root bin?: $(adb shell 'which su' || echo 'Não encontrado')"
    echo "Permite terceiros: $(adb shell settings get secure install_non_market_apps)"
  } >"${OUTPUT_DIR}/${PREFIX}_essenciais.txt"

  # 3) Portas/serviços relevantes
  adb shell netstat -tuln >"${OUTPUT_DIR}/${PREFIX}_netstat.txt"
}

save_ensaio() {
  cat <<EOF >"${OUTPUT_DIR}/${PREFIX}_resumo.json"
{
  "protocolo": "$PROTOCOLO",
  "orcamento": "$ORCAMENTO",
  "serial": "$SERIAL",
  "kernel_version:" "$(adb shell uname -r)"
  "android_versao": "$(adb shell getprop ro.build.version.release)",
  "modelo": "$(adb shell getprop ro.product.model)"
  "Patch de segurança: $(adb shell getprop ro.build.version.security_patch)"
  "Modo root: $(adb shell getprop ro.debuggable)"
  "Root bin?: $(adb shell 'which su' || echo 'Não encontrado')"
  "Permite terceiros: $(adb shell settings get secure install_non_market_apps)"
}
EOF
  # Finalização
  log "Coleta finalizada em ${OUTPUT_DIR}"
  log "Arquivos salvos com prefixo: ${PREFIX}"
  exit 0
}

main() {
  init_ensaio
  exec_ensaio
  save_ensaio
}

main "$@"
