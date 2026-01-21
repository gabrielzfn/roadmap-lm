#!/usr/bin/env bash

# |----|LABELO/VSW|----|@author:FelipeArnt|----|
#
# Ferramentas = nmap, talvez MITM, BURPSUITE

set -euo pipefail

OUTPUT_DIR="coleta_roteador"
LOGFILE="${OUTPUT_DIR}/exec.log"

die() {
  echo "[ERRO] $*" | tee -a "$LOGFILE"
  exit 1
}

log() { echo "[INFO] $*" | tee -a "$LOGFILE"; }

uso() {
  cat <<EOF
Uso: $0 [-h]

-h   Exibe esta ajuda
-c   Limpa coleta_roteador anterior

EOF
  exit 0
}

while getopts "hc" opt; do
  case $opt in
  h) uso ;;
  c) rm -rf "$OUTPUT_DIR" ;;
  *) uso ;;
  esac
done

init_ensaio() {

  command -v nmap >/dev/null 2>&1 || die "Nmap não foi encontrado, instale o pacote para proseguir com o ensaio..."
  mkdir -p "$OUTPUT_DIR" || die "Não foi possível criar o diretório..."

  arp -a
  ifconfig

  read -rp "Digite o IP do dispostivo: " IP
  [[ -z "$IP" ]] && die "IP não pode ser vazio..."

  read -rp "Digite o protocolo da amostra: " PROTOCOLO
  [[ -z "$PROTOCOLO" ]] && die "Protocolo não pode ser vazio..."

  read -rp "Digite o orçamento da amostra: " ORCAMENTO
  [[ -z "$ORCAMENTO" ]] && die "Protocolo não pode ser vazio..."

  PREFIXO="$ORCAMENTO"
}

exec_ensaio() {
  log "Iniciando ensaios funcionais no dispostivo..."
  # Apenas nmap por enquanto
  sudo nmap -sV "$IP" >"${OUTPUT_DIR}/${PREFIXO}_sV.txt"
  sudo nmap -sV -webxml -oX vuln.xml -v --script vuln "$IP"
  sudo nmap -sV -webxml -oX vulners.xml --script -v vulners "$IP"
  sudo nmap -webxml -oX vulscan.xml -v -sV --script=vulscan/vulscan.nse "$IP"
}

save_ensaio() {
  cat <<EOF >"${OUTPUT_DIR}/${PREFIXO}_resumo.json"
{
  "Protocolo": "$PROTOCOLO",
  "Orcamento": "$ORCAMENTO",
  "IP":    "$IP"
}
EOF

  log "Ensaio funcional finalizado em {OUTPUT_DIR}"
  log "Arquivos salvos com prefixo {PREFIXO}"
  exit 0
}

main() {
  init_ensaio
  exec_ensaio
  save_ensaio
}

main "$@"
