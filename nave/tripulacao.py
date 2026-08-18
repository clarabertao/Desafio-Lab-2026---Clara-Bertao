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
        """Executa a tarefa correspondente a esta funcao.

        Args:
            tripulante: O Tripulante (contexto) que esta executando a
                estrategia, usado para exibir o nome nas mensagens.
        """
        ...


class OperadorCanhoes(FuncaoTripulante):
    """Estrategia concreta: comportamento de operador de canhoes."""

    nome = "Operador de Canhoes"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        """Simula o tripulante mirando e disparando os canhoes.

        Args:
            tripulante: O Tripulante que executa esta funcao.
        """
        print(f"[{tripulante.nome}] Mirando e disparando os canhoes principais.")


class MecanicoMotor(FuncaoTripulante):
    """Estrategia concreta: comportamento de mecanico do motor."""

    nome = "Mecanico do Motor"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        """Simula o tripulante ajustando e reparando o motor.

        Args:
            tripulante: O Tripulante que executa esta funcao.
        """
        print(f"[{tripulante.nome}] Ajustando a pressao do motor e reparando conduites.")


class EngenheiroSuporteVida(FuncaoTripulante):
    """Estrategia concreta: comportamento de engenheiro de suporte de vida."""

    nome = "Engenheiro de Suporte de Vida"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        """Simula o tripulante monitorando oxigenio e filtros de ar.

        Args:
            tripulante: O Tripulante que executa esta funcao.
        """
        print(f"[{tripulante.nome}] Monitorando niveis de oxigenio e filtros de ar.")


class Piloto(FuncaoTripulante):
    """Estrategia concreta: comportamento de piloto."""

    nome = "Piloto"

    def trabalhar(self, tripulante: "Tripulante") -> None:
        """Simula o tripulante ajustando rota e trajetoria.

        Args:
            tripulante: O Tripulante que executa esta funcao.
        """
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
        """Cria um tripulante com uma funcao (estrategia) inicial.

        Args:
            nome: Identificador/nome de exibicao do tripulante.
            funcao_inicial: Instancia de FuncaoTripulante a ser usada
                como estrategia ativa desde a criacao.
        """
        self.nome = nome
        self._funcao = funcao_inicial

    def trocar_funcao(self, nova_funcao: FuncaoTripulante) -> None:
        """Troca a estrategia ativa em tempo de execucao, sem recriar o
        objeto Tripulante.

        Args:
            nova_funcao: Nova instancia de FuncaoTripulante a assumir.
        """
        print(f"[{self.nome}] Funcao alterada: {self._funcao.nome} -> {nova_funcao.nome}")
        self._funcao = nova_funcao

    def trabalhar(self) -> None:
        """Delega a execucao da tarefa para a estrategia (funcao) atual."""
        self._funcao.trabalhar(self)

    @property
    def funcao_atual(self) -> str:
        """str: Nome de exibicao da funcao (estrategia) atualmente ativa."""
        return self._funcao.nome
