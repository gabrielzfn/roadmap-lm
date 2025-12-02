# Simulador de envios de dados para medidores

- Mudar permissões de execução dos scripts "run" e "clean" 
  - `chmod +x run.sh clean.sh`
  - run.sh abre a porta de comunicação serial ficticía.
  - clean.sh fecha a porta de comunicação serial ficticía.

- Rodar arquivo "medidor_simulado.py"
  - `python3 medidor_simulado.py`
  - Inicia o medidor e aguarda os comandos enviados pelo script "sender.py"

- Rodar arquivo "sender.py"
  - `python3 sender.py`
  - Inicia o sender de comandos ficticíos para o medidor simulado.

### Setup utilizado para testes

Para testar o simulador é fundamental utilizar o emulador de terminal "tmux" no wsl ou wsl2 e socat para a criação da comunicação serial ficticía.

- Após a instalação do tmux e do wsl2, temos alguns atalhos importantes para dividir as sessões do terminal na mesma janela, os mesmos podem ser visualizados abaixo:
  - `tmux` é o comando utilizado para iniciar o emulador;
  - `ctrl + b` + `%` é o comando utilizado para splitar a tela verticalmente;
  - `ctrl + b` + `"` é o comando utilizado para splitar a tela horizontalmente.
  > para navegar entre as sessões, utilize `ctrl + b` + `right arrow` ou a direção da sessão que você quer ir`


