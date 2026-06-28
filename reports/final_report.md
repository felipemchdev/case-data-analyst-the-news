# Palavritas: o que determina se um usuario volta a jogar?

**Case para Analista de Dados Produto & Growth - the news**

---

## 1. Objetivo

Entender quais variaveis mais se associam com o usuario voltar a jogar no dia seguinte (D+1) e estar ativo apos 30 dias (D30), e propor acoes concretas para aumentar a retencao.

---

## 2. Entendimento do problema

O Palavritas e um jogo diario de palavras com ate 6 tentativas. A retencao D+1 media e de **22.1%** e a D30 e de **31.9%**. A pergunta central: o que diferencia os 22% que voltam dos 78% que nao voltam?

Separei em quatro camadas de analise:

1. Comportamento na sessao (resultado, tempo, hora, streak)
2. Relacao com a newsletter
3. Perfil do usuario (setor, salario, device)
4. Padroes longitudinais (curva de retencao, coortes, segmentacao)

---

## 3. Qualidade dos dados

### 3.1 Problemas encontrados e decisoes

| Problema | Decisao | Impacto |
|---|---|---|
| Datas em formato misto (ISO e DD/MM/YYYY) | Parse duplo com fallback. 0 linhas perdidas | Resolvido |
| `attempts` com valores 0, 7 e 8 | Removidos (fora do range 1-6, 93 linhas) | 93 linhas removidas |
| `device` inconsistente (`Android`, `android`, `ios`, `iOS`) | Normalizado. Nao mapeados assumidos Android | Resolvido |
| `user_profile` com 800 usuarios vs ~12k unicos em sessions | Apenas ~6% tem perfil. Analises de perfil tem amostra reduzida | Limitacao documentada |
| `orders_food_delivery`, `plays_other_word_games`, `newsletter_subscriber` com strings inconsistentes | Normalizado para booleano | Resolvido |
| `age_range` e `salary_range` com ~15% nulos | Preenchidos como "Nao informado" | Resolvido |
| 1.198 session_id duplicados | Removidos | 1.198 linhas removidas |
| 63 resultados invalidos (nem win nem lose) | Removidos | 63 linhas removidas |
| Caracteres quebrados em palavras com acentos | Encoding do CSV. Cosmetico, nao corrigido | Cosmetico |

### 3.2 Tamanho final apos limpeza

- `palavritas_sessions`: 39.849 sessoes, ~12.000 usuarios unicos (periodo: dez/2025 a mai/2026)
- `palavritas_attempts`: 147.217 tentativas
- `user_profile`: 800 usuarios

---

## 4. Analises

### 4.1 Ganhar ou perder muda a retencao?

| Resultado | Sessoes | D+1 | D30 |
|---|---|---|---|
| Win | 24.043 | 21.9% | 32.7% |
| Lose | 15.806 | 22.5% | 30.8% |

Ganhar ou perder tem **efeito praticamente nulo em D+1** (diferenca de apenas -0.6pp). Em D30, quem ganha tem 1.9pp a mais. A diferenca nao e estatisticamente significativa para D+1 (z=1.6, p=0.11).

**Interpretacao:** ao contrario do que se poderia esperar, o resultado do jogo nao e o que determina se o usuario volta amanha. A retencao D+1 e baixa (~22%) independente de ganhar ou perder.

---

### 4.2 Streak: o efeito habito

| Streak Day | Sessoes | D+1 | D30 |
|---|---|---|---|
| 1 | 31.032 | 21.7% | 32.0% |
| 2 | 6.720 | 23.4% | 31.8% |
| 3 | 1.576 | 23.8% | 31.4% |
| 4 | 374 | 27.5% | 34.0% |
| 5 | 104 | 29.8% | 35.6% |
| 6 | 31 | 29.0% | 35.5% |

D+1 sobe gradualmente de 21.7% (streak 1) para 29.8% (streak 5) — um ganho de +8pp. A maior queda de volume acontece entre streak 1 (31k) e streak 2 (6.7k), ou seja, **78% das sessoes sao de usuarios sem sequencia**.

**Interpretacao:** o habito existe mas e fraco. Mesmo no streak 5, D+1 e de apenas 30%. O gargalo nao e o dia 3 — e o dia 1. O problema e que 78% das sessoes sao de usuarios que nao estao em sequencia nenhuma.

---

### 4.3 Existe um horario ideal?

| Faixa | Sessoes | D+1 | D30 |
|---|---|---|---|
| Manha (6-9h) | ~16.000 | 22.8% | 32.5% |
| Tarde (10-14h) | ~4.800 | 21.5% | 31.0% |
| Fim de tarde (15-19h) | ~9.500 | 22.1% | 31.8% |
| Noite (20-23h) | ~9.500 | 21.4% | 31.4% |

Diferenca maxima entre horarios: 1.4pp em D+1. Horario nao explica retencao.

**Interpretacao:** o horario nao e um driver de retencao. Importa mais para estrategia de push — manha concentra mais usuarios.

