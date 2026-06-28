# Dicionario de Dados - Palavritas

## palavritas_sessions.csv (~41.000 linhas)

| Coluna | Tipo | Descricao | Valores validos |
|---|---|---|---|
| session_id | string | Identificador unico da sessao de jogo | UUID |
| user_id | string | Identificador anonimizado do usuario | UUID |
| word | string | Palavra do desafio do dia | 5 letras |
| word_date | date | Data do desafio | 2025-12-01 a 2026-05-29 |
| attempts | int | Numero de tentativas na sessao | 1 a 6 |
| result | string | Resultado do jogo | win ou lose |
| time_to_complete_sec | int | Tempo total de jogo em segundos | ~60 a ~480 (P1 a P99) |
| device | string | Dispositivo usado | Android ou iOS |
| session_hour | int | Hora do dia em que jogou | 0 a 23 |
| streak_day | int | Dia atual da sequencia do usuario | 1 a 8 (maximo observado) |
| played_next_day | boolean | Se o usuario voltou a jogar no dia seguinte | True ou False |
| newsletter_open_before_game | boolean | Se abriu a newsletter do the news antes de jogar | True ou False |
| active_d30 | boolean | Se o usuario estava ativo 30 dias apos essa sessao | True ou False |

### Notas
- ~1.200 session_id duplicados no raw (removidos na limpeza)
- Datas em formato misto no raw (ISO e DD/MM/YYYY, padronizadas na limpeza)
- 93 linhas com attempts fora do range 1-6 (removidas)
- 63 linhas com result invalido (removidas)
- Período coberto: dezembro/2025 a maio/2026 (~6 meses)

---

## palavritas_attempts.csv (~149.000 linhas)

| Coluna | Tipo | Descricao | Valores validos |
|---|---|---|---|
| session_id | string | FK para palavritas_sessions | UUID |
| attempt_number | int | Numero da tentativa (1 a 6) | 1 a 6 |
| guess | string | Palavra digitada pelo usuario | texto |
| correct_letters | int | Letras corretas em posicao errada | 0 a 5 |
| correct_positions | int | Letras corretas na posicao certa | 0 a 5 |

### Notas
- 41 linhas com attempt_number fora de 1-6 (removidas)
- 12 linhas com correct_letters + correct_positions > 5 (removidas)
- ~40.000 sessions distintas com attempts

---

## user_profile.csv (800 linhas)

| Coluna | Tipo | Descricao | Valores validos | % Nulo (raw) |
|---|---|---|---|---|
| user_id | string | FK para palavritas_sessions | UUID | 0% |
| age_range | string | Faixa etaria | 18-24, 25-34, 35-44, 45+ | 14.6% |
| state | string | Estado (UF) | 2 letras ou nome por extenso | 0% |
| city | string | Cidade | texto | 37.1% |
| salary_range | string | Faixa salarial | ate R$2k, R$2k-R$4k, R$4k-R$6k, R$6k-R$10k, acima de R$10k | 24.1% |
| job_role | string | Cargo | texto | 0% |
| sector | string | Setor de trabalho | texto | 0% |
| company_size | string | Porte da empresa | pequena, media, grande, multinacional, MEI/micro | 0% |
| orders_food_delivery | boolean | Se pede comida por app | True ou False | 0% |
| food_delivery_freq_week | int | Vezes por semana que pede comida | 0 a 7 | 0% |
| food_delivery_platform | string | Plataforma usada | iFood, Rappi, Ambos, Nenhum | 0% |
| primary_device | string | Dispositivo principal | Android, iOS | 0% |
| plays_other_word_games | boolean | Se joga outros jogos de palavras | True ou False | 0% |
| typical_play_time | string | Periodo tipico de jogo | morning, afternoon, evening, night | 0% |
| newsletter_subscriber | boolean | Se e assinante da newsletter do the news | True ou False | 0% |

### Notas
- Apenas 800 usuarios (~6% da base de sessions) tem perfil preenchido
- Valores booleanos normalizados de strings inconsistentes ("sim"/"nao"/"True"/"False") para Python bool
- Campos nulos preenchidos com "Nao informado" (categoricos) ou False (booleanos)
- Estados com nome por extenso mantidos como estao (ex: "Sao Paulo", "Minas Gerais")
- Encoding do CSV raw apresentou caracteres quebrados em acentos (cosmetico, nao corrigido)
