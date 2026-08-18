"""
Camada puramente visual do terminal: cores ANSI, caixas com borda e o menu de
ajuda formatado. Nao contem nenhuma regra de negocio -- so formata texto para
exibicao. Fica separado para que cli.py continue tratando apenas de
orquestrar comandos, e para que a "casca" visual possa ser trocada (ou
desligada) sem mexer em nenhum outro modulo.
"""

from __future__ import annotations

import os
import sys


# ----------------------------------------------------------------------
# Suporte a cores ANSI (funciona no Windows Terminal, PowerShell moderno,
# VS Code, Linux e macOS). No cmd.exe antigo o truque abaixo liga o
# processamento de sequencias ANSI; se algo nao suportar mesmo assim, as
# cores sao desativadas automaticamente e o programa continua funcionando
# normalmente, so que sem cor.
# ----------------------------------------------------------------------

def _cores_suportadas() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        try:
            os.system("")  # habilita processamento de sequencias VT no cmd/PowerShell
        except Exception:
            return False
    return True


_ANSI_ATIVO = _cores_suportadas()


class Cor:
    RESET = "\033[0m" if _ANSI_ATIVO else ""
    NEGRITO = "\033[1m" if _ANSI_ATIVO else ""
    CIANO = "\033[96m" if _ANSI_ATIVO else ""
    VERDE = "\033[92m" if _ANSI_ATIVO else ""
    AMARELO = "\033[93m" if _ANSI_ATIVO else ""
    VERMELHO = "\033[91m" if _ANSI_ATIVO else ""
    MAGENTA = "\033[95m" if _ANSI_ATIVO else ""
    AZUL = "\033[94m" if _ANSI_ATIVO else ""
    CINZA = "\033[90m" if _ANSI_ATIVO else ""


def colorir(texto: str, cor: str) -> str:
    if not cor:
        return texto
    return f"{cor}{texto}{Cor.RESET}"


LARGURA_PADRAO = 64


def linha_caixa(caractere_esquerda: str, caractere_meio: str, caractere_direita: str, largura: int = LARGURA_PADRAO) -> str:
    return caractere_esquerda + caractere_meio * (largura - 2) + caractere_direita


def caixa_titulo(titulo: str, cor: str = Cor.CIANO, largura: int = LARGURA_PADRAO) -> str:
    topo = colorir(linha_caixa("╔", "═", "╗", largura), cor)
    meio = colorir("║", cor) + titulo.center(largura - 2) + colorir("║", cor)
    base = colorir(linha_caixa("╚", "═", "╝", largura), cor)
    return f"{topo}\n{meio}\n{base}"


def separador(largura: int = LARGURA_PADRAO, cor: str = Cor.CINZA) -> str:
    return colorir("─" * largura, cor)


def imprimir_banner() -> None:
    print()
    print(caixa_titulo(" SISTEMAS DA NAVE — PAINEL DE CONTROLE ", cor=Cor.CIANO))
    print(colorir("Digite 'ajuda' a qualquer momento para ver os comandos.", Cor.CINZA))
    print()


SECOES_AJUDA = [
    (
        "NUCLEO DE ENERGIA",
        Cor.VERMELHO,
        [
            ("tomar_dano <valor>", "aplica dano ao nucleo de energia"),
            ("reduzir_energia <valor>", "reduz energia manualmente"),
            ("recarregar <valor>", "recarrega energia do nucleo"),
            ("suporte_vida_on", "ativa o Suporte de Vida como sistema reativo"),
        ],
    ),
    (
        "TRIPULACAO",
        Cor.VERDE,
        [
            ("add_tripulante <id> <funcao>", "cria tripulante (canhoes, motor, suporte_vida, piloto)"),
            ("trocar_funcao <id> <funcao>", "troca a funcao do tripulante em tempo real"),
            ("trabalhar <id>", "tripulante executa a tarefa da funcao atual"),
        ],
    ),
    (
        "ARMAMENTO",
        Cor.AMARELO,
        [
            ("equipar_arma <tipo>", "equipa arma base (laser, misseis)"),
            ("adicionar_modificador <tipo>", "empilha modificador (fogo, perfuracao, tiro_duplo)"),
            ("atirar", "dispara com a configuracao atual"),
        ],
    ),
    (
        "GERAL",
        Cor.AZUL,
        [
            ("status", "mostra o estado atual da nave"),
            ("ajuda", "mostra este menu novamente"),
            ("sair", "encerra o programa"),
        ],
    ),
]


def imprimir_ajuda() -> None:
    print()
    print(caixa_titulo(" COMANDOS DISPONIVEIS ", cor=Cor.MAGENTA))
    for titulo_secao, cor_secao, comandos in SECOES_AJUDA:
        print()
        print(colorir(f" {titulo_secao}", cor_secao + Cor.NEGRITO))
        print(separador(largura=LARGURA_PADRAO, cor=cor_secao))
        for comando, descricao in comandos:
            comando_fmt = colorir(f"  {comando:<32}", Cor.CINZA)
            print(f"{comando_fmt}{descricao}")
    print()


def imprimir_status(
    energia: int,
    limiar_critico: int,
    tripulantes: dict,
    arma_equipada: str | None = None,
) -> None:
    print()
    print(caixa_titulo(" STATUS DA NAVE ", cor=Cor.CIANO))

    cor_energia = Cor.VERDE if energia > limiar_critico else Cor.VERMELHO
    barra_preenchida = int(energia / 100 * 20)
    barra = "█" * barra_preenchida + "░" * (20 - barra_preenchida)
    print(f" Energia do nucleo: {colorir(barra, cor_energia)} {colorir(f'{energia}%', cor_energia)}")
    if energia <= limiar_critico:
        print(colorir("  >>> NIVEL CRITICO <<<", Cor.VERMELHO + Cor.NEGRITO))

    print()
    if tripulantes:
        print(colorir(" Tripulacao:", Cor.VERDE + Cor.NEGRITO))
        for tid, trip in tripulantes.items():
            print(f"   • {colorir(tid, Cor.VERDE)} — {trip.funcao_atual}")
    else:
        print(colorir(" Tripulacao: nenhum tripulante cadastrado ainda.", Cor.CINZA))

    print()
    print(colorir(" Armamento:", Cor.AMARELO + Cor.NEGRITO))
    if arma_equipada:
        print(f"   • {colorir(arma_equipada, Cor.AMARELO)}")
    else:
        print(colorir("   Nenhuma arma equipada.", Cor.CINZA))
    print()


def imprimir_prompt() -> str:
    return colorir("nave", Cor.CIANO + Cor.NEGRITO) + colorir(" » ", Cor.CINZA)


def imprimir_info(mensagem: str) -> None:
    print(colorir(mensagem, Cor.CINZA))


def imprimir_erro(mensagem: str) -> None:
    print(colorir(f"✖ {mensagem}", Cor.VERMELHO))


def imprimir_ok(mensagem: str) -> None:
    print(colorir(f"✔ {mensagem}", Cor.VERDE))