---

### 4.4 Device: Android vs iOS

| Device | Sessoes | D+1 | D30 |
|---|---|---|---|
| Android | ~24.500 | 22.2% | 31.8% |
| iOS | ~15.300 | 22.0% | 32.0% |

Praticamente identico. Device nao explica retencao.

---

### 4.5 Newsletter: o unico driver forte de D30

| Abriu newsletter? | Sessoes | D+1 | D30 |
|---|---|---|---|
| Sim | 7.651 | 21.5% | 37.8% |
| Nao | 32.198 | 22.3% | 30.5% |

Quem abre a newsletter tem D+1 **praticamente igual** (21.5% vs 22.3%), mas D30 **7.3pp maior** (37.8% vs 30.5%). A newsletter nao traz o usuario amanha — mas mantem ele no longo prazo.

**Interpretacao:** abrir a newsletter e um sinal de que o usuario esta no ecossistema the news. Nao e um gatilho de retorno imediato, e sim um indicador de retencao de longo prazo. A newsletter funciona como "cola" do ecossistema, nao como alavanca de jogo.

### 4.5.1 Stickiness e uso diario

| Metrica | Valor |
|---|---|
| DAU medio (jogadores/dia) | 221 |
| WAU medio (jogadores/semana) | 1.533 |
| MAU medio (jogadores/mes) | 6.642 |
| Stickiness (DAU/MAU) | 3.3% |

Stickiness de 3.3% e baixo para um jogo diario (benchmark: 10-20%). A maioria dos MAU joga esporadicamente.

---

### 4.6 Palavras dificeis derrubam retencao?

Palavras agrupadas por win rate:

| Dificuldade | Win Rate medio | Palavras | D+1 medio |
|---|---|---|---|
| Dificil (win rate < 70%) | ~62% | ~25 | 20.5% |
| Media (70-85%) | ~78% | ~50 | 22.1% |
| Facil (> 85%) | ~93% | ~55 | 23.0% |

Diferenca de apenas 2.5pp entre palavras dificeis e faceis. Impacto e bem menor do que parecia inicialmente.

**Interpretacao:** a dificuldade da palavra tem efeito marginal em D+1. Nao e um driver primario.

---

### 4.7 Curva de Retencao Global

| Dia | Usuarios ativos (%) |
|---|---|
| D1 | 38.5% |
| D3 | 14.2% |
| D7 | 6.8% |
| D14 | 3.5% |
| D30 | 1.8% |

Queda mais acentuada entre D1 e D3 (-24pp). Quem sobrevive ao terceiro dia tem retencao mais estavel.

---

### 4.8 Analise de Coorte Semanal

Coortes recentes (abr-mai/2026) tem retencao levemente superior as iniciais (dez/2025). Retencao na Semana 1 varia entre 20-30%, caindo para 5-10% na Semana 4. Produto parece estar melhorando ao longo do tempo.

---

### 4.9 Segmentacao de Usuarios

| Segmento | Usuarios | Sessoes medias | D+1 medio | D30 medio | Win Rate |
|---|---|---|---|---|---|
| Heavy (6+ jogos) | ~1.200 | 9.2 | 68.1% | 76.4% | 87.3% |
| Medium (2-5) | ~4.500 | 2.8 | 42.3% | 47.8% | 81.2% |
| Light (1) | ~6.300 | 1.0 | 12.4% | 18.5% | 78.9% |

Heavy users (10% da base) tem D30 de 76.4%. Light users (52% da base) tem D30 de apenas 18.5%. **Este e o maior diferencial de retencao encontrado.**

---

### 4.10 Perfil do usuario (base: 800 usuarios com survey)

| Variavel | Maior D30 | Menor D30 |
|---|---|---|
| Faixa salarial | acima de R$10k (52%) | ate R$2k (35%) |
| Setor | tech (45%) | direito (35%) |
| Faixa etaria | 45+ (44%) | 18-24 (36%) |
| Horario tipico | morning (43%) | night (36%) |
| Assinante newsletter | Sim (42%) | Nao (35%) |

Base pequena (6% dos usuarios). Trato como direcional.

---

## 5. Ranking final: o que REALMENTE se associa com retencao?

### Para voltar no dia seguinte (D+1):

| Variavel | Impacto | Explicacao |
|---|---|---|
| Streak day | +8pp (streak 1 → 5) | Moderado. Sobe gradualmente |
| Horario | +1.4pp (manha vs noite) | Muito baixo |
| Resultado (win/lose) | -0.6pp (win vs lose) | Irrelevante |
| Newsletter aberta | -0.8pp (sim vs nao) | Irrelevante para D+1 |
| Palavra dificil | -2.5pp (dificil vs facil) | Baixo |

### Para estar ativo em 30 dias (D30):

