"""
Ticket 3 - Armamento Modular e Modificadores Piratas.
Padroes aplicados: COMMAND (comando generico de disparo) + DECORATOR
(modificadores empilhaveis).

A Nave so conhece a interface Arma e emite o comando generico "disparar()".
Ela nunca sabe qual fabricante ou fisica esta por tras da arma equipada.

Os modificadores (fogo, perfuracao...) sao decorators: cada um envolve a arma
atual e acrescenta seu efeito ao resultado do disparo, permitindo empilhar
quantos modificadores quiser sem criar uma classe nova para cada combinacao.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Arma(ABC):
    """Interface comum a qualquer arma-base ou arma decorada."""

    @abstractmethod
    def disparar(self) -> str:
        ...

    @abstractmethod
    def descricao(self) -> str:
        ...


class LaserContinuo(Arma):
    def disparar(self) -> str:
        return "Feixe de laser continuo disparado"

    def descricao(self) -> str:
        return "Laser Continuo"


class EnxameMisseis(Arma):
    def disparar(self) -> str:
        return "Enxame de misseis lancado"

    def descricao(self) -> str:
        return "Enxame de Misseis"


ARMAS_DISPONIVEIS: dict[str, type[Arma]] = {
    "laser": LaserContinuo,
    "misseis": EnxameMisseis,
}


class ModificadorArma(Arma):
    """Decorator base: embrulha uma Arma e acrescenta um efeito extra."""

    def __init__(self, arma_decorada: Arma) -> None:
        self._arma = arma_decorada

    def descricao(self) -> str:
        return self._arma.descricao()


class DanoFogoDecorator(ModificadorArma):
    def disparar(self) -> str:
        return f"{self._arma.disparar()} + chamas incendiando o alvo (Dano de Fogo)"

    def descricao(self) -> str:
        return f"{self._arma.descricao()} + Dano de Fogo"


class PerfuracaoBlindagemDecorator(ModificadorArma):
    def disparar(self) -> str:
        return f"{self._arma.disparar()} + impacto perfurante ignorando blindagem"

    def descricao(self) -> str:
        return f"{self._arma.descricao()} + Perfuracao de Blindagem"


class TiroDuploDecorator(ModificadorArma):
    def disparar(self) -> str:
        return f"{self._arma.disparar()} + segundo disparo simultaneo (Tiro Duplo)"

    def descricao(self) -> str:
        return f"{self._arma.descricao()} + Tiro Duplo"


MODIFICADORES_DISPONIVEIS: dict[str, type[ModificadorArma]] = {
    "fogo": DanoFogoDecorator,
    "perfuracao": PerfuracaoBlindagemDecorator,
    "tiro_duplo": TiroDuploDecorator,
}


class Nave:
    """A Nave so emite o comando generico 'atirar'. Nao sabe nada sobre a
    fisica de cada fabricante de arma nem sobre os modificadores acoplados."""

    def __init__(self) -> None:
        self._arma_atual: Arma | None = None

    def equipar_arma(self, arma: Arma) -> None:
        self._arma_atual = arma
        print(f"[NAVE] Arma equipada: {arma.descricao()}")

    def adicionar_modificador(self, decorator_cls: type[ModificadorArma]) -> None:
        if self._arma_atual is None:
            print("[NAVE] Nenhuma arma equipada para modificar.")
            return
        self._arma_atual = decorator_cls(self._arma_atual)
        print(f"[NAVE] Modificador aplicado. Configuracao atual: {self._arma_atual.descricao()}")

    def atirar(self) -> None:
        if self._arma_atual is None:
            print("[NAVE] Comando 'Atirar' emitido, mas nenhuma arma esta equipada.")
            return
        print("[NAVE] Comando generico 'Atirar' emitido.")
        print(f"[ARMA] {self._arma_atual.disparar()}")

    @property
    def descricao_arma_atual(self) -> str | None:
        """Descricao da arma equipada (com modificadores ja empilhados), ou
        None se nenhuma arma estiver equipada. Usado pela camada visual para
        exibir o status atual sem que ela precise conhecer a estrutura
        interna dos decorators."""
        if self._arma_atual is None:
            return None
        return self._arma_atual.descricao()
