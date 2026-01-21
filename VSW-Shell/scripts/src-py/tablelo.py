#!/usr/bin/env python3
# |----|LABELO/VSW|----|@author:FelipeArnt|----|
# Tablelo - Script para extração de tabelas em arquivos PDF do laboratório de Verificação de Software do LABELO.

from tkinter import Tk, filedialog
import pdfplumber
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from typing import List, Optional, Tuple, Dict, Any
import time
import sys
import subprocess


def selecionar_arquivo() -> Optional[str]:
    root = Tk()
    root.withdraw()
    caminho = filedialog.askopenfilename(title="Selecione o arquivo", filetypes=[("PDF Files", "*.pdf")])
    root.destroy()
    return caminho if caminho else None

def instalar_requisitos(arquivo='requisitos.txt'):
    try:
        try:
            with open(arquivo, 'r') as f:
                pass
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado.")
            return False

        comando = [sys.executable, '-m', 'pip', 'install', '-r', arquivo]
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)

        if resultado.stdout:
            print(resultado.stdout)
        if resultado.stderr:
            print(resultado.stderr)

        print("\nPacotes do arquivo instalados com sucesso!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar requisitos:")
        print(e.stderr)
        return False
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {str(e)}")
        return False


def limpar_tabela(tabela: List[List[Any]]) -> Optional[List[List[str]]]:
    cleaned = [
        [str(cell).strip() for cell in linha if str(cell).strip()]
        for linha in tabela if any(str(cell).strip() for cell in linha)
    ]
    return cleaned or None


