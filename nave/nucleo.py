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
        """Reage a um evento emitido pelo NucleoEnergia.

        Args:
            evento: Identificador do evento ("energia_critica" ou
                "energia_normalizada").
            contexto: Dados extras sobre o evento (ex.: {"energia": 20}).
        """
        ...


class NucleoEnergia:
    """Sujeito observado. So conhece a interface ObservadorNucleo, nunca as
    classes concretas que reagem aos eventos."""

    ENERGIA_MAXIMA = 100
    LIMIAR_CRITICO = 30

    def __init__(self) -> None:
        """Inicializa o nucleo com energia cheia e nenhum observador registrado."""
        self._energia = self.ENERGIA_MAXIMA
        self._observadores: list[ObservadorNucleo] = []
        self._em_crise = False

    def adicionar_observador(self, observador: ObservadorNucleo) -> None:
        """Registra um novo sistema reativo para ser notificado por eventos futuros.

        Args:
            observador: Instancia que implementa ObservadorNucleo.
        """
        self._observadores.append(observador)

    def remover_observador(self, observador: ObservadorNucleo) -> None:
        """Remove um sistema reativo da lista de notificacao, se estiver presente.

        Args:
            observador: Instancia previamente registrada via adicionar_observador.
        """
        if observador in self._observadores:
            self._observadores.remove(observador)

    def _notificar_todos(self, evento: str, contexto: dict) -> None:
        """Propaga um evento para todos os observadores registrados.

        Args:
            evento: Identificador do evento a propagar.
            contexto: Dados extras sobre o evento.
        """
        for observador in self._observadores:
            observador.notificar(evento, contexto)

    def _checar_estado_critico(self) -> None:
        """Verifica se a energia cruzou o limiar critico (para cima ou para
        baixo) e, se sim, dispara a notificacao correspondente aos
        observadores registrados."""
        if self._energia <= self.LIMIAR_CRITICO and not self._em_crise:
            self._em_crise = True
            print(f"\n[NUCLEO] >>> ENERGIA CRITICA ({self._energia}%) <<<")
            self._notificar_todos("energia_critica", {"energia": self._energia})
        elif self._energia > self.LIMIAR_CRITICO and self._em_crise:
            self._em_crise = False
            print(f"\n[NUCLEO] Energia estabilizada ({self._energia}%). Encerrando crise.")
            self._notificar_todos("energia_normalizada", {"energia": self._energia})

    def tomar_dano(self, valor: int) -> None:
        """Aplica dano de combate ao nucleo, reduzindo a energia.

        Args:
            valor: Quantidade de dano a subtrair da energia atual (nao
                permite energia negativa).
        """
        self._energia = max(0, self._energia - valor)
        print(f"[NUCLEO] Dano recebido: -{valor}. Energia atual: {self._energia}%")
        self._checar_estado_critico()

    def reduzir_energia(self, valor: int) -> None:
        """Reduz a energia manualmente (fora de um contexto de dano/combate).

        Args:
            valor: Quantidade de energia a subtrair.
        """
        self._energia = max(0, self._energia - valor)
        print(f"[NUCLEO] Energia reduzida manualmente: -{valor}. Energia atual: {self._energia}%")
        self._checar_estado_critico()

    def recarregar(self, valor: int) -> None:
        """Recarrega a energia do nucleo, respeitando o teto de ENERGIA_MAXIMA.

        Args:
            valor: Quantidade de energia a adicionar.
        """
        self._energia = min(self.ENERGIA_MAXIMA, self._energia + valor)
        print(f"[NUCLEO] Energia recarregada: +{valor}. Energia atual: {self._energia}%")
        self._checar_estado_critico()

    @property
    def energia(self) -> int:
        """int: Nivel atual de energia do nucleo (0 a ENERGIA_MAXIMA)."""
        return self._energia


class EscudoSistema(ObservadorNucleo):
    """Observador concreto: ajusta a configuracao dos escudos conforme o
    estado de energia do nucleo."""

    def notificar(self, evento: str, contexto: dict) -> None:
        """Reage a mudancas de estado do nucleo redirecionando os escudos.

        Args:
            evento: "energia_critica" ou "energia_normalizada".
            contexto: Dados extras sobre o evento (nao utilizados aqui).
        """
        if evento == "energia_critica":
            print("[ESCUDOS] Redirecionando foco para defesa frontal de emergencia.")
        elif evento == "energia_normalizada":
            print("[ESCUDOS] Retornando para configuracao de defesa padrao.")


class LuzesSistema(ObservadorNucleo):
    """Observador concreto: liga/desliga iluminacao nao essencial da nave."""

    def notificar(self, evento: str, contexto: dict) -> None:
        """Reage a mudancas de estado do nucleo ajustando a iluminacao.

        Args:
            evento: "energia_critica" ou "energia_normalizada".
            contexto: Dados extras sobre o evento (nao utilizados aqui).
        """
        if evento == "energia_critica":
            print("[LUZES] Apagando iluminacao nao essencial das salas.")
        elif evento == "energia_normalizada":
            print("[LUZES] Reacendendo iluminacao das salas.")


class PaineisSistema(ObservadorNucleo):
    """Observador concreto: exibe/remove alertas visuais nos paineis de
    navegacao."""

    def notificar(self, evento: str, contexto: dict) -> None:
        """Reage a mudancas de estado do nucleo atualizando os paineis.

        Args:
            evento: "energia_critica" ou "energia_normalizada".
            contexto: Dados extras sobre o evento (nao utilizados aqui).
        """
        if evento == "energia_critica":
            print("[PAINEIS] Exibindo alerta vermelho de energia critica na navegacao.")
        elif evento == "energia_normalizada":
            print("[PAINEIS] Removendo alertas de energia da navegacao.")


class SuporteVidaSistema(ObservadorNucleo):
    """Exemplo de extensao futura: observador concreto adicionado sem
    alterar NucleoEnergia (basta instanciar esta classe e chamar
    nucleo.adicionar_observador(SuporteVidaSistema()))."""

    def notificar(self, evento: str, contexto: dict) -> None:
        """Reage a mudancas de estado do nucleo ajustando o consumo do
        suporte de vida.

        Args:
            evento: "energia_critica" ou "energia_normalizada".
            contexto: Dados extras sobre o evento (nao utilizados aqui).
        """
        if evento == "energia_critica":
            print("[SUPORTE DE VIDA] Reduzindo consumo ao minimo vital.")
        elif evento == "energia_normalizada":
            print("[SUPORTE DE VIDA] Retomando operacao normal.")
