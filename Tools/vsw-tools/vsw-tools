#!/bin/bash
# |----|LABELO/VSW|----|@author:FelipeArnt|----|
# vsw_tools - Canivete suíço do laboratório de Verificação de Software do LABELO.

R='\033[0;31m'
G='\033[0;32m'
Y='\033[1;33m'
C='\033[0;36m'
NC='\033[0m'

declare -A DEPENDENCIAS=(
  ["hash"]="md5sum sha1sum sha256sum sha512sum"
  ["check"]="cksum crc32"
  ["ip"]="ip sudo"
  ["nmap"]="nmap sudo"
  ["tcpdump"]="tcpdump sudo"
)

die() {
  echo -e "${R}Erro: $1${NC}" >&2
  exit 1
}

verificar_deps() {
  local cmds=("$@")
  local faltando=()
  for cmd in "${cmds[@]}"; do
    command -v "$cmd" &>/dev/null || faltando+=("$cmd")
  done
  [ ${#faltando[@]} -gt 0 ] && echo "${faltando[@]}" || echo ""
}

ajuda() {
  printf "\n"
  printf "%b\n" "${C}Ferramenta para Metrologia Legal e Segurança Cibernética.${NC}\nUso: ${0} <comando> [args]"
  printf "\n${Y}Comandos:${NC}\n"
  printf "  ${G}verificar${NC}         Verifica todas as dependências\n"
  printf "  ${G}ajuda${NC}             Mostra esta ajuda\n"
  printf "\n"
  printf "  ${G}hash <arquivo>${NC}    Calcula MD5, SHA1, SHA256, SHA512\n"
  printf "  ${G}check <arquivo>${NC}   Calcula CRC32 e Checksum\n"
  printf "  ${G}ip${NC}                Configura IP estático\n"
  printf "  ${G}nmap <args>${NC}       Executa nmap (ex: -sV 192.168.1.0/24)\n"
  printf "  ${G}tcpdump <args>${NC}    Executa tcpdump (ex: -i eth0)\n"
  printf "\n${R}Aviso: Comandos de rede requerem privilégios; use com responsabilidade.${NC}\n"
  exit 0
}

validar_arquivo() {
  [ -z "$1" ] && {
    printf "%b\n" "${R}Erro: Arquivo não especificado${NC}"
    ajuda
  }
  [ -f "$1" ] || die "Arquivo '$1' não encontrado"
}

calcular_hashes() {
  validar_arquivo "$1"
  printf "%b\n" "${C}Hashes para:${NC} $1\n${Y}----------------------------------------${NC}"
  local algoritmos=("md5" "sha1" "sha256" "sha512")
  for algo in "${algoritmos[@]}"; do
    local hash_val=$(${algo}sum "$1" 2>/dev/null | awk '{print $1}') || hash_val="N/A"
    printf "%-7s: ${G}%s${NC}\n" "${algo^^}" "$hash_val"
  done
  printf "${Y}----------------------------------------${NC}\n"
}

calcular_checksum() {
  validar_arquivo "$1"
  printf "%b\n" "${C}Checksum/CRC para:${NC} $1\n${Y}----------------------------------------${NC}"
  command -v cksum &>/dev/null && printf "Checksum (POSIX): ${G}$(cksum "$1" | awk '{print $1}')${NC}\n" || printf "${Y}cksum: não disponível${NC}\n"
  command -v crc32 &>/dev/null && printf "CRC32          : ${G}$(crc32 "$1")${NC}\n" || printf "${Y}CRC32: instale libarchive-utils${NC}\n"
  printf "${Y}----------------------------------------${NC}\n"
}

configurar_ip() {
  printf "${Y}Interfaces disponíveis:${NC}\n"
  ip link show | grep -E '^[0-9]+:' | awk -F: '{print $2}' | tr -d ' '
  read -p "Interface: " interface
  ip link show "$interface" &>/dev/null || {
    printf "%b\n" "${R}Interface '$interface' não existe${NC}"
    return 1
  }
  read -p "IP/CIDR (ex: 192.168.1.10/24): " ip_cidr
  [[ $ip_cidr =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/[0-9]{1,2}$ ]] || {
    printf "%b\n" "${R}Formato IP/CIDR inválido${NC}"
    return 1
  }
  printf "${Y}Aplicando:${NC} ip addr add $ip_cidr dev $interface\n"
  sudo ip addr add "$ip_cidr" dev "$interface" 2>/dev/null && printf "${G}IP configurado!${NC}\n" || printf "${R}Erro ao configurar IP${NC}\n"
  printf "${Y}Configuração atual:${NC}\n"
  ip addr show "$interface" | grep inet
}

executar_nmap() {
  [ $# -eq 0 ] && {
    printf "%b\n" "${R}Erro: Argumentos para nmap não especificados${NC}"
    ajuda
  }
  printf "${Y}Executando nmap: $@${NC}\n${R}Aviso: Use com responsabilidade.${NC}\n"
  sudo nmap "$@"
}

executar_tcpdump() {
  [ $# -eq 0 ] && {
    printf "%b\n" "${R}Erro: Argumentos para tcpdump não especificados${NC}"
    ajuda
  }
  printf "${Y}Executando tcpdump: $@${NC}\n${R}Aviso: Use com responsabilidade.${NC}\n"
  sudo tcpdump "$@"
}

# Função principal para processar comandos (permite usar local)
main() {
  case "${1,,}" in
  verificar)
    local todas_faltando=()
    for cmd in "${!DEPENDENCIAS[@]}"; do
      local deps=(${DEPENDENCIAS[$cmd]})
      local falt=$(verificar_deps "${deps[@]}")
      [ -n "$falt" ] && todas_faltando+=($falt)
    done
    if [ ${#todas_faltando[@]} -gt 0 ]; then
      local faltando_unicas=($(printf "%s\n" "${todas_faltando[@]}" | sort -u))
      printf "${R}Dependências faltando:${NC}\n"
      printf "  - %s\n" "${faltando_unicas[@]}"
      printf "${Y}Instale antes de continuar.${NC}\n"
    else
      printf "${G}Todas as dependências instaladas!${NC}\n"
    fi
    ;;
  hash)
    local deps=(${DEPENDENCIAS[hash]})
    [ -n "$(verificar_deps "${deps[@]}")" ] && die "Dependências faltando: $(verificar_deps "${deps[@]}")"
    calcular_hashes "$2"
    ;;
  check)
    local deps=(${DEPENDENCIAS[check]})
    [ -n "$(verificar_deps "${deps[@]}")" ] && die "Dependências faltando: $(verificar_deps "${deps[@]}")"
    calcular_checksum "$2"
    ;;
  ip)
    local deps=(${DEPENDENCIAS[ip]})
    [ -n "$(verificar_deps "${deps[@]}")" ] && die "Dependências faltando: $(verificar_deps "${deps[@]}")"
    configurar_ip
    ;;
  nmap)
    local deps=(${DEPENDENCIAS[nmap]})
    [ -n "$(verificar_deps "${deps[@]}")" ] && die "Dependências faltando: $(verificar_deps "${deps[@]}")"
    shift
    executar_nmap "$@"
    ;;
  tcpdump)
    local deps=(${DEPENDENCIAS[tcpdump]})
    [ -n "$(verificar_deps "${deps[@]}")" ] && die "Dependências faltando: $(verificar_deps "${deps[@]}")"
    shift
    executar_tcpdump "$@"
    ;;
  ajuda | -h | --help) ajuda ;;
  *)
    printf "${R}Comando não reconhecido: $1${NC}\n"
    ajuda
    ;;
  esac
}
# Chamar a função main com os argumentos do script
main "$@"
