# Case - Analista de Dados Produto & Growth | the news

Analise de retenção do Palavritas, jogo de palavras diário do the news.

## Estrutura

```
the-news-case/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  (palavritas_sessions.csv, palavritas_attempts.csv, user_profile.csv)
│   └── processed/            (dados limpos após rodar o notebook)
├── notebooks/
│   └── exploration.ipynb     (notebook principal com todas as análises)
├── src/
│   ├── __init__.py           (imports centralizados)
│   ├── load.py               (carregamento dos CSVs)
│   ├── cleaning.py           (diagnóstico e limpeza separados)
│   ├── analysis.py           (análises: retenção, corte, curva, features)
│   ├── statistics.py         (testes estatisticos)
│   └── plots.py              (visualizações com matplotlib)
├── sql/
│   ├── quality_checks.sql    (validações de qualidade dos dados)
│   ├── retention.sql         (retenção por dimensão + segmentação)
│   ├── profile.sql           (perfil dos jogadores)
│   ├── newsletter.sql        (relação newsletter x jogo)
│   └── word_difficulty.sql   (dificuldade por palavra + agrupamento)
├── reports/
│   ├── figures/              (9 graficos PNG)
│   └── final_report.md       (relatório executivo com hipóteses e experimentos)
```

## Setup

```bash
pip install -r requirements.txt
jupyter notebook notebooks/exploration.ipynb
```

## Autor

Felipe - Case para Analista de Dados Produto & Growth @the news
