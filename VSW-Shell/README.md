# VSW-Shell 🛡️

> **Shell Interativa para Metrologia Legal & Testes de Segurança Cibernética**

![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-Audit%20Required-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Beta-orange?style=for-the-badge)

---

## 🎯 Visão Geral

A **VSW-Shell** é uma shell interativa customizada desenvolvida para profissionais de metrologia legal e testes de segurança cibernética (CTF). Ela fornece uma interface profissional com builtins especializados, wrappers seguros e integração com ferramentas Python & Basg para automação de ensaios.

### Características Principais
- ✅ **Input sanitizado** em todos os comandos
- ✅ **Execução segura** via `fork()+exec()` (sem `system()`)
- ✅ **Output colorido** para melhor legibilidade
- ✅ **Histórico persistente** (`.vsw_history`)
- ✅ **Modular**: C + Python + Bash
- ✅ **Pronta para auditoria**: Código documentado e validado

---

## 📦 Requisitos de Sistema

### Dependências de Compilação
```bash
gcc >= 11.0
make (opcional)
bash >= 4.0 (para nameref)
```

### Dependências de Runtime
```bash
# Ferramentas de rede
nmap, netcat (nc), tcpdump, adb (para TV-BOX)

# Utilitários de hash
md5sum, sha1sum, sha256sum, sha512sum, crc32

# Python 3.9+
python3, python3-pip

# Ambiente virtual (recomendado)
uv (ou pip + venv)
```

### Instalação no Arch Linux
```bash
sudo pacman -S gcc bash python nmap tcpdump adb md5deep libarchive
yay -S uv  # ou instale via pip
```

---

## 🎮 Uso

### Iniciando a Shell
```bash
vsw
```

### Comandos Disponíveis

| Comando | Descrição | Segurança |
|---------|-----------|-----------|
| `cd <dir>` | Navegação de diretórios | ✅ Sanitizado |
| `help` | Lista todos os builtins | ✅ Estável |
| `tools` | Canivete suíço (hash, nmap, tcpdump) | ✅ Sanitizado |
| `tvbox` | Auditoria de TV-BOX via ADB | ✅ Sanitizado |
| `roteador` | Scan de roteadores com nmap | ✅ Sanitizado |
| `comparador` | Comparação de dados (Python) | ✅ Estável |
| `tabela` | Geração de tabelas (Python) | ✅ Estável |
| `difere` | Diff de arquivos (Python) | ✅ Estável |
| `autometro` | Automação de ensaios (Python) | ✅ Estável |
| `exit` | Sai da shell | ✅ Estável |

### Exemplos

```bash
# Navegar diretório
vsw > cd /var/log

# Verificar dependências do sistema
vsw > tools verificar

# Calcular hash de arquivo
vsw > tools hash /path/to/firmware.bin

# Configurar IP estático
vsw > tools ip

# Scan de roteador (inputs sanitizados)
vsw > roteador
# Digite IP: 192.168.1.1  # ✅ Aceito
# Digite IP: 192.168.1.1; ls -la  # ❌ Bloqueado

# Auditoria TV-BOX
vsw > tvbox
# Digite protocolo: http  # ✅ Aceito
# Digite protocolo: http; rm -rf  # ❌ Bloqueado
```

---

## 🔒 Detalhes de Segurança

### Sanitização em C (src/utils.c)
```c
bool limpador(const char *input, char *output, size_t out_size) {
    // Permite apenas: alfanuméricos, . - _ /
    // Bloqueia: ; | & ` $ ( ) etc.
}
```

### Sanitização em Bash (src-sh/security.sh)
```bash

ler_input_validado() {
    # Valida input contra regex predefinidos
    # Bloqueia command injection automaticamente
}
```

### Execução Segura

- **Nenhum `system()`** no código C
- **Fork+Exec** para isolamento de processos
- **Caminhos absolutos** para executáveis
- **Validação de permissões** antes de executar scripts

---

**Desenvolvido por Felipe Arnt | LABELO/VSW - Metrologia Legal & Segurança Cibernética**`

