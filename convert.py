import re

with open('aulas-projeto-e-analise-de-algoritmos/aula02.tex', 'r') as f:
    lines = f.readlines()

out = []
in_doc = False
in_itemize = False
itemize_incremental = False
in_table = False
table_content = []

header = """---
title: "Projeto e Análise de Algoritmos I"
subtitle: "Aula 02: Emparelhamento Estável"
author: "Lucas Nunes Alegre"
institute: |
  Universidade Federal do Rio Grande do Sul  <br>
  Instituto de Informática <br> Departamento de Informática Teórica  
  <br><br><br>
  <span style="display:inline-block; max-width:60%; font-size:0.55em;">Estes slides utilizam conteúdo adaptado da bibliografia da disciplina e também de notas de aula e slides prévios dos professores Bruno Grisci, Rodrigo Machado, André Grahl Pereira, Lucas Nunes Alegre, Marcus Ritt e Luciana Buriol.</span>
date: ""
lang: pt-BR

format:
  revealjs:
    theme: [default, metropolis.scss]
    slide-number: true
    progress: true
    transition: fade
    width: 1024
    height: 768
    margin: 0.15
    html-math-method: katex
    title-slide-attributes:
      data-background-color: "#ffffff"
    center: false
    highlight-style: github
    fig-align: center
    embed-resources: false
    preview-links: true
    include-in-header:
      - pseudocode-reveal.html
    chalkboard:
      theme: whiteboard
      boardmarker-width: 5
      buttons: false

filters:
  - leovan/pseudocode
---
"""
out.append(header)

