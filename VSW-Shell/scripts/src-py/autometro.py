#!/usr/bin/env python3
import pyautogui  # type: ignore
import time
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich import box
from rich.text import Text
from rich.style import Style

# Configuração do rich
console = Console()


class AutoMetro:  # Implementando a classe Autômetro para lidar melhor com o código.
    def __init__(self):
        self.actions = None  # Variável que armazena as ações do usuário
        self.state_machine = {
            "1": self.gravar_acoes,
            "2": self.carregar_acoes,
            "3": self.repetir_acoes,
            "4": self.sair,
        }

    def gravar_acoes(self):
        self.actions = rec()
        save(self.actions)

    def carregar_acoes(self):
        filename = Prompt.ask("\nArquivo JSON", default="actions.json")
        self.actions = load(filename)

    def repetir_acoes(self):
        if self.actions:
            try:
                n = IntPrompt.ask("Quantas repetições?")
                rep(self.actions, n)
            except ValueError:
                console.print("Digite um número válido!", style="bold red")
        else:
            console.print(
                "Nenhuma ação carregada! Use opção 1 ou 2 primeiro.",
                style="bold yellow",
            )

    def sair(self):
        console.print("Saindo...", style="bold blue")
        exit()

    def run(self):
        while True:
            opt = menu_interativo()
            rodar = self.state_machine.get(
                opt, lambda: console.print("Opção inválida!", style="bold red")
            )
            rodar()


def rec():
    console.print(
        "Você tem 5 segundos para ir a tela do software de ensaio.", style="bold yellow"
    )
    time.sleep(5)
    # Registra ações do usuário (cliques do mouse ou pressionamentos de teclas).

    actions = []
    console.rule("[bold blue]Modo de Gravação[/]")
    console.print(
        "Clique onde deseja repetir a ação. Pressione 'Ctrl+C' para parar.",
        style="italic",
    )
    # Loop while.
    try:
        while True:
            # Tipo de ação.
            action_type = (
                Prompt.ask(
                    "O próximo clique é do [bold]teclado[/], [bold]mouse[/] ou [bold]texto[/]?",
                    choices=["k", "m", "m2", "t"],
                    show_choices=False,
                )
                .strip()
                .lower()
            )

            if action_type == "m":
                x, y = pyautogui.position()
                actions.append(("mouse", x, y))
                console.print(
                    f"Posição do clique registrada: [bold green]({x}, {y})[/]"
                )
            elif action_type == "m2":
                x, y = pyautogui.position()
                actions.append(("mouse2", x, y))
                console.print(
                    f"Posição do duplo clique registrada: [bold green]({x}, {y})[/]"
                )
            elif action_type == "k":
                key = Prompt.ask("Pressione a tecla desejada")
                if key in pyautogui.KEYBOARD_KEYS:
                    actions.append(("keyboard", key))
                    console.print(f"Tecla registrada: [bold green]{key}[/]")
                else:
                    console.print(
                        "Tecla inválida. Por favor, tente novamente.", style="bold red"
                    )
            elif action_type == "t":
                text = Prompt.ask("Digite o texto desejado")
                actions.append(("text", text))
                console.print(f"Texto registrado: [bold green]{text}[/]")

            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\nGravação de ações interrompida.", style="bold yellow")
    return actions


# Manipulação de Arquivos
def save(actions):
    nome_arquivo = Prompt.ask(
        "Digite o nome do software utilizado", default="actions.json"
    )
    # Salva as ações em um arquivo JSON.
    with open(nome_arquivo, "w") as file:  # modo escrita "w".
        json.dump(actions, file)
    console.print(
        f"\nAções salvas em [bold green]{nome_arquivo}[/].", style="bold green"
    )


# Manipulação de Arquivos
def load(filename="actions.json"):
    # Carrega as ações de um arquivo JSON.
    try:
        with open(filename, "r") as file:  # modo leitura "r".
            actions = json.load(file)
        console.print(
            f"\nAções carregadas de [bold green]{filename}[/].", style="bold green"
        )
        return actions
    except FileNotFoundError:
        console.print(
            f"\nArquivo [bold red]{filename}[/] não encontrado.", style="bold red"
        )
        return None
    except json.JSONDecodeError:
        console.print(
            f"\nArquivo [bold red]{filename}[/] corrompido.", style="bold red"
        )
        return None


def rep(actions, n):
    # Repete as ações registradas 'n' vezes.
    console.print(f"\nRepetindo ações [bold yellow]{n}[/] vezes...", style="bold blue")
    for i in range(n):
        console.print(f"\nRepetição [bold]{i + 1}[/] de [bold]{n}[/]", style="blue")
        for action in actions:
            if action[0] == "mouse":
                pyautogui.click(action[1], action[2])
                console.print(f"Clicando em [bold green]({action[1]}, {action[2]})[/]")
            elif action[0] == "mouse2":
                pyautogui.doubleClick(action[1], action[2])
                console.print(
                    f"Duplo clique em [bold green]({action[1]}, {action[2]})[/]"
                )
            elif action[0] == "keyboard":
                pyautogui.press(action[1])
                console.print(f"Pressionando tecla: [bold green]{action[1]}[/]")
            elif action[0] == "text":
                pyautogui.write(action[1])
                console.print(f"Digitando texto: [bold green]{action[1]}[/]")
            time.sleep(1)


def menu_interativo():
    # Exibe o menu interativo
    console.rule("[bold blue]AutoMetro[/]")

    table = Table(show_header=False, box=box.SIMPLE)
    table.add_column("Opção", style="cyan", width=10)
    table.add_column("Ação", style="magenta")

    table.add_row("1", "Gravar ações")
    table.add_row("2", "Carregar ações de um arquivo")
    table.add_row("3", "Repetir ações")
    table.add_row("4", "Sair")

    console.print(table)

    opt = Prompt.ask("Escolha uma opção", choices=["1", "2", "3", "4"])
    return opt


def main():
    autoMetro = AutoMetro()
    autoMetro.run()


if __name__ == "__main__":
    main()
