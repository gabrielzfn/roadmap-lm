import difflib
import sys
import time
import os
from collections import Counter
import tkinter as tk
from tkinter import filedialog

# PDFPLUMBER é responsável pela extração e análise dos docs, o script não funciona sem essa lib.
try:
    import pdfplumber
    PDF_SUPPORT = True
except ImportError:
    print("Aviso: pdfplumber não está instalado. Instale com: pip install pdfplumber")
    PDF_SUPPORT = False

def escolher_arquivos():
    root = tk.Tk()
    root.withdraw()
    arquivo1 = filedialog.askopenfilename(
        title="Selecione o primeiro arquivo (PDF ou TXT)", 
        filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")]
    )
    if not arquivo1:
        print("Nenhum arquivo selecionado.")
        return None, None, None
    
    arquivo2 = filedialog.askopenfilename(
        title="Selecione o segundo arquivo (PDF ou TXT)", 
        filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")]
    )
    if not arquivo2:
        print("Nenhum segundo arquivo selecionado.")
        return None, None, None
    
    arquivo_saida = filedialog.asksaveasfilename(
        title="Salvar relatório como", 
        defaultextension=".txt", 
        filetypes=[("Text files", "*.txt")]
    )
    if not arquivo_saida:
        print("Nenhum arquivo de saída selecionado.")
        return None, None, None
    
    return arquivo1, arquivo2, arquivo_saida

def extrair_linhas(caminho_arquivo):
    """Extrai linhas de um arquivo PDF ou TXT"""
    if caminho_arquivo.lower().endswith('.pdf'):
        if not PDF_SUPPORT:
            raise ImportError("pdfplumber não está instalado. Não é possível processar PDFs.")
        
        linhas = []
        try:
            with pdfplumber.open(caminho_arquivo) as pdf:
                for pagina in pdf.pages:
                    texto = pagina.extract_text()
                    if texto:
                        # Divide o texto em linhas e adiciona informação da página
                        linhas_pagina = texto.splitlines()
                        for i, linha in enumerate(linhas_pagina):
                            if linha.strip():  # Apenas linhas não vazias
                                linhas.append(f"[Página {pagina.page_number}] {linha}")
            
            if not linhas:
                print(f"Aviso: Nenhum texto extraído do PDF {caminho_arquivo}")
                
        except Exception as e:
            print(f"Erro ao processar PDF {caminho_arquivo}: {e}")
            return []
            
        return linhas
    
    else:  # Arquivo de texto
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                return f.read().splitlines()
        except UnicodeDecodeError:
            # Tenta com outra codificação se UTF-8 falhar
            with open(caminho_arquivo, 'r', encoding='latin-1') as f:
                return f.read().splitlines()

def relatar_diferencas(saida, padroes_diferencas, diferencas_repetidas, diferencas_por_secao, 
                      qtd_linhas1, qtd_linhas2, arquivo1, arquivo2):
    if len(padroes_diferencas) == 1:
        saida.write("\n=== ALTERAÇÃO GLOBAL DETECTADA ===\n")
        saida.write("O mesmo padrão de diferença aparece em todo o arquivo:\n")
        for linha in next(iter(padroes_diferencas)):
            saida.write(f"{linha}\n")
    else:
        saida.write("\n=== DIFERENÇAS MAIS FREQUENTES ===\n")
        for diff, contagem in diferencas_repetidas.most_common():
            saida.write(f"[{contagem:03d}x] {diff}\n")
        
        if diferencas_por_secao:
            saida.write("\n=== DIFERENÇAS ESPECÍFICAS POR SEÇÃO ===\n")
            for secao, padrao in diferencas_por_secao:
                saida.write(f"\n--- Seção {secao} ---\n")
                for linha in padrao:
                    saida.write(f"{linha}\n")
    
    if qtd_linhas1 > qtd_linhas2:
        saida.write(f"\n--- Linhas extras em {arquivo1} ---\n")
        saida.write(f"Linhas {qtd_linhas2+1} até {qtd_linhas1} só existem no primeiro arquivo.\n")
    elif qtd_linhas2 > qtd_linhas1:
        saida.write(f"\n--- Linhas extras em {arquivo2} ---\n")
        saida.write(f"Linhas {qtd_linhas1+1} até {qtd_linhas2} só existem no segundo arquivo.\n")

