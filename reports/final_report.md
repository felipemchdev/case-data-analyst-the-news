# Palavritas: o que determina se um usuario volta a jogar?

**Case para Analista de Dados Produto & Growth - the news**

---

## 1. Objetivo

Entender quais variaveis mais se associam com o usuario voltar a jogar no dia seguinte (D+1) e estar ativo apos 30 dias (D30), e propor acoes concretas para aumentar a retencao.

---

## 2. Entendimento do problema

O Palavritas e um jogo diario de palavras. O usuario pode jogar uma vez por dia, com ate 6 tentativas. A pergunta central do Head de Produto e: o que faz um usuario criar o habito de voltar?

Para responder, separei em quatro camadas:

1. Comportamento dentro da sessao (resultado, tempo, hora, streak)
2. Relacao com a newsletter (abriu antes de jogar?)
3. Perfil do usuario (setor, salario, device, habitos)
4. Padroes longitudinais (curva de retencao, coortes, segmentacao)

---

## 3. Qualidade dos dados

### 3.1 Problemas encontrados e decisoes

| Problema | Decisao | Impacto |
|---|---|---|
| Datas em formato misto (ISO `2026-01-15` e `DD/MM/YYYY`) | Parse duplo com fallback. 0 linhas perdidas | Resolvido |
| `attempts = 7` em uma sessao | Removida (fora do range esperado 1-6) | 1 linha removida |
| `device` inconsistente (`Android`, `android`, `ios`, `iOS`, `iphone os`) | Normalizado para `Android` e `iOS`. Não mapeados assumidos Android | Resolvido |
| `user_profile` com 800 usuarios vs ~12k usuarios unicos em sessions | Apenas ~6% tem perfil. Analises de perfil tem amostra reduzida | Limitacao documentada |
| `orders_food_delivery` com "sim"/"nao"/"True"/"False" misturados | Normalizado para booleano | Resolvido |
| `plays_other_word_games` e `newsletter_subscriber` com strings inconsistentes | Normalizado para booleano | Resolvido |
| `age_range` e `salary_range` com ~15% nulos | Preenchidos como "Nao informado" | Resolvido |
| `state` com nome por extenso ("Sao Paulo", "Minas Gerais") ao inves de UF | Mantido (baixo impacto na analise principal) | Cosmetico |
| Caracteres quebrados (`DANçA`, `PAZAO`) em palavras com acentos | Encoding do CSV original. Nao corrigido, palavras sao identificaveis | Cosmetico |

### 3.2 Tamanho final dos datasets

- `palavritas_sessions`: ~41.000 sessoes, ~12.000 usuarios unicos (periodo: dez/2025 a mai/2026)
- `palavritas_attempts`: ~149.000 tentativas
- `user_profile`: 800 usuarios (normalizados para booleano e com nulos preenchidos)

---

## 4. Analises

### 4.1 Ganhar ou perder muda a retencao?

| Resultado | Sessoes | D+1 (IC 95%) | D30 (IC 95%) | Media tentativas |
|---|---|---|---|---|
| Win | ~33.000 | 38.2% [37.7%, 38.7%] | 41.8% [41.3%, 42.3%] | 2.3 |
| Lose | ~8.000 | 21.1% [20.2%, 22.0%] | 31.4% [30.4%, 32.4%] | 6.0 |

Ganhar quase dobra a chance de voltar no dia seguinte. A diferenca e estatisticamente significativa (teste Z, z=28.4, p < 0.001, corrigido por Bonferroni). O efeito em D30 e similar, porem menos intenso (diferenca de ~10pp).

**Interpretacao:** o resultado e o fator mais impactante. Perder desengaja. Mas 21% dos que perdem ainda voltam - tem oportunidade ai.

---

### 4.2 Streak: o efeito habito

| Streak Day | Sessoes | D+1 | D30 |
|---|---|---|---|
| 1 | ~38.000 | 32.4% | 38.1% |
| 2 | ~2.500 | 48.6% | 52.3% |
| 3 | ~400 | 84.1% | 85.2% |
| 4 | ~100 | 67.3% | 72.1% |
| 5 | ~20 | 57.9% | 64.0% |

A retencao dispara no dia 3 da sequencia. Quem chega no terceiro dia seguido tem 84% de chance de voltar - e isso se mantem alto. O problema e que pouquissimos chegam la: menos de 3% das sessoes estao em streak >= 2.

**Interpretacao:** o habito se forma no terceiro dia. O funil de streak e o gargalo principal: de ~38k sessoes no dia 1, apenas ~2.500 chegam ao dia 2.

---

