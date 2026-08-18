"""
Ticket 2 - Comportamento Dinamico da Tripulacao.
Padrao aplicado: STRATEGY.

Cada funcao (operador de canhoes, mecanico do motor, etc.) e uma estrategia
intercambiavel. O Tripulante (contexto) guarda uma REFERENCIA a estrategia
atual e delega o trabalho a ela -- nada de if/elif gigante, e o objeto nunca
e destruido para trocar de funcao.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class FuncaoTripulante(ABC):
    """Interface de estrategia: cada funcao sabe como 'trabalhar'."""

    nome: str = "Funcao Generica"

    @abstractmethod
    def trabalhar(self, tripulante: "Tripulante") -> None:
        ...


class OperadorCanhoes(FuncaoTripulante):
    nome = "Operador de Canhoes"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        print(f"[{tripulante.nome}] Mirando e disparando os canhoes principais.")


class MecanicoMotor(FuncaoTripulante):
    nome = "Mecanico do Motor"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        print(f"[{tripulante.nome}] Ajustando a pressao do motor e reparando conduites.")


class EngenheiroSuporteVida(FuncaoTripulante):
    nome = "Engenheiro de Suporte de Vida"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        print(f"[{tripulante.nome}] Monitorando niveis de oxigenio e filtros de ar.")


class Piloto(FuncaoTripulante):
    nome = "Piloto"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        print(f"[{tripulante.nome}] Ajustando rota e corrigindo trajetoria.")


FUNCOES_DISPONIVEIS: dict[str, type[FuncaoTripulante]] = {
    "canhoes": OperadorCanhoes,
    "motor": MecanicoMotor,
    "suporte_vida": EngenheiroSuporteVida,
    "piloto": Piloto,
}


class Tripulante:
    """O mesmo objeto/entidade e reaproveitado; so a estrategia (funcao) muda."""

    def __init__(self, nome: str, funcao_inicial: FuncaoTripulante) -> None:
        self.nome = nome
        self._funcao = funcao_inicial

    def trocar_funcao(self, nova_funcao: FuncaoTripulante) -> None:
        print(f"[{self.nome}] Funcao alterada: {self._funcao.nome} -> {nova_funcao.nome}")
        self._funcao = nova_funcao

    def trabalhar(self) -> None:
        self._funcao.trabalhar(self)

    @property
    def funcao_atual(self) -> str:
        return self._funcao.nome