i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    if stripped == r'\begin{document}':
        in_doc = True
        i += 1
        continue
    if not in_doc:
        i += 1
        continue
    if stripped == r'\end{document}':
        break
        
    if stripped == r'\maketitle' or stripped == r'% TODO: Refazer Karatsuba com base nos slides de Complexidade':
        i += 1
        continue
        
    if stripped.startswith(r'\section{'):
        title = re.search(r'\\section\{(.*?)\}', stripped).group(1)
        out.append(f"\n# {title}\n")
        i += 1
        continue
        
    if stripped.startswith(r'\begin{frame}'):
        title_match = re.search(r'\\begin\{frame\}(?:\[.*?\])?\{(.*?)\}', line)
        if title_match:
            title = title_match.group(1)
            out.append(f"\n## {title}\n")
        else:
            out.append(f"\n## \n")
        i += 1
        continue
        
    if stripped == r'\end{frame}':
        out.append("\n")
        i += 1
        continue
        
    if stripped.startswith(r'\begin{itemize}'):
        if r'[<+->]' in stripped:
            out.append("::: {.incremental}\n")
            itemize_incremental = True
        else:
            itemize_incremental = False
        in_itemize = True
        i += 1
        continue
        
    if stripped.startswith(r'\end{itemize}'):
        if itemize_incremental:
            out.append(":::\n")
        in_itemize = False
        itemize_incremental = False
        i += 1
        continue
        
    if stripped.startswith(r'\item'):
        # Fix \item being in the middle of line? Usually it's at start.
        content = line.replace(r'\item', '-', 1)
        # handle color embedded
        content = re.sub(r'\{\\color\{.*?\} (.*?)\}', r'\1', content)
        content = re.sub(r'\{\\color\{.*?\}(.*?)\}', r'\1', content)
        content = re.sub(r'\\emph\{(.*?)\}', r'*\1*', content)
        content = re.sub(r'\\alert\{(.*?)\}', r'**\1**', content)
        content = re.sub(r'\\bemph\{(.*?)\}', r'**\1**', content)
        content = re.sub(r'\\cemph\[.*?\]\{(.*?)\}', r'**\1**', content)
        out.append(content)
        i += 1
        continue
        
    if stripped.startswith(r'\begin{algorithm}'):
        alg_content = []
        alg_content.append("```pseudocode")
        alg_content.append('#| label: alg-gale-shapley')
        alg_content.append('#| html-indent-size: "1.2em"')
        alg_content.append('#| html-comment-delimiter: "//"')
        alg_content.append('#| html-line-number: true')
        alg_content.append('#| html-line-number-punc: ":"')
        alg_content.append('#| html-no-end: false')
        
        while not lines[i].strip().startswith(r'\end{algorithm}'):
            if lines[i].strip() == r'\small':
                i += 1
                continue
            alg_content.append(lines[i].rstrip())
            i += 1
        alg_content.append(r'\end{algorithm}')
        alg_content.append("```")
        out.append('\n'.join(alg_content) + '\n')
        i += 1
        continue
        
    if stripped.startswith(r'\includepdf'):
        match = re.search(r'\{(.*?)\}', stripped)
        if match:
            pdf_name = match.group(1)
            out.append(f"\n<iframe src=\"{pdf_name}\" width=\"100%\" height=\"600px\"></iframe>\n")
        i += 1
        continue
        
    if stripped.startswith(r'\begin{tikzpicture}'):
        tikz_content = []
        tikz_content.append("```latex")
        while not lines[i].strip().startswith(r'\end{tikzpicture}'):
            tikz_content.append(lines[i].rstrip())
            i += 1
        tikz_content.append(r'\end{tikzpicture}')
        tikz_content.append("```")
        out.append('\n'.join(tikz_content) + '\n')
        i += 1
        continue
        
    if stripped.startswith(r'\begin{figure}') or stripped.startswith(r'\end{figure}'):
        i += 1
        continue
    if stripped.startswith(r'\includegraphics'):
        match = re.search(r'\\includegraphics(?:\[.*?\])?\{(.*?)\}', line)
        if match:
            out.append(f"![](images/{match.group(1)}.png){{width=60%}}\n")
        i += 1
        continue
        
    if stripped.startswith(r'\begin{minipage}') or stripped.startswith(r'\end{minipage}'):
        i += 1
        continue
        
    if stripped.startswith(r'\begin{tabular}'):
        in_table = True
        i += 1
        continue
        
    if stripped.startswith(r'\end{tabular}'):
        in_table = False
        i += 1
        continue
        
    if stripped.startswith(r'\begin{table}') or stripped.startswith(r'\end{table}'):
        i += 1
        continue
        
    if in_table:
        if stripped.startswith(r'\toprule') or stripped.startswith(r'\bottomrule') or stripped.startswith(r'\midrule'):
            i += 1
            continue
        # Table row
        row = stripped.replace(r'\\', '').strip()
        cols = row.split('&')
        if len(cols) > 1:
            out.append("| " + " | ".join(c.strip() for c in cols) + " |\n")
        i += 1
        continue
        
    line = line.replace(r'\pause', '. . .')
    line = re.sub(r'\\emph\{(.*?)\}', r'*\1*', line)
    line = re.sub(r'\\alert\{(.*?)\}', r'**\1**', line)
    line = re.sub(r'\\bemph\{(.*?)\}', r'**\1**', line)
    line = re.sub(r'\\cemph\[.*?\]\{(.*?)\}', r'**\1**', line)
    line = re.sub(r'\{\\color\{.*?\} (.*?)\}', r'\1', line)
    line = re.sub(r'\{\\color\{.*?\}(.*?)\}', r'\1', line)
    line = line.replace(r'\QED', '$\\blacksquare$')
    line = line.replace(r'\quad', ' ')
    line = line.replace(r'\,', ' ')
    line = line.replace(r'\;', ' ')
    line = line.replace(r'\ ', ' ')
    line = line.replace(r'\noindent', '')
    line = line.replace(r'\medskip', '')
    line = line.replace(r'\vspace{5pt}', '')
    line = line.replace(r'\centering', '')
    line = line.replace(r'\raggedright', '')
    line = line.replace(r'\\', '\n')
    line = line.replace(r'\small', '')
    line = line.replace(r'\Huge', '')
    line = line.replace(r'\caption', '')
    
    out.append(line)
    i += 1

with open('aulas/aula2-gale-shapley.md', 'w') as f:
    f.writelines(out)
