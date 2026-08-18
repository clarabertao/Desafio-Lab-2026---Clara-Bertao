"""
Loop de comandos manual (REPL) para testar os tres sistemas em tempo real.
Este modulo so orquestra: instancia os objetos, le comandos do terminal e
chama os metodos publicos de cada sistema. Nenhuma regra de negocio mora
aqui -- ela fica isolada em nucleo.py, tripulacao.py e armamento.py. A parte
visual (cores, caixas, menu) fica isolada em ui.py.
"""

from __future__ import annotations

from . import ui
from .nucleo import (
    NucleoEnergia,
    EscudoSistema,
    LuzesSistema,
    PaineisSistema,
    SuporteVidaSistema,
)
from .tripulacao import Tripulante, FUNCOES_DISPONIVEIS
from .armamento import Nave, ARMAS_DISPONIVEIS, MODIFICADORES_DISPONIVEIS


def mostrar_status(nucleo: NucleoEnergia, tripulantes: dict[str, Tripulante], nave: Nave) -> None:
    ui.imprimir_status(
        nucleo.energia,
        NucleoEnergia.LIMIAR_CRITICO,
        tripulantes,
        arma_equipada=nave.descricao_arma_atual,
    )


def _criar_nucleo_padrao() -> NucleoEnergia:
    nucleo = NucleoEnergia()
    nucleo.adicionar_observador(EscudoSistema())
    nucleo.adicionar_observador(LuzesSistema())
    nucleo.adicionar_observador(PaineisSistema())
    return nucleo


def executar_comando(
    linha: str,
    nucleo: NucleoEnergia,
    tripulantes: dict[str, Tripulante],
    nave: Nave,
) -> bool:
    """Processa uma linha de comando. Retorna False se o programa deve encerrar."""

    partes = linha.split()
    cmd = partes[0].lower()
    args = partes[1:]

    if cmd == "sair":
        ui.imprimir_info("Encerrando sistemas da nave.")
        return False

    elif cmd == "ajuda":
        ui.imprimir_ajuda()

    elif cmd == "status":
        mostrar_status(nucleo, tripulantes, nave)

    # ---------------- Nucleo de energia ----------------
    elif cmd == "tomar_dano":
        nucleo.tomar_dano(int(args[0]))

    elif cmd == "reduzir_energia":
        nucleo.reduzir_energia(int(args[0]))

    elif cmd == "recarregar":
        nucleo.recarregar(int(args[0]))

    elif cmd == "suporte_vida_on":
        nucleo.adicionar_observador(SuporteVidaSistema())
        ui.imprimir_ok("Suporte de Vida registrado como novo sistema reativo do nucleo.")

    # ---------------- Tripulacao ----------------
    elif cmd == "add_tripulante":
        tid, funcao_key = args[0], args[1]
        if funcao_key not in FUNCOES_DISPONIVEIS:
            ui.imprimir_erro(f"Funcao invalida. Opcoes: {list(FUNCOES_DISPONIVEIS)}")
        else:
            tripulantes[tid] = Tripulante(tid, FUNCOES_DISPONIVEIS[funcao_key]())
            ui.imprimir_ok(f"Tripulante '{tid}' criado como {tripulantes[tid].funcao_atual}.")

    elif cmd == "trocar_funcao":
        tid, funcao_key = args[0], args[1]
        if tid not in tripulantes:
            ui.imprimir_erro(f"Tripulante '{tid}' nao encontrado.")
        elif funcao_key not in FUNCOES_DISPONIVEIS:
            ui.imprimir_erro(f"Funcao invalida. Opcoes: {list(FUNCOES_DISPONIVEIS)}")
        else:
            tripulantes[tid].trocar_funcao(FUNCOES_DISPONIVEIS[funcao_key]())

    elif cmd == "trabalhar":
        tid = args[0]
        if tid not in tripulantes:
            ui.imprimir_erro(f"Tripulante '{tid}' nao encontrado.")
        else:
            tripulantes[tid].trabalhar()

    # ---------------- Armamento ----------------
    elif cmd == "equipar_arma":
        tipo = args[0]
        if tipo not in ARMAS_DISPONIVEIS:
            ui.imprimir_erro(f"Arma invalida. Opcoes: {list(ARMAS_DISPONIVEIS)}")
        else:
            nave.equipar_arma(ARMAS_DISPONIVEIS[tipo]())

    elif cmd == "adicionar_modificador":
        tipo = args[0]
        if tipo not in MODIFICADORES_DISPONIVEIS:
            ui.imprimir_erro(f"Modificador invalido. Opcoes: {list(MODIFICADORES_DISPONIVEIS)}")
        else:
            nave.adicionar_modificador(MODIFICADORES_DISPONIVEIS[tipo])

    elif cmd == "atirar":
        nave.atirar()

    else:
        ui.imprimir_erro(f"Comando desconhecido: '{cmd}'. Digite 'ajuda' para a lista de comandos.")

    return True


def main() -> None:
    nucleo = _criar_nucleo_padrao()
    tripulantes: dict[str, Tripulante] = {}
    nave = Nave()

    ui.imprimir_banner()
    ui.imprimir_ajuda()

    while True:
        try:
            linha = input(ui.imprimir_prompt()).strip()
        except EOFError:
            break

        if not linha:
            continue

        try:
            continuar = executar_comando(linha, nucleo, tripulantes, nave)
        except (IndexError, ValueError) as erro:
            ui.imprimir_erro(f"Argumentos invalidos para o comando digitado. Detalhe: {erro}")
            continue

        if not continuar:
            break