### 4.3 Existe um horario ideal?

| Hora | Sessoes | D+1 | D30 | Win Rate |
|---|---|---|---|---|
| 6-9h | ~17.000 | 36.0% | 41.2% | 81.7% |
| 10-14h | ~5.000 | 32.1% | 36.4% | 79.6% |
| 15-19h | ~10.000 | 35.2% | 40.1% | 78.9% |
| 20-23h | ~9.000 | 32.4% | 37.2% | 80.3% |

A manha (6h-9h) concentra mais sessoes (41%) e tem retencao levemente superior. A diferenca entre o melhor e o pior horario e de apenas 4pp em D+1. Nao e o fator decisivo.

**Interpretacao:** o horario importa pouco para retencao. Importa mais para estrategia de push.

---

### 4.4 Device: Android vs iOS

| Device | Sessoes | D+1 | D30 | Win Rate |
|---|---|---|---|---|
| Android | ~24.500 | 34.1% | 38.9% | 79.8% |
| iOS | ~16.500 | 33.8% | 39.6% | 81.1% |

Praticamente identico. Device nao explica retencao.

---

### 4.5 Newsletter: abrir antes de jogar ajuda?

| Abriu newsletter? | Sessoes | D+1 (IC 95%) | D30 (IC 95%) |
|---|---|---|---|
| Sim | ~10.500 | 40.8% [39.9%, 41.7%] | 46.2% [45.2%, 47.2%] |
| Nao | ~30.500 | 31.8% [31.3%, 32.3%] | 37.6% [37.1%, 38.1%] |

Usuarios que abrem a newsletter antes do jogo tem D+1 de 40.8% contra 31.8% de quem nao abre. Diferenca de 9pp, significativa (z=16.8, p < 0.001).

**Interpretacao:** a newsletter e um sinal forte de engajamento com o ecossistema the news. A integracao newsletter -> jogo funciona como alavanca de retencao.

### 4.5.1 Funil de engajamento

Olhando os dados como funil (acoes dentro da mesma sessao), temos:

| Etapa | Sessoes | % da etapa anterior | % do total |
|---|---|---|---|
| Sessao iniciada | 39.849 | 100% | 100% |
| Abriu newsletter antes | 7.651 | 19% | 19% |
| Ganhou o jogo | 24.043 | (independente) | 60% |
| Voltou D+1 | 8.823 | 37% dos que ganharam | 22% |

A maior queda esta entre "sessao iniciada" e "abriu newsletter" — apenas 19% dos jogadores abrem a newsletter antes de jogar. Isso sugere que a newsletter nao e o principal canal de entrada no jogo — talvez o app ou notificacoes sejam.

---

### 4.5.2 Stickiness e uso diario

| Metrica | Valor |
|---|---|
| DAU medio (jogadores/dia) | 221 |
| WAU medio (jogadores/semana) | 1.533 |
| MAU medio (jogadores/mes) | 6.642 |
| Stickiness (DAU/MAU) | 3.3% |

Stickiness de 3.3% significa que, em media, apenas 3.3% dos usuarios mensais jogam em um dia qualquer. Para um jogo diario, esse numero e baixo — indica que a maioria dos 6.600 MAU joga com baixa frequencia. O benchmark de referencia para apps de jogo e 10-20%.

**Interpretacao:** o produto tem alcance (MAU razoavel) mas baixa recorrência diaria. Converter usuarios ocasionais em daily active users e a maior alavanca de crescimento.

---

### 4.6 Palavras dificeis derrubam retencao?

As palavras foram agrupadas por dificuldade baseada em win_rate:

| Dificuldade | Win Rate medio | Palavras | D+1 medio |
|---|---|---|---|
| Dificil (win rate < 70%) | ~62% | ~25 | 29.8% |
| Media (70-85%) | ~78% | ~50 | 34.2% |
| Facil (> 85%) | ~93% | ~55 | 37.5% |

Palavras dificeis reduzem D+1 em ~8pp comparado com palavras faceis. A correlacao entre win_rate da palavra e D+1 e r=0.31 (p<0.01).

**Interpretacao:** calibrar a dificuldade da palavra do dia impacta diretamente quantos voltam amanha.

---

### 4.7 Curva de Retencao Global

| Dia | Usuarios ativos (%) |
|---|---|
| D1 | 38.5% |
| D3 | 14.2% |
| D7 | 6.8% |
| D14 | 3.5% |
| D30 | 1.8% |

A queda mais acentuada ocorre entre D1 e D3 (-24pp). Quem sobrevive ao terceiro dia tem retencao mais estavel.

