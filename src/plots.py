import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

FIGS_DIR = Path(__file__).parent.parent / "reports" / "figures"
FIGS_DIR.mkdir(parents=True, exist_ok=True)


def salvar(nome):
    plt.tight_layout()
    caminho = FIGS_DIR / f"{nome}.png"
    plt.savefig(caminho, dpi=150, bbox_inches="tight")
    print(f"Salvo: {caminho}")
    plt.close()


def grafico_retencao_resultado(df):
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, col, titulo in zip(axes, ["d1_pct", "d30_pct"], ["D+1", "D30"]):
        vals = df.set_index("result")[col] * 100
        vals.plot(kind="bar", ax=ax, color=["#2ecc71", "#e74c3c"])
        ax.set_title(f"Retencao {titulo} por Resultado")
        ax.set_ylabel("% Retencao")
        ax.bar_label(ax.containers[0], fmt="%.1f%%")
    salvar("retencao_resultado")


def grafico_retencao_streak(df):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["streak_day"], df["d1_pct"] * 100, "o-", label="D+1", color="#3498db")
    ax.plot(df["streak_day"], df["d30_pct"] * 100, "s-", label="D30", color="#e67e22")
    ax.set_xlabel("Dia da Sequencia")
    ax.set_ylabel("% Retencao")
    ax.set_title("Retencao por Dia da Sequencia")
    ax.legend()
    salvar("retencao_streak")


def grafico_retencao_hora(df):
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.bar(df["session_hour"], df["sessoes"], alpha=0.3, color="gray", label="Sessoes")
    ax1.set_ylabel("Sessoes")
    ax2 = ax1.twinx()
    ax2.plot(df["session_hour"], df["d1_pct"] * 100, "o-", color="#3498db", label="D+1")
    ax2.plot(df["session_hour"], df["d30_pct"] * 100, "s-", color="#e67e22", label="D30")
    ax2.set_ylabel("% Retencao")
    ax1.set_xlabel("Hora do Dia")
    ax1.set_title("Sessoes e Retencao por Hora")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    salvar("retencao_hora")


def grafico_palavras(df):
    ordenado = df.sort_values("win_rate")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    dificeis = ordenado.head(15)
    axes[0].barh(dificeis["word"], dificeis["win_rate"] * 100, color="#e74c3c")
    axes[0].set_title("15 Palavras Mais Dificeis")
    axes[0].set_xlabel("Taxa de Vitoria (%)")

    faceis = ordenado.tail(15)
    axes[1].barh(faceis["word"], faceis["win_rate"] * 100, color="#2ecc71")
    axes[1].set_title("15 Palavras Mais Faceis")
    axes[1].set_xlabel("Taxa de Vitoria (%)")

    salvar("palavras_dificuldade")


def grafico_heatmap(corr):
    fig, ax = plt.subplots(figsize=(9, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, square=True, ax=ax,
                cbar_kws={"shrink": 0.8})
    ax.set_title("Correlacoes entre Variaveis")
    salvar("heatmap")


def grafico_perfil(df, var, titulo, top_n=10):
    top = df.nlargest(top_n, "sessoes")
    fig, ax = plt.subplots(figsize=(max(6, top_n * 0.5), max(4, top_n * 0.35)))
    x = range(len(top))
    w = 0.35
    ax.barh([i - w/2 for i in x], top["d1_pct"] * 100, w, label="D+1", color="#3498db")
    ax.barh([i + w/2 for i in x], top["d30_pct"] * 100, w, label="D30", color="#e67e22")
    ax.set_yticks(x)
    ax.set_yticklabels(top[var])
    ax.set_xlabel("% Retencao")
    ax.set_title(titulo)
    ax.legend()
    salvar(f"perfil_{var}")


def grafico_ranking(features, titulo="Ranking de Associacao com Retencao"):
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#e74c3c" if x < 0 else "#2ecc71" for x in features["correlacao"]]
    ax.barh(features["variavel"], features["correlacao"], color=colors)
    ax.set_xlabel("Correlacao")
    ax.set_title(titulo)
    ax.axvline(0, color="black", linewidth=0.5)
    salvar("ranking")


def grafico_curva_retencao(retention):
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(retention["dia"], retention["retencao"] * 100, "o-", color="#3498db", linewidth=2, markersize=4)
    ax.set_xlabel("Dias desde a primeira sessao")
    ax.set_ylabel("Usuarios ativos (%)")
    ax.set_title("Curva de Retencao Global - Palavritas")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 31)
    ax.set_ylim(0, 45)
    for d in [1, 3, 7, 14, 30]:
        if d in retention["dia"].values:
            v = retention[retention["dia"] == d]["retencao"].values[0] * 100
            ax.annotate(f"D{d}: {v:.1f}%", (d, v), textcoords="offset points", xytext=(0, 10), fontsize=9, color="#2c3e50")
    salvar("curva_retencao")


def grafico_coorte(cohort):
    pivot = cohort.pivot(index="cohort_week", columns="week_number", values="retencao")
    pivot = pivot[pivot.columns[:10]]
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(pivot * 100, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax,
                cbar_kws={"label": "Retencao (%)"}, vmin=0, vmax=100)
    ax.set_title("Retencao por Coorte Semanal (%)")
    ax.set_xlabel("Semana relativa (0 = aquisicao)")
    ax.set_ylabel("Coorte (semana da 1a sessao)")
    salvar("coorte")