class Tablelo:
    def __init__(self):
        self.console = Console()
        self.tabelas: List[Dict[str, Any]] = []
        self.total_paginas: int = 0
        self.caminho_arquivo: Optional[str] = None

    def extrair_tabelas(self, caminho: str, paginas: Optional[List[int]] = None) -> None:
        start = time.time()
        try:
            with pdfplumber.open(caminho) as pdf:
                total = len(pdf.pages)
                self.total_paginas = total
                paginas = paginas or list(range(total))

                agrupadas, atual, cabecalho, pag_inicio = [], [], None, None

                for idx in paginas:
                    pagina = pdf.pages[idx]
                    for tab in pagina.extract_tables():
                        limpa = limpar_tabela(tab)
                        if not limpa: continue

                        cab, dados = limpa[0], limpa[1:]
                        if cab == cabecalho:
                            atual.extend(dados)
                        else:
                            if atual:
                                agrupadas.append({
                                    'cabecalho': cabecalho,
                                    'dados': atual,
                                    'pagina_inicial': pag_inicio,
                                    'pagina_final': idx
                                })
                            atual, cabecalho, pag_inicio = dados, cab, idx + 1

                if atual:
                    agrupadas.append({
                        'cabecalho': cabecalho,
                        'dados': atual,
                        'pagina_inicial': pag_inicio,
                        'pagina_final': paginas[-1] + 1
                    })

                self.tabelas = agrupadas
                self.console.print(f"[green]Extraídas {len(agrupadas)} tabelas em {time.time() - start:.2f}s[/green]")

        except Exception as e:
            self.console.print(f"[red]Erro ao processar PDF: {e}[/red]")

    def selecionar_paginas(self) -> Optional[List[int]]:
        if self.total_paginas <= 10:
            return None
        self.console.print(f"Documento com {self.total_paginas} páginas")
        entrada = Prompt.ask("Páginas (ex: 1,3-5) [Enter = todas]:", default="")
        if not entrada.strip(): return None
        try:
            paginas = set()
            for parte in entrada.split(','):
                if '-' in parte:
                    i, f = map(int, parte.split('-'))
                    paginas.update(range(i - 1, f))
                else:
                    paginas.add(int(parte) - 1)
            return sorted(paginas)
        except:
            self.console.print("[red]Formato inválido![/red]")
            return self.selecionar_paginas()

    def exibir_tabelas(self):
        for i, tabela in enumerate(self.tabelas):
            self.console.print(Panel.fit(
                f"Tabela {i+1} (Páginas {tabela['pagina_inicial']}-{tabela['pagina_final']})", style="blue"))
            table = Table(show_header=True, header_style="bold magenta")
            for h in tabela['cabecalho']:
                table.add_column(h)
            for linha in tabela['dados'][:3]:
                table.add_row(*[str(c)[:50] + ('...' if len(str(c)) > 50 else '') for c in linha])
            if len(tabela['dados']) > 3:
                table.add_row(*['...' for _ in tabela['cabecalho']])
            self.console.print(table)
            self.console.print(f"Total de linhas: {len(tabela['dados'])}\n")

    def remover_linhas(self):
        if not self.tabelas:
            self.console.print("[red]Nenhuma tabela carregada![/red]")
            return

        self.console.print(Panel.fit("Método de Remoção", style="yellow"))
        metodo = Prompt.ask("1. Por índices  2. Por palavra-chave  0. Cancelar", choices=["0", "1", "2"])

        if metodo == "0":
            return

        elif metodo == "1":
            self.exibir_tabelas_para_selecao()
            entrada = Prompt.ask("Índices das linhas a remover (ex: 1,3-5):", default="")
            if not entrada: return

            try:
                indices = set()
                for p in entrada.split(','):
                    if '-' in p:
                        i, f = map(int, p.split('-'))
                        indices.update(range(i - 1, f))
                    else:
                        indices.add(int(p) - 1)

                total_removidas = 0
                for tabela in self.tabelas:
                    original = len(tabela['dados'])
                    tabela['dados'] = [l for i, l in enumerate(tabela['dados']) if i not in indices]
                    total_removidas += original - len(tabela['dados'])

                self.console.print(f"[green]{total_removidas} linha(s) removida(s)[/green]")
            except:
                self.console.print("[red]Formato inválido![/red]")

        elif metodo == "2":
            palavras = Prompt.ask("Palavras-chave para remover linhas (separadas por vírgula):", 
                                 default="exemplo,teste,placeholder")
            if not palavras.strip():
                return

            palavras_lista = [p.strip().lower() for p in palavras.split(',') if p.strip()]
            case_sensitive = Prompt.ask("Case sensitive? (s/n)", choices=["s", "n"], default="n") == "s"

            total_removidas = 0
            for tabela in self.tabelas:
                original = len(tabela['dados'])
                novos_dados = []

                for linha in tabela['dados']:
                    linha_texto = " ".join(str(c) for c in linha)
                    if not case_sensitive:
                        linha_texto = linha_texto.lower()

                    encontrou = any(
                        (p if case_sensitive else p.lower()) in linha_texto 
                        for p in palavras_lista
                    )

                    if not encontrou:
                        novos_dados.append(linha)

                tabela['dados'] = novos_dados
                total_removidas += original - len(tabela['dados'])

            self.console.print(f"[green]{total_removidas} linha(s) removida(s) contendo as palavras-chave[/green]")

    def exibir_tabelas_para_selecao(self):
        for i, tabela in enumerate(self.tabelas):
            self.console.print(Panel.fit(
                f"Tabela {i+1} (Páginas {tabela['pagina_inicial']}-{tabela['pagina_final']})", style="blue"))
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Índice")
            for h in tabela['cabecalho']:
                table.add_column(h)
            for j, linha in enumerate(tabela['dados'][:5]):
                table.add_row(str(j+1), *[str(x) for x in linha])
            if len(tabela['dados']) > 5:
                table.add_row("...", *["" for _ in range(len(tabela['cabecalho']))])
            self.console.print(table)

    def filtrar_por_palavras(self):
        palavras = Prompt.ask("Palavras-chave para excluir tabelas (vírgulas):", 
                             default="marca d'água,assinatura,copyright,revisado,revisão")
        palavras = [p.strip().lower() for p in palavras.split(',') if p.strip()]
        case_sensitive = Prompt.ask("Case sensitive? (s/n)", choices=["s", "n"], default="n") == "s"

        filtradas = []
        removidas = 0

        for t in self.tabelas:
            texto = " ".join([" ".join(t['cabecalho'])] + [" ".join(map(str, l)) for l in t['dados']])
            if not case_sensitive:
                texto = texto.lower()

            encontrou = any(
                (p if case_sensitive else p.lower()) in texto 
                for p in palavras
            )

            if encontrou:
                removidas += 1
            else:
                filtradas.append(t)

        self.tabelas = filtradas
        self.console.print(f"[green]{removidas} tabela(s) removida(s)[/green]")

    def exportar_markdown(self):
        if not self.tabelas:
            self.console.print("[red]Nenhuma tabela carregada![/red]")
            return

        nome_base = self.caminho_arquivo.rsplit("/", 1)[-1].rsplit(".", 1)[0] if self.caminho_arquivo else "casos_teste"
        nome_arquivo = Prompt.ask("Nome do arquivo Markdown", default=f"{nome_base}.md")

        try:
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write("<table>\n")
                f.write("<tr>\n")
                f.write("    <th>Caso de teste</th>\n")
                f.write("    <th>Objetivo</th>\n")
                f.write("    <th>Resultados</th>\n")
                f.write("</tr>\n\n")
                
                for i, tabela in enumerate(self.tabelas):
                    # Extrair informações da tabela
                    caso_teste = ""
                    objetivo = ""
                    resultados = ""
                    
                    # Tenta obter o caso de teste do cabeçalho
                    if tabela['cabecalho']:
                        caso_teste = tabela['cabecalho'][0].split("–")[-1].strip()
                    
                    # Procura pelas informações nas linhas da tabela
                    for linha in tabela['dados']:
                        if len(linha) >= 2:
                            chave = str(linha[0]).strip().lower()
                            valor = str(linha[1]).strip()
                            
                            if "caso de teste" in chave:
                                caso_teste = valor
                            elif "objetivo" in chave:
                                objetivo = valor
                            elif "resultados obtidos" in chave:
                                resultados = valor
                    
                    # Se não encontrou caso de teste, usa o título da tabela
                    if not caso_teste:
                        caso_teste = tabela['cabecalho'][0] if tabela['cabecalho'] else f"Tabela {i+1}"
                    
                    # Se não encontrou resultados, tenta a última coluna da primeira linha
                    if not resultados and tabela['dados']:
                        if len(tabela['dados'][0]) > 1:
                            resultados = str(tabela['dados'][0][-1])
                    
                    # Escreve a linha da tabela
                    f.write("<tr>\n")
                    f.write(f"    <td>{caso_teste}</td>\n")
                    f.write(f"    <td>{objetivo or 'Não especificado'}</td>\n")
                    f.write(f"    <td>{resultados or 'Não especificado'}</td>\n")
                    f.write("</tr>\n\n")
                
                f.write("</table>")
                self.console.print(f"[green]Arquivo salvo como {nome_arquivo}[/green]")
        except Exception as e:
            self.console.print(f"[red]Erro ao salvar arquivo: {e}[/red]")

    def carregar(self):
        caminho = selecionar_arquivo()
        if not caminho:
            return False
        self.caminho_arquivo = caminho
        paginas = self.selecionar_paginas()
        self.extrair_tabelas(caminho, paginas)
        return bool(self.tabelas)

    def executar(self):
        self.console.print(Panel.fit("Tablelo - Extrator Turbo PDF", style="bold blue"))
        if not self.carregar():
            return
        while True:
            self.console.print(Panel.fit("Menu Principal", style="bold cyan"))
            op = Prompt.ask(
                "1. Novo arquivo\n"
                "2. Visualizar tabelas\n"
                "3. Remover linhas\n"
                "4. Filtrar tabelas\n"
                "5. Exportar Markdown\n"
                "0. Sair\n\n"
                "Selecione uma opção:",
                choices=["0", "1", "2", "3", "4", "5"]
            )
            if op == "0":
                self.console.print("[green]Até logo[/green]")
                break
            elif op == "1":
                self.carregar()
            elif op == "2":
                self.exibir_tabelas()
            elif op == "3":
                self.remover_linhas()
            elif op == "4":
                self.filtrar_por_palavras()
            elif op == "5":
                self.exportar_markdown()


if __name__ == "__main__":
    try:
        instalar_requisitos()
        app = Tablelo()
        app.executar()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"Erro fatal: {str(e)}", file=sys.stderr)
        sys.exit(1)

