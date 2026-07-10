Você converterá slides existentes latex para quarto.

Use aulas/aula1-intro.qmd e aula27-cobertura-emparelhamento.qmd como exemplo.

O slide título apenas copie da aula1, alterando só o título da aula.

Não altere o conteúdo, e não deixe nenhum slide para trás.

Para pseudocódigos, use exatamente o estilo de pseudocódigo da aula1-intro.qmd com 
#| html-line-number: true
#| html-no-end: true

Todo pseucódigo deve começar com \Procedure com o nome da função e entradas, tal qual o exemplo em aula1-intro.qmd.

Para comando textbf ou \bemph, use **asteriscos duplos**

Para teoremas, observações, etc, use ">" e os .label-thm, .label-rmk, etc. em metropolis.scss

Confira se os caminhos das imagens estão corretos. Todas as imagens estão em aulas/images ou aulas/fig.

Toda aula deve terminar exatamente com:

#

::: {style="text-align: center; margin-top: 15vh;"}
[?]{style="font-size: 5em; color: #d10000; font-weight: 700;"}
:::

