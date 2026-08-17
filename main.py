"""Ponto de entrada. Rode com: python3 main.py

Este arquivo garante que a propria pasta onde ele esta (a raiz do projeto)
seja adicionada ao sys.path, para que o pacote "nave" seja encontrado mesmo
que o script seja executado de outro diretorio de trabalho (ex.: chamado
por um atalho, por outra pasta no terminal, ou por um IDE configurado com
um "working directory" diferente).
"""

import os
import sys

# Garante que a pasta que contem este arquivo (e, portanto, a pasta "nave")
# esteja no caminho de busca de modulos do Python.
_DIRETORIO_DO_PROJETO = os.path.dirname(os.path.abspath(__file__))
if _DIRETORIO_DO_PROJETO not in sys.path:
    sys.path.insert(0, _DIRETORIO_DO_PROJETO)

from nave.cli import main

if __name__ == "__main__":
    main()