def comparar_arquivos(arquivo1, arquivo2, arquivo_saida):
    inicio_execucao = time.time()
    
    print(f"Extraindo texto de: {arquivo1}")
    linhas_arq1 = extrair_linhas(arquivo1)
    
    print(f"Extraindo texto de: {arquivo2}")
    linhas_arq2 = extrair_linhas(arquivo2)
    
    qtd_linhas1, qtd_linhas2 = len(linhas_arq1), len(linhas_arq2)
    linhas_para_comparar = min(qtd_linhas1, qtd_linhas2)
    
    diferencas_repetidas = Counter()
    padroes_diferencas = set()
    diferencas_por_secao = []
    houve_diferenca = False
    
    # Compara linha por linha
    if linhas_arq1 != linhas_arq2:
        houve_diferenca = True
        diferencas = list(difflib.Differ().compare(linhas_arq1, linhas_arq2))
        diferencas_secao = [linha for linha in diferencas if linha.startswith(('-', '+'))]
        diferencas_repetidas.update(diferencas_secao)
        
        if diferencas_secao:
            chave_padrao = tuple(diferencas_secao)
            padroes_diferencas.add(chave_padrao)
            diferencas_por_secao.append((1, chave_padrao))  # Seção única
    
    with open(arquivo_saida, "w", encoding="utf-8") as saida:
        saida.write("=== RELATÓRIO DE COMPARAÇÃO DE ARQUIVOS ===\n")
        saida.write(f"Arquivo 1: {arquivo1} ({qtd_linhas1} linhas)\n")
        saida.write(f"Arquivo 2: {arquivo2} ({qtd_linhas2} linhas)\n")
        saida.write(f"Tipo 1: {'PDF' if arquivo1.lower().endswith('.pdf') else 'TXT'}\n")
        saida.write(f"Tipo 2: {'PDF' if arquivo2.lower().endswith('.pdf') else 'TXT'}\n\n")
        
        if qtd_linhas1 != qtd_linhas2:
            saida.write(f"ATENÇÃO: Quantidade de linhas diferente ({qtd_linhas1} vs {qtd_linhas2})\n\n")
        
        if not houve_diferenca:
            saida.write("\nNenhuma diferença de conteúdo encontrada!")
        else:
            relatar_diferencas(saida, padroes_diferencas, diferencas_repetidas, diferencas_por_secao,
                               qtd_linhas1, qtd_linhas2, arquivo1, arquivo2)
    
    tempo_execucao = time.time() - inicio_execucao
    print("\nComparação concluída:")
    print(f"- Linhas analisadas: {linhas_para_comparar}")
    print(f"- Padrões de diferença únicos: {len(padroes_diferencas)}")
    print(f"- Tempo de execução: {tempo_execucao:.2f} segundos")
    print(f"Relatório gerado em: {arquivo_saida}")

def comparar_diretorios(dir1, dir2, dir_saida):
    if not os.path.exists(dir_saida):
        os.makedirs(dir_saida)
    
    # Procura por arquivos PDF e TXT
    arquivos_dir1 = {f for f in os.listdir(dir1) if f.lower().endswith(('.pdf', '.txt'))}
    arquivos_dir2 = {f for f in os.listdir(dir2) if f.lower().endswith(('.pdf', '.txt'))}
    
    comuns = arquivos_dir1 & arquivos_dir2
    if not comuns:
        print("Nenhum arquivo PDF ou TXT em comum encontrado entre os diretórios.")
        return
    
    for nome_arquivo in comuns:
        caminho1 = os.path.join(dir1, nome_arquivo)
        caminho2 = os.path.join(dir2, nome_arquivo)
        caminho_saida = os.path.join(dir_saida, f"{os.path.splitext(nome_arquivo)[0]}_comparacao.txt")
        print(f"\n=== Comparando: {nome_arquivo} ===")
        comparar_arquivos(caminho1, caminho2, caminho_saida)

def main():
    if len(sys.argv) == 1:
        # Modo interface gráfica
        print("Modo interface gráfica selecionado...")
        arquivo1, arquivo2, arquivo_saida = escolher_arquivos()
        if arquivo1 and arquivo2 and arquivo_saida:
            comparar_arquivos(arquivo1, arquivo2, arquivo_saida)
        else:
            print("Operação cancelada.")
    
    elif len(sys.argv) == 4:
        # Modo linha de comando
        entrada1, entrada2, saida = sys.argv[1], sys.argv[2], sys.argv[3]
        
        if os.path.isdir(entrada1) and os.path.isdir(entrada2):
            comparar_diretorios(entrada1, entrada2, saida)
        elif os.path.isfile(entrada1) and os.path.isfile(entrada2):
            comparar_arquivos(entrada1, entrada2, saida)
        else:
            print("Erro: os dois primeiros argumentos devem ser ambos arquivos ou ambos diretórios.")
    
    else:
        print("Uso:")
        print("  python pdf_differ.py")
        print("  python pdf_differ.py arquivo1.pdf arquivo2.pdf saida.txt")
        print("  python pdf_differ.py arquivo1.txt arquivo2.txt saida.txt")
        print("  python pdf_differ.py dir1 dir2 dir_saida")
        sys.exit(1)

if __name__ == "__main__":
    main()
