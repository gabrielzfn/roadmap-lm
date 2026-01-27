# VSW-SHELL

Uma shell é um programa que interage com o computador, nesse caso os comandos servem para a realização de ensaios de Segurança Cibernética, de acordo com os Atos da ANATEL.

Comandos básicos para se localizar na shell:

- `sudo` = super user do, Garante permissões de administrador. 
- `cd` = cwdir, Troca de diretório (Pasta).
- `ls`= list, Exibe o conteúdo do diretório atual ou do utilizado como argumento após o comando
- `cat`= concatenate, Exibe o conteúdo do arquivo utilizado após o comando.  
- `ifconfig` ou `ipconfig`, Exibe as interfaces de rede da máquina.
- `roteador`, Inicia os ensaios funcionais de acordo com a IT de VSW no roteador alvo. 
- `tvbox`, Inicia os ensaios funcionais no dispositivo TV-Box. 
- `vswit`, Exibe as Instruções de Trabalho do laboratório de VSW.

## Como iniciar os ensaios em roteadores?

O primeiro passo é verificar se possuímos todas dependências necessárias para o ensaio.

- nmap
- tcpdump (opcional por enquanto)
- script do vulnscan, localizado no github abaixo:
  - https://github.com/scipag/vulscan

1. `cd vsw-shell`
2. `cd script`
3. `./Config.sh` ou `bash Config.sh` -> se o script funcionou, apenas digite "build" no diretório "src" que contém o código-fonte da **VSW-SHELL**.
4. `cd ..` -> para voltar para a pasta anterior.
5. Se programa for compilado com sucesso, a vsw-shell terá inicializado e você precisa apenas digitar "roteador" e seguir o procedimento padrão de configuração de IP, protocolo e orçamentos da amostra.

## Como iniciar os ensaios de TV-Box

É fundamental a instalação do android-debug-bridge-tool, que pode ser instalado pelo pacote "android-platform-tools" sendo a única dependência necessária para o ensaio. 

> Se o script "Config.sh" já foi rodado, não precisa rodar novamente.

1. Dentro da vsw-shell é necessário rodar o comando `adb` para verificar se o pacote foi devidamente instalado.
2. Realizar as configurações do ensaio, digitando o protocolo e orçamento da amostra.
3. O Comando tvbox inicia os ensaios e gera uma pasta com as informações coletadas, as mesmas serão utilizadas para a escrita do relatório. 

## Demonstração da VSW-SHELL

<img width="765" height="291" alt="DEMO-VSWS-SHELL" src="https://github.com/user-attachments/assets/7bb25a2c-2886-4b47-8f92-587df66d4d68" />

