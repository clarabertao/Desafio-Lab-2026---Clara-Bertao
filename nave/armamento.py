"""
Ticket 3 - Armamento Modular e Modificadores Piratas.
Padroes aplicados: COMMAND (comando generico de disparo) + DECORATOR
(modificadores empilhaveis).

A Nave so conhece a interface Arma e emite o comando generico "disparar()".
Ela nunca sabe qual fabricante ou fisica esta por tras da arma equipada.

Nota sobre o Command: aqui usamos uma aplicacao enxuta do padrao. Nave.atirar()
e o Invocador, que conhece apenas a interface Arma.disparar() (o "comando"),
sem saber qual e a implementacao concreta por tras dela. Nao implementamos
fila de comandos nem undo/redo porque o briefing nao pediu isso -- o foco do
padrao aqui e exclusivamente desacoplar o invocador (Nave) da logica concreta
de cada arma/fabricante.

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
        """Executa o disparo (o "comando") e retorna a descricao textual do
        efeito produzido.

        Returns:
            Uma frase descrevendo o resultado do disparo.
        """
        ...

    @abstractmethod
    def descricao(self) -> str:
        """Retorna o nome de exibicao da arma (incluindo modificadores
        empilhados, quando aplicavel).

        Returns:
            Nome de exibicao da configuracao atual da arma.
        """
        ...


class LaserContinuo(Arma):
    """Arma concreta: feixe continuo de laser."""

    def disparar(self) -> str:
        """Dispara o laser continuo.

        Returns:
            Descricao do efeito do disparo.
        """
        return "Feixe de laser continuo disparado"

    def descricao(self) -> str:
        """Returns:
            Nome de exibicao desta arma.
        """
        return "Laser Continuo"


class EnxameMisseis(Arma):
    """Arma concreta: enxame de misseis guiados."""

    def disparar(self) -> str:
        """Dispara o enxame de misseis.

        Returns:
            Descricao do efeito do disparo.
        """
        return "Enxame de misseis lancado"

    def descricao(self) -> str:
        """Returns:
            Nome de exibicao desta arma.
        """
        return "Enxame de Misseis"


ARMAS_DISPONIVEIS: dict[str, type[Arma]] = {
    "laser": LaserContinuo,
    "misseis": EnxameMisseis,
}


class ModificadorArma(Arma):
    """Decorator base: embrulha uma Arma e acrescenta um efeito extra."""

    def __init__(self, arma_decorada: Arma) -> None:
        """Envolve uma arma existente (base ou ja decorada) para acrescentar
        um novo efeito por cima dela.

        Args:
            arma_decorada: A Arma (concreta ou ja decorada) a ser envolvida.
        """
        self._arma = arma_decorada

    def descricao(self) -> str:
        """Por padrao repassa a descricao da arma interna; subclasses
        sobrescrevem para acrescentar o proprio nome do modificador.

        Returns:
            Nome de exibicao da arma interna.
        """
        return self._arma.descricao()


class DanoFogoDecorator(ModificadorArma):
    """Decorator concreto: acrescenta dano de fogo ao disparo da arma
    interna."""

    def disparar(self) -> str:
        """Dispara a arma interna e acrescenta o efeito de fogo.

        Returns:
            Descricao do disparo original + o efeito de fogo.
        """
        return f"{self._arma.disparar()} + chamas incendiando o alvo (Dano de Fogo)"

    def descricao(self) -> str:
        """Returns:
            Descricao da arma interna + "Dano de Fogo".
        """
        return f"{self._arma.descricao()} + Dano de Fogo"


class PerfuracaoBlindagemDecorator(ModificadorArma):
    """Decorator concreto: acrescenta perfuracao de blindagem ao disparo da
    arma interna."""

    def disparar(self) -> str:
        """Dispara a arma interna e acrescenta o efeito de perfuracao.

        Returns:
            Descricao do disparo original + o efeito de perfuracao.
        """
        return f"{self._arma.disparar()} + impacto perfurante ignorando blindagem"

    def descricao(self) -> str:
        """Returns:
            Descricao da arma interna + "Perfuracao de Blindagem".
        """
        return f"{self._arma.descricao()} + Perfuracao de Blindagem"


class TiroDuploDecorator(ModificadorArma):
    """Decorator concreto: acrescenta um segundo disparo simultaneo."""

    def disparar(self) -> str:
        """Dispara a arma interna e acrescenta o segundo disparo.

        Returns:
            Descricao do disparo original + o efeito de tiro duplo.
        """
        return f"{self._arma.disparar()} + segundo disparo simultaneo (Tiro Duplo)"

    def descricao(self) -> str:
        """Returns:
            Descricao da arma interna + "Tiro Duplo".
        """
        return f"{self._arma.descricao()} + Tiro Duplo"


MODIFICADORES_DISPONIVEIS: dict[str, type[ModificadorArma]] = {
    "fogo": DanoFogoDecorator,
    "perfuracao": PerfuracaoBlindagemDecorator,
    "tiro_duplo": TiroDuploDecorator,
}


class Nave:
    """Invocador do Command: so emite o comando generico 'atirar'. Nao sabe
    nada sobre a fisica de cada fabricante de arma nem sobre os
    modificadores (decorators) acoplados a ela."""

    def __init__(self) -> None:
        """Inicializa a nave sem nenhuma arma equipada."""
        self._arma_atual: Arma | None = None

    def equipar_arma(self, arma: Arma) -> None:
        """Equipa uma arma-base (ainda sem modificadores) na nave.

        Args:
            arma: Instancia concreta de Arma (ex.: LaserContinuo) a equipar.
        """
        self._arma_atual = arma
        print(f"[NAVE] Arma equipada: {arma.descricao()}")

    def adicionar_modificador(self, decorator_cls: type[ModificadorArma]) -> None:
        """Empilha um novo modificador (decorator) sobre a arma atual.

        Args:
            decorator_cls: Classe do ModificadorArma a aplicar (ex.:
                DanoFogoDecorator). Uma nova instancia e criada envolvendo
                a arma atual.
        """
        if self._arma_atual is None:
            print("[NAVE] Nenhuma arma equipada para modificar.")
            return
        self._arma_atual = decorator_cls(self._arma_atual)
        print(f"[NAVE] Modificador aplicado. Configuracao atual: {self._arma_atual.descricao()}")

    def atirar(self) -> None:
        """Emite o comando generico de disparo para a arma atualmente
        equipada, sem conhecer sua implementacao concreta nem os
        modificadores empilhados nela."""
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
