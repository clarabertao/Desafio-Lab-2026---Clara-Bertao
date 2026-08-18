# Sistemas da Nave — Sprint de Mecânicas

Implementação dos três tickets aprovados pelo Game Design: Contingência do
Núcleo, Comportamento Dinâmico da Tripulação e Armamento Modular com
Modificadores. O projeto é dividido em módulos por responsabilidade dentro do
pacote `nave/`, cada um isolando um padrão de projeto, mais um loop de
comandos (REPL) para testar tudo manualmente.

## Estrutura do projeto

```
.
├── main.py                # ponto de entrada (python3 main.py)
└── nave/
    ├── __init__.py
    ├── nucleo.py           # Núcleo de Energia — Observer
    ├── tripulacao.py       # Tripulação — Strategy
    ├── armamento.py        # Armamento — Command + Decorator
    ├── ui.py               # camada visual: cores, caixas, menu (sem regra de negócio)
    └── cli.py              # REPL: só orquestra os módulos acima
```

Cada arquivo de padrão não conhece os outros — `nucleo.py`, `tripulacao.py`
e `armamento.py` não se importam entre si, nem conhecem `ui.py`. Só o
`cli.py` importa tudo, porque ele é a camada de orquestração/demo. Isso
facilita testar, reaproveitar ou trocar qualquer um dos sistemas
isoladamente (inclusive em outro projeto) sem arrastar os demais — e permite
trocar a "casca" visual do terminal sem tocar em nenhuma regra de negócio.

---

## 1. Mapeamento e Justificativa

### Ticket 1 — Contingência do Núcleo → **Observer**

O requisito proíbe o `Núcleo` de conhecer `Escudo`, `Luzes` ou `Painéis`, e
exige que novos sistemas (ex.: "Suporte de Vida") possam reagir a uma crise
sem alterar o Núcleo. Isso é exatamente o problema que o **Observer**
resolve: um sujeito (`NucleoEnergia`) mantém uma lista de observadores
genéricos e apenas notifica "algo aconteceu", sem saber quem está do outro
lado nem o que cada um vai fazer com a informação. Acoplamento fica
unidirecional (observador → interface do sujeito), então adicionar reações
novas é uma questão de criar uma classe e registrá-la — nunca de tocar no
Núcleo.

### Ticket 2 — Comportamento Dinâmico da Tripulação → **Strategy**

O requisito proíbe destruir/recriar o NPC para trocar de função e proíbe
if/else ou switch gigante para decidir o comportamento. O **Strategy**
resolve isso encapsulando cada função (operador de canhões, mecânico, etc.)
em uma classe própria que implementa uma interface comum. O `Tripulante`
(contexto) guarda apenas uma *referência* para a estratégia atual e delega o
trabalho a ela; trocar de função é só trocar essa referência em tempo de
execução, sem recriar o objeto e sem lógica condicional acumulada dentro do
`Tripulante`.

### Ticket 3 — Armamento Modular e Modificadores → **Command + Decorator**

Aqui há dois gargalos diferentes, então dois padrões se complementam:

- **Command**: a `Nave` não pode entender a física de cada fabricante de
  arma, só precisa emitir um comando genérico de "Atirar". Por isso toda
  arma (base ou modificada) implementa a mesma interface `Arma` com o método
  `disparar()`; a Nave chama sempre esse único método, delegando toda a
  lógica específica para o objeto arma.
- **Decorator**: os modificadores (Dano de Fogo, Perfuração de Blindagem,
  etc.) precisam se acoplar e empilhar dinamicamente sem gerar uma classe
  nova para cada combinação possível (Laser+Fogo, Laser+Fogo+Perfuração,
  Mísseis+Perfuração, ...). O Decorator resolve isso envolvendo a arma atual
  em camadas: cada modificador implementa a mesma interface `Arma`, guarda a
  arma anterior e adiciona seu efeito por cima do resultado dela. Empilhar
  efeitos vira só embrulhar objetos, sem explosão combinatória de classes.

> **Nota sobre o escopo do Command usado aqui:** esta é uma aplicação enxuta
> do padrão, focada apenas no problema descrito no ticket. `Nave.atirar()`
> atua como Invocador e conhece somente a interface `Arma.disparar()` (o
> "comando"), nunca a implementação concreta por trás dela — o que já
> resolve o desacoplamento pedido no briefing. Não foram implementados fila
> de comandos, histórico ou undo/redo, recursos comuns em implementações
> mais completas do Command, porque o requisito não pedia essas
> funcionalidades.

---

## 2. Identificação dos Papéis no Código

### Observer (Núcleo de Energia) — `nave/nucleo.py`

| Papel do padrão            | Classe/Interface no código                              |
|-----------------------------|-----------------------------------------------------------|
| Sujeito (Subject)           | `NucleoEnergia`                                            |
| Interface do Observador     | `ObservadorNucleo` (método `notificar(evento, contexto)`) |
| Observadores concretos      | `EscudoSistema`, `LuzesSistema`, `PaineisSistema`, `SuporteVidaSistema` (extensão de exemplo) |