**Interpretacao:** os primeiros 3 dias sao a janela critica. Se conseguirmos aumentar D3 em 5pp, o efeito cascata em D30 e significativo.

---

### 4.8 Analise de Coorte Semanal

Coortes mais recentes (abr-mai/2026) apresentam retencao levemente superior as coortes iniciais (dez/2025). A retencao na Semana 1 varia entre 20-30% entre coortes, caindo para 5-10% na Semana 4.

**Interpretacao:** produto esta melhorando ao longo do tempo (possivelmente ajustes de UX ou qualidade das palavras). As coortes mais antigas servem como baseline historica; as mais recentes como benchmark.

---

### 4.9 Segmentacao de Usuarios (heavy/medium/light)

| Segmento | Usuarios | Sessoes medias | D1 medio | D30 medio | Win Rate | Streak Max |
|---|---|---|---|---|---|---|
| Heavy (6+ jogos) | ~1.200 | 9.2 | 68.1% | 76.4% | 87.3% | 3.1 |
| Medium (2-5) | ~4.500 | 2.8 | 42.3% | 47.8% | 81.2% | 1.4 |
| Light (1) | ~6.300 | 1.0 | 12.4% | 18.5% | 78.9% | 1.0 |

Heavy users representam apenas 10% da base mas tem D30 de 76%. Light users sao 52% da base com D30 de apenas 18.5%.

**Interpretacao:** o maior ganho potencial esta em converter light -> medium. Se 20% dos light users jogarem uma segunda vez, o impacto em D30 da base pode subir 5-8pp.

---

### 4.10 Perfil do usuario (base: 800 usuarios com survey)

| Variavel | Maior D30 | Menor D30 |
|---|---|---|
| Faixa salarial | acima de R$10k (52%) | ate R$2k (35%) |
| Setor | tech (45%) | direito (35%) |
| Faixa etaria | 45+ (44%) | 18-24 (36%) |
| Horario tipico | morning (43%) | night (36%) |
| Joga outras word games | Sim (42%) | Nao (37%) |
| Assinante newsletter | Sim (42%) | Nao (35%) |
| Pede comida | Sim (42%) | Nao (37%) |

ANOVA confirma diferencas significativas entre faixas salariais (F=3.21, p=0.013) e setores (F=2.45, p=0.028) para D30. A base de perfil e pequena (6% dos usuarios), mas os padroes sao consistentes com as analises de comportamento.

**Interpretacao:** usuarios de maior renda, setor tech, que jogam de manha e sao assinantes da newsletter tendem a reter mais. Sao early adopters. O desafio e trazer usuarios fora desse perfil.

---

## 5. Ranking final: o que mais se associa com retencao?

### Para voltar no dia seguinte (D+1):

| Variavel | Correlacao | Associacao |
|---|---|---|
| streak_day | +0.18 | Muito alta |
| newsletter_open | +0.09 | Alta |
| win (vitoria) | +0.08 | Alta |
| word win_rate | +0.06 | Media |
| session_hour (manha) | +0.03 | Baixa |
| device_Android | -0.01 | Muito baixa |

### Para estar ativo em 30 dias (D30):

| Variavel | Correlacao | Associacao |
|---|---|---|
| streak_day | +0.12 | Muito alta |
| newsletter_open | +0.09 | Alta |
| win (vitoria) | +0.07 | Media |
| plays_other_games | +0.04 | Baixa |
| assinante_news | +0.03 | Baixa |
| salary_rank | +0.02 | Muito baixa |

---

## 6. Insights principais

1. **Ganhar importa, mas nao resolve tudo.** Quem perde tem 21% de D+1. Se subirmos para 28%, o ganho em volume e enorme (8.000 sessoes).

2. **O habito se forma no dia 3. Mas o funil e um gargalo.** Apenas 6.5% das sessoes do dia 1 chegam ao dia 2. A curva de retencao mostra queda de 38% para 14% entre D1 e D3.

3. **A newsletter e uma alavanca de retencao subestimada.** +9pp em D+1 e D30 para quem abre. A integracao entre os dois produtos e uma oportunidade clara.

4. **Palavras dificeis tem efeito cascata.** D+1 cai 8pp entre palavras faceis e dificeis.

5. **Light users sao 52% da base com D30 de apenas 18.5%.** Converter 20% deles para medium users seria o maior ganho de retencao possivel.

6. **As coortes estao melhorando.** Coortes recentes tem retencao superior, sugerindo que ajustes no produto ja estao surtindo efeito.

---

### 6.7 LTV estimado por segmento

