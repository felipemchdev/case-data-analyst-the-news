# Case - Analista de Dados Produto & Growth | the news

Analise de retencao do Palavritas, jogo de palavras diario do the news.

## Estrutura

```
the-news-case/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                  (palavritas_sessions.csv, palavritas_attempts.csv, user_profile.csv)
│   └── processed/            (dados limpos apos rodar o notebook)
├── notebooks/
│   └── exploration.ipynb     (notebook principal com todas as analises)
├── src/
│   ├── __init__.py           (imports centralizados)
│   ├── load.py               (carregamento dos CSVs)
│   ├── cleaning.py           (diagnostico e limpeza separados)
│   ├── analysis.py           (analises: retencao, coorte, curva, features)
│   ├── statistics.py         (testes estatisticos, IC, Bonferroni)
│   └── plots.py              (visualizacoes com matplotlib/seaborn)
├── sql/
│   ├── quality_checks.sql    (validacoes de qualidade dos dados)
│   ├── retention.sql         (retencao por dimensao + segmentacao)
│   ├── profile.sql           (perfil dos jogadores)
│   ├── newsletter.sql        (relacao newsletter x jogo)
│   └── word_difficulty.sql   (dificuldade por palavra + agrupamento)
├── reports/
│   ├── figures/              (9 graficos PNG)
│   └── final_report.md       (relatorio executivo com hipoteses e experimentos)
```

## Setup

```bash
pip install -r requirements.txt
jupyter notebook notebooks/exploration.ipynb
```

## Autor

Felipe - Case para Analista de Dados Produto & Growth @ the news
