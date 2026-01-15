# Script de Ensaios Funcionais em TV-Box

## Descrição

Este script em shell foi desenvolvido para automatizar a coleta de dados de dispositivos TV-Box baseados em Android, com foco na conformidade com o ATO 9281/2016 da Agência Nacional de Telecomunicações (Anatel). 

Executa verificações essenciais para procedimentos de ensaio, incluindo listagem de softwares e softwares de terceiros, propriedades do sistema, configurações de rede e verificações específicas de segurança cibernética.

O script está estruturado em 4 funções específicas para a realização dos ensaios nos dispositivos, as funções são:

- #### `main()`
- #### `init_ensaio()`
- #### `exec_ensaio()`
- #### `save_ensaio()`


## Pré-requisitos

- **Sistema Operacional**: Linux, macOS ou Windows (com WSL ou Git Bash).
- **ADB (Android Debug Bridge)**: Instalado e configurado. Baixe do [site oficial do Android](https://developer.android.com/studio/command-line/adb).
- **Dispositivo TV-Box**: Conectado via USB, com depuração USB habilitada e autorizada no dispositivo.
- **Permissões**: Execute o script com privilégios adequados (ex.: `chmod +x tvbox_script.sh`). O dispositivo deve estar na configuração de mercado, conforme exigido pelo ATO 9281 (5.2.1).

## Instalação

1. Baixe ou clone o repositório contendo o script.
2. Torne o script executável:

   ```bash
   chmod +x tvbox_script.sh
   ```

3. Certifique-se de que o ADB está no PATH do sistema. Teste com:

   ```bash
   adb version
   ```

## Uso

1. Conecte o TV-Box ao computador via USB.
2. Execute o script:

   ```bash
   ./tvbox_script.sh
   ```

3. Insira o protocolo e orçamento da amostra quando solicitado.
4. Aguarde a execução (aproximadamente 1-2 minutos, dependendo do dispositivo).

### Exemplo de Execução

```bash
$ ./tvbox_script.sh
==== VSW ====
==== TV-BOX ====
Digite o protocolo da amostra: 0000
Digite o orçamento da amostra: 0000
[INFO]: Script finalizado. Relatórios em relatorio_tvbox.md e aplicativos_tvbox.md
```

### Tratamento de Erros

- Se o ADB não detectar o dispositivo, verifique a conexão USB e habilite a depuração pelo modo de desenvolvedor da TV-BOX.
- Em caso de falha em comandos ADB (ex.: dispositivo não rootado), o script registra "Erro" ou "NÃO detectado" e continua.
- Para dispositivos com restrições (ex.: sem root), algumas verificações podem requerer análise manual.

## Funcionalidades

- **Coleta Automatizada**:
  - Propriedades do sistema (modelo, versão Android, kernel).
  - Listagem de aplicativos (sistema e terceiros) em tabelas Markdown.
  - Informações de rede (Netstat, conectividade, Wi-Fi, telefone).
  - Estado do dispositivo (dumpsys de pacotes e rede).