Como nao temos dados de receita por usuario, fiz uma estimativa simples de sessoes vitalicias usando a retencao observada. Multipliquei a retencao media de cada segmento por 12 meses para projetar sessoes/ano.

| Segmento | Usuarios | Retencao D30 | Sessoes/ano (estimado) | Sessoes totais/ano |
|---|---|---|---|---|
| Heavy (6+ jogos) | ~1.200 | 76.4% | ~110 | ~132.000 |
| Medium (2-5) | ~4.500 | 47.8% | ~25 | ~112.500 |
| Light (1) | ~6.300 | 18.5% | ~3 | ~18.900 |

Heavy users representam 10% da base mas geram ~50% das sessoes anuais projetadas. Um heavy user vale ~37x mais sessoes/ano que um light user.

Se o the news monetiza por volume de audiencia (ex: anuncios na newsletter, branded content), heavy users sao o ativo mais valioso. E se cada light user convertido a medium gera +22 sessoes/ano, converter 20% dos light users (~1.260 usuarios) adicionaria ~27.700 sessoes/ano.

---

## 7. Recomendacoes

### 7.1 Hipoteses e experimentos

**Hipotese 1: Um "consolo" para quem perde aumenta D+1**

Acredito que quem perde abandona porque a experiencia termina em frustracao. Se oferecermos algo positivo apos a derrota, a retencao sobe.

*Acao:* Mostrar uma tela pos-derrota com curiosidade sobre a palavra do dia, estatisticas pessoais ou um "tente amanha, a palavra sera mais facil".

*Criterio de sucesso:* D+1 entre perdedores subir de 21.1% [IC: 20.2-22.0%] para >= 28%.

---

**Hipotese 2: Recompensar streak nos dias 2 e 3 dobra a chegada ao dia 3**

Acredito que usuarios nao sentem progresso suficiente entre os dias 1 e 3. Uma recompensa visivel aumenta a motivacao.

*Acao:* Implementar contador de streak com mensagem de incentivo ("So mais 1 dia para seu recorde!").

*Criterio de sucesso:* % de sessoes em streak >= 3 subir de ~1.3% para >= 4%.

---

**Hipotese 3: Conectar newsletter ao jogo aumenta engajamento cruzado**

Acredito que usuarios que nao abrem a newsletter tem menor retencao porque nao tem o gatilho diario.

*Acao:* Adicionar ao fim do jogo um teaser da newsletter com CTA "Receba o jogo por email todo dia".

*Criterio de sucesso:* 5% de conversao de nao-assinantes em 30 dias e D+1 do grupo exposto >= 35%.

---

**Hipotese 4: Nudge para segunda sessao em light users**

Acredito que 52% dos usuarios que jogam uma unica vez podem ser reativados com um estímulo temporal certo.

*Acao:* Push notification 24h apos a primeira sessao: "Nova palavra do dia te esperando!".

*Criterio de sucesso:* Taxa de segunda sessao em light users subir de ~12% para >= 25%.

---

### 7.2 Priorizacao

| Experimento | Esforco | Impacto esperado | Prioridade |
|---|---|---|---|
| Consolo pos-derrota | Baixo | Alto (+7pp D+1 em 20% da base) | 1 |
| Streak counter visivel | Baixo | Alto (dobra streak>=3) | 1 |
| Nudge light users | Baixo | Alto (52% da base) | 1 |
| Integracao newsletter | Medio | Medio | 2 |
| Dificuldade adaptativa | Alto | Medio | 3 |

---

## 8. Proximos passos

1. Implementar experimentos 1, 2 e 4 na proxima sprint (baixo esforco, alto impacto)
2. Configurar tracking para medir D+1 e D30 por coorte de experimento
3. Coletar mais dados de perfil (survey dentro do app) para reduzir vies de selecao
4. Investigar com qual: usuarios que jogam e nao abrem newsletter - o que mais consomem?
5. Analise de coorte continua para monitorar tendencia de melhoria do produto

---

## Anexo: figuras geradas

Todas as figuras estao em `reports/figures/`:

- `retencao_resultado.png` - barras win/lose vs D+1 e D30
- `retencao_streak.png` - linha de retencao por streak day
- `retencao_hora.png` - sessoes e retencao por hora
- `palavras_dificuldade.png` - palavras mais dificeis e mais faceis
- `heatmap.png` - correlacoes entre variaveis
- `ranking.png` - ranking de features vs D+1
- `curva_retencao.png` - curva de retencao D1 a D30
- `coorte.png` - heatmap de retencao por coorte semanal
- `perfil_*.png` - retencao por variaveis de perfil
