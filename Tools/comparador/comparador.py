#!/usr/bin/env Python3
# |----|LABELO/VSW|----|@author:FelipeArnt|----|

import os
import sys
from filecmp import dircmp
from typing import Optional, Dict, Any, List
from tkinter import Tk, filedialog
import time

# Função que peguei do script TABLELO.
def selecionar_pasta(titulo: str) -> Optional[str]:
    root = Tk()
    root.withdraw()
    caminho = filedialog.askdirectory(title=titulo)
    root.update()
    root.destroy()
    return caminho if caminho else None
# Comparador do diretorio e subdiretorios
def comparar_pastas(pasta1: str, pasta2: str) -> Dict[str, Any]:
    inicio = time.time()
    
    dcmp = dircmp(pasta1, pasta2)
    resultados = {
        'modificados': dcmp.diff_files,
        'apenas_na_pasta1': dcmp.left_only,
        'apenas_na_pasta2': dcmp.right_only,
        'subdiretorios': {}
    }
    # Compara subdiretórios recursivamente
    for subdir_nome, subdir_dcmp in dcmp.subdirs.items():
        caminho_sub1 = os.path.join(pasta1, subdir_nome)
        caminho_sub2 = os.path.join(pasta2, subdir_nome)
        resultados['subdiretorios'][subdir_nome] = comparar_pastas(caminho_sub1, caminho_sub2)
    
    tempo_exec = time.time() - inicio
    print(f"Comparação concluída em {tempo_exec:.2f} segundos")
    return resultados
# Formata os resultados pra printar
def formatar_resultados(resultados: dict, nivel: int = 0) -> str:
    indent = "  " * nivel
    output: List[str] = []
    
    if resultados['modificados']:
        output.append(f"{indent}[MODIFICADOS]:")
        for arquivo in resultados['modificados']:
            output.append(f"{indent}  - {arquivo}")
        output.append("")
    
    if resultados['apenas_na_pasta1']:
        output.append(f"{indent}[REMOVIDOS]:")
        for arquivo in resultados['apenas_na_pasta1']:
            output.append(f"{indent}  - {arquivo}")
        output.append("")
    
    if resultados['apenas_na_pasta2']:
        output.append(f"{indent}[ADICIONADOS]:")
        for arquivo in resultados['apenas_na_pasta2']:
            output.append(f"{indent}  - {arquivo}")
        output.append("")
    
    # Subdiretórios / Subpastas
    for subdir_nome, subresult in resultados['subdiretorios'].items():
        sub_output = formatar_resultados(subresult, nivel + 1)
        if sub_output.strip():
            output.append(f"{indent}Subdiretório: {subdir_nome}")
            output.append(sub_output)
    
    return "\n".join(output)

def main():
    # Seleção das pastas
    pasta1 = selecionar_pasta("Selecione o PACOTE ANTIGO")    
    if not pasta1:
        sys.exit("Nenhuma pasta selecionada!")
    pasta2 = selecionar_pasta("Selecione o PACOTE ATUALIZADO")
    if not pasta2:
        sys.exit("Nenhuma pasta selecionada!")
    
    # pastas existem
    if not os.path.isdir(pasta1) or not os.path.isdir(pasta2):
        sys.exit("Uma ou ambas as pastas não existem!")
    
    print("\n" + "=" * 80)
    print(f"Comparando pastas:\n- Primeiro pacote: {pasta1}\n- Pacote Atualizado: {pasta2}")
    print("=" * 80 + "\n")
    
    # comparação
    try:
        resultados = comparar_pastas(pasta1, pasta2)
    except PermissionError:
        sys.exit("Erro de permissão ao acessar os arquivos!")
    
    # Verifica alterações
    alteracoes = (
        resultados['modificados'] or
        resultados['apenas_na_pasta1'] or
        resultados['apenas_na_pasta2'] or
        any(
            sub['modificados'] or 
            sub['apenas_na_pasta1'] or 
            sub['apenas_na_pasta2'] 
            for sub in resultados['subdiretorios'].values()
        )
    )
    # Formata resultado
    relatorio = (
        "ALTERAÇÕES ENCONTRADAS:\n\n" + 
        formatar_resultados(resultados) 
        if alteracoes else 
        "NENHUMA ALTERAÇÃO ENCONTRADA"
    )
           # Adicionar ao final de main()
    salvar = input("Salvar relatório em arquivo? (s/n): ").lower()
    if salvar == 's':
           with open("relatorio_comparacao.txt", "w") as f:
               f.write(relatorio)
           print("Relatório salvo em 'relatorio_comparacao.txt'")
    # Exibe resultados
    print("\n" + "=" * 80)
    print(relatorio)
    print("=" * 80)
    
if __name__ == "__main__":
    main()