`NucleoEnergia` guarda `self._observadores: list[ObservadorNucleo]` e chama
`_notificar_todos(...)` quando cruza o limiar crítico — sem importar nem
referenciar nenhuma classe concreta.

### Strategy (Tripulação) — `nave/tripulacao.py`

| Papel do padrão            | Classe/Interface no código                              |
|-----------------------------|-----------------------------------------------------------|
| Contexto                    | `Tripulante`                                                |
| Interface da Estratégia     | `FuncaoTripulante` (método `trabalhar(tripulante)`)        |
| Estratégias concretas       | `OperadorCanhoes`, `MecanicoMotor`, `EngenheiroSuporteVida`, `Piloto` |

`Tripulante._funcao` guarda a estratégia ativa; `trocar_funcao(nova_funcao)`
troca essa referência e `trabalhar()` delega para `self._funcao.trabalhar(self)`.

### Command + Decorator (Armamento) — `nave/armamento.py`

| Papel do padrão                        | Classe/Interface no código                     |
|------------------------------------------|---------------------------------------------------|
| Invocador do comando genérico            | `Nave` (método `atirar()`)                         |
| Interface do comando/produto             | `Arma` (método `disparar()`)                       |
| Armas concretas (implementação real)     | `LaserContinuo`, `EnxameMisseis`                   |
| Decorator base                            | `ModificadorArma` (implementa `Arma`, guarda uma `Arma` interna) |
| Decorators concretos                      | `DanoFogoDecorator`, `PerfuracaoBlindagemDecorator`, `TiroDuploDecorator` |

`Nave._arma_atual` é sempre do tipo `Arma` — pode ser uma arma-base ou uma
pilha de decorators em cima dela. `adicionar_modificador` envolve a arma
atual com um novo decorator; `atirar()` só chama `self._arma_atual.disparar()`.

---

## 3. Instruções de Execução

Pré-requisito: **Python 3.10+** instalado (o script usa `from __future__
import annotations` e sintaxe de union type `X | None`, compatível a partir
do 3.10).

```bash
# 1. Clonar o repositório
git clone <url-do-repositorio>
cd <pasta-do-repositorio>

# 2. Rodar a demonstração (não há dependências externas, é só stdlib)
python3 main.py
```

Não é preciso instalar nada nem compilar — `nave/` é reconhecido como pacote
Python automaticamente pelo `__init__.py`, e `main.py` importa `nave.cli` a
partir da raiz do repositório. Rode sempre com o diretório raiz como
diretório de trabalho (`cd` até a pasta que contém `main.py` antes de
executar).

Ao iniciar, o programa já registra os observadores do núcleo (Escudos, Luzes,
Painéis) e imprime a lista de comandos disponíveis. Digite `ajuda` a qualquer
momento para ver a lista de novo, ou `status` para ver o estado atual do
núcleo e da tripulação.

### Exemplo de sessão manual

```
>> tomar_dano 80
>> add_tripulante joao canhoes
>> trabalhar joao
>> trocar_funcao joao motor
>> trabalhar joao
>> equipar_arma laser
>> adicionar_modificador fogo
>> adicionar_modificador perfuracao
>> atirar
>> recarregar 50
>> status
>> sair
```

Isso deve, na ordem: levar o núcleo ao estado crítico (disparando os
observadores), criar um tripulante e trocar sua função em runtime (sem
recriar o objeto), equipar uma arma e empilhar dois modificadores nela antes
de atirar, e por fim recarregar energia até sair do estado de crise.

### Erro comum: `ModuleNotFoundError: No module named 'nave'`

Esse erro acontece quando o Python não encontra a pasta `nave/` ao lado do
`main.py` — geralmente porque o terminal está em outro diretório. Coisas a
checar:

1. **A estrutura de pastas está intacta?** Confirme que existe uma pasta
   `nave/` no mesmo nível de `main.py`, contendo `__init__.py`, `nucleo.py`,
   `tripulacao.py`, `armamento.py` e `cli.py`. Se você baixou os arquivos
   separadamente (ex.: um por um pelo navegador), é fácil perder essa
   estrutura — baixe/clone o projeto inteiro de uma vez.
2. **Onde o Windows PowerShell está posicionado?** Rode `dir` no terminal;
   você deve ver `main.py` e a pasta `nave` listados ali. Se não aparecerem,
   navegue até a pasta certa com `cd caminho\para\a\pasta` antes de rodar
   `python3 main.py`.
3. **A partir da versão atual do `main.py`**, isso não deveria mais
   acontecer mesmo rodando de outra pasta: o script adiciona automaticamente
   seu próprio diretório ao `sys.path` antes de importar `nave`. Se o erro
   persistir mesmo assim, é sinal de que a pasta `nave/` realmente não está
   ao lado do `main.py` que está sendo executado — confira o item 1.