| Variavel | Impacto | Explicacao |
|---|---|---|
| Segmento (heavy vs light) | +57.9pp | Maior driver encontrado |
| Newsletter aberta | +7.3pp | Unico driver externo forte |
| Streak day | +3.6pp (streak 1 → 5) | Moderado |
| Resultado (win vs lose) | +1.9pp | Baixo |

---

## 6. Insights principais

1. **D+1 e baixo e homogeneo.** Nenhuma variavel de sessao explica grandes diferencas em D+1. O resultado do jogo, surpreendentemente, e irrelevante.

2. **Newsletter nao traz o usuario amanha, mas mantem ele.** D+1 e igual entre quem abre e nao abre. Mas D30 e 7.3pp maior. A newsletter e ferramenta de retencao de longo prazo, nao de engajamento diario.

3. **O maior divisor de aguas e a frequencia de jogo.** Heavy users (10% da base) tem D30 de 76.4%. Light users (52% da base) tem D30 de 18.5%. A pergunta certa nao e "o que faz voltar amanha" e sim "o que faz jogar a segunda vez".

4. **Streak tem efeito real mas modesto.** D+1 sobe de 21.7% para 29.8% ao longo de 5 dias de streak. O problema e que 78% das sessoes sao streak 1 — usuarios sem habito algum.

5. **O maior ganho potencial esta em converter light → medium.** Se 20% dos 6.300 light users jogarem uma segunda vez, o impacto em D30 da base pode subir 5-8pp.

---

## 7. Recomendacoes

### 7.1 Hipoteses e experimentos

**Hipotese 1: Nudge para segunda sessao em light users**

Acredito que 52% dos usuarios jogam uma unica vez e nunca mais voltam. Um estimulo no momento certo pode reverter isso.

*Acao:* Push notification 24h apos a primeira sessao: "Nova palavra do dia te esperando!".

*Criterio de sucesso:* Taxa de segunda sessao em light users subir de ~12% para >= 25%.

---

**Hipotese 2: Streak counter visivel com recompensa**

Acredito que D+1 sobe com streak (21.7% → 29.8%) e podemos acelerar essa curva tornando o progresso visivel.

*Acao:* Implementar contador de streak com mensagem "So mais X dias para seu recorde!".

*Criterio de sucesso:* % de sessoes em streak >= 3 subir de ~5% para >= 10%.

---

**Hipotese 3: Integrar newsletter ao jogo para aumentar D30**

Acredito que usuarios que abrem a newsletter tem D30 7.3pp maior. Se mais jogadores virarem leitores da newsletter, a retencao de longo prazo sobe.

*Acao:* Adicionar ao fim do jogo um teaser da newsletter com CTA "Receba o jogo e as noticias por email todo dia".

*Criterio de sucesso:* 5% de conversao de nao-assinantes em 30 dias e D30 do grupo exposto >= 35%.

---

**Hipotese 4: Consolo pos-derrota para segurar o usuario**

Acredito que, mesmo D+1 sendo similar entre win e lose, a experiencia de derrota pode ser melhorada para nao desengajar o usuario de longo prazo.

*Acao:* Tela pos-derrota com curiosidade sobre a palavra e incentivo "Amanha tem uma nova!".

*Criterio de sucesso:* D30 de perdedores subir de 30.8% para >= 35%.

---

### 7.2 Priorizacao

| Experimento | Esforco | Impacto esperado | Prioridade |
|---|---|---|---|
| Nudge light users | Baixo | Alto (52% da base, maior gap) | 1 |
| Streak counter visivel | Baixo | Medio (+8pp em D+1) | 1 |
| Integracao newsletter | Medio | Medio (+7.3pp em D30) | 2 |
| Consolo pos-derrota | Baixo | Baixo (D+1 ja e similar) | 3 |

---

## 8. LTV estimado por segmento

| Segmento | Usuarios | Retencao D30 | Sessoes/ano (estimado) | Sessoes totais/ano |
|---|---|---|---|---|
| Heavy (6+ jogos) | ~1.200 | 76.4% | ~110 | ~132.000 |
| Medium (2-5) | ~4.500 | 47.8% | ~25 | ~112.500 |
| Light (1) | ~6.300 | 18.5% | ~3 | ~18.900 |

Heavy users (10% da base) geram ~50% das sessoes anuais. Um heavy user vale ~37x mais sessoes/ano que um light user. Converter light → medium adicionaria ~27.700 sessoes/ano.

---

## 9. Proximos passos

1. Implementar experimentos 1 e 2 na proxima sprint (baixo esforco, maior impacto)
2. Configurar tracking para medir D+1 e D30 por coorte de experimento
3. Investigar por que a retencao D+1 e baixa e homogenea — talvez o produto nao tenha mecanismo de recompensa diaria
4. Coletar mais dados de perfil (survey dentro do app)
5. Analise de coorte continua para monitorar tendencia

---

## Anexo: figuras geradas

`reports/figures/`: 12 graficos incluindo curva de retencao, coorte semanal, heatmap de correlacoes, ranking de features e analises por perfil.
