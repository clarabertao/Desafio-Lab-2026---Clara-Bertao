"""
Ticket 1 - Contingencia do Nucleo da Nave.
Padrao aplicado: OBSERVER.

O NucleoEnergia (sujeito) nao conhece Escudo, Luzes ou Paineis. Ele so
conhece a interface ObservadorNucleo e notifica todos os registrados quando
cruza o limiar critico. Novos sistemas reativos (ex.: Suporte de Vida) podem
ser adicionados criando uma classe nova e chamando adicionar_observador,
sem tocar em nenhuma linha desta classe.
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class ObservadorNucleo(ABC):
    """Interface que qualquer sistema reativo da nave deve implementar."""

    @abstractmethod
    def notificar(self, evento: str, contexto: dict) -> None:
        ...


class NucleoEnergia:
    """Sujeito observado. So conhece a interface ObservadorNucleo, nunca as
    classes concretas que reagem aos eventos."""

    ENERGIA_MAXIMA = 100
    LIMIAR_CRITICO = 30

    def __init__(self) -> None:
        self._energia = self.ENERGIA_MAXIMA
        self._observadores: list[ObservadorNucleo] = []
        self._em_crise = False

    def adicionar_observador(self, observador: ObservadorNucleo) -> None:
        self._observadores.append(observador)

    def remover_observador(self, observador: ObservadorNucleo) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)

    def _notificar_todos(self, evento: str, contexto: dict) -> None:
        for observador in self._observadores:
            observador.notificar(evento, contexto)

    def _checar_estado_critico(self) -> None:
        if self._energia <= self.LIMIAR_CRITICO and not self._em_crise:
            self._em_crise = True
            print(f"\n[NUCLEO] >>> ENERGIA CRITICA ({self._energia}%) <<<")
            self._notificar_todos("energia_critica", {"energia": self._energia})
        elif self._energia > self.LIMIAR_CRITICO and self._em_crise:
            self._em_crise = False
            print(f"\n[NUCLEO] Energia estabilizada ({self._energia}%). Encerrando crise.")
            self._notificar_todos("energia_normalizada", {"energia": self._energia})

    def tomar_dano(self, valor: int) -> None:
        self._energia = max(0, self._energia - valor)
        print(f"[NUCLEO] Dano recebido: -{valor}. Energia atual: {self._energia}%")
        self._checar_estado_critico()

    def reduzir_energia(self, valor: int) -> None:
        self._energia = max(0, self._energia - valor)
        print(f"[NUCLEO] Energia reduzida manualmente: -{valor}. Energia atual: {self._energia}%")
        self._checar_estado_critico()

    def recarregar(self, valor: int) -> None:
        self._energia = min(self.ENERGIA_MAXIMA, self._energia + valor)
        print(f"[NUCLEO] Energia recarregada: +{valor}. Energia atual: {self._energia}%")
        self._checar_estado_critico()

    @property
    def energia(self) -> int:
        return self._energia


class EscudoSistema(ObservadorNucleo):
    def notificar(self, evento: str, contexto: dict) -> None:
        if evento == "energia_critica":
            print("[ESCUDOS] Redirecionando foco para defesa frontal de emergencia.")
        elif evento == "energia_normalizada":
            print("[ESCUDOS] Retornando para configuracao de defesa padrao.")


class LuzesSistema(ObservadorNucleo):
    def notificar(self, evento: str, contexto: dict) -> None:
        if evento == "energia_critica":
            print("[LUZES] Apagando iluminacao nao essencial das salas.")
        elif evento == "energia_normalizada":
            print("[LUZES] Reacendendo iluminacao das salas.")


class PaineisSistema(ObservadorNucleo):
    def notificar(self, evento: str, contexto: dict) -> None:
        if evento == "energia_critica":
            print("[PAINEIS] Exibindo alerta vermelho de energia critica na navegacao.")
        elif evento == "energia_normalizada":
            print("[PAINEIS] Removendo alertas de energia da navegacao.")


# Exemplo de extensao futura sem tocar em NucleoEnergia: basta somar esta classe
# e chamar nucleo.adicionar_observador(SuporteVidaSistema()).
class SuporteVidaSistema(ObservadorNucleo):
    def notificar(self, evento: str, contexto: dict) -> None:
        if evento == "energia_critica":
            print("[SUPORTE DE VIDA] Reduzindo consumo ao minimo vital.")
        elif evento == "energia_normalizada":
            print("[SUPORTE DE VIDA] Retomando operacao normal.")
