import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List


def teste_chi2(tabela: pd.DataFrame) -> Dict:
    """Teste qui-quadrado de independencia."""
    chi2, p, dof, esperado = stats.chi2_contingency(tabela)
    return {"chi2": chi2, "p_valor": p, "dof": dof, "significativo": p < 0.05}


def teste_t(grupo_a: np.ndarray, grupo_b: np.ndarray) -> Dict:
    """Teste t de Welch (variancias desiguais) entre dois grupos independentes."""
    t, p = stats.ttest_ind(grupo_a, grupo_b, equal_var=False)
    d = tamanho_efeito_cohen(grupo_a, grupo_b)
    return {"t": float(t), "p_valor": float(p), "media_a": float(np.mean(grupo_a)), "media_b": float(np.mean(grupo_b)),
            "cohens_d": d, "significativo": p < 0.05}


def teste_z_proporcoes(sucessos1: int, total1: int, sucessos2: int, total2: int) -> Dict:
    """Teste Z para diferenca entre duas proporcoes (bicaudal)."""
    p1 = sucessos1 / total1
    p2 = sucessos2 / total2
    p_pool = (sucessos1 + sucessos2) / (total1 + total2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / total1 + 1 / total2))
    z = (p1 - p2) / se
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return {"z": float(z), "p_valor": float(p), "prop_a": p1, "prop_b": p2, "significativo": p < 0.05}


def ic_proporcao(sucessos: int, total: int, confianca: float = 0.95) -> Dict:
    """Intervalo de confianca para uma proporcao (metodo Wald)."""
    p = sucessos / total
    z = stats.norm.ppf(1 - (1 - confianca) / 2)
    erro = z * np.sqrt(p * (1 - p) / total)
    return {"proporcao": p, "ic_inferior": max(0, p - erro), "ic_superior": min(1, p + erro), "confianca": confianca}


def tamanho_efeito_cohen(grupo_a: np.ndarray, grupo_b: np.ndarray) -> float:
    """Cohen's d para tamanho de efeito entre dois grupos."""
    n1, n2 = len(grupo_a), len(grupo_b)
    s1, s2 = np.var(grupo_a, ddof=1), np.var(grupo_b, ddof=1)
    s_pool = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    if s_pool == 0:
        return 0.0
    return float((np.mean(grupo_a) - np.mean(grupo_b)) / s_pool)


def ranking_correlacao(matriz_corr: pd.DataFrame, alvo: str) -> pd.DataFrame:
    """Ranking das variaveis com maior correlacao (absoluta) com uma variavel alvo."""
    corr = matriz_corr[alvo].drop(alvo).sort_values(key=abs, ascending=False)
    return pd.DataFrame({
        "variavel": corr.index,
        "correlacao": corr.values,
        "abs_corr": corr.abs().values,
    }).sort_values("abs_corr", ascending=False)


def teste_anova(df: pd.DataFrame, col_grupo: str, col_alvo: str) -> Dict:
    """ANOVA one-way entre grupos."""
    grupos = [g[col_alvo].dropna().values for _, g in df.groupby(col_grupo)]
    f, p = stats.f_oneway(*grupos)
    return {"f": float(f), "p_valor": float(p), "significativo": p < 0.05}


def correcao_bonferroni(p_valores: List[float]) -> List[float]:
    """Aplica correcao de Bonferroni em uma lista de p-valores."""
    n = len(p_valores)
    return [min(p * n, 1.0) for p in p_valores]
