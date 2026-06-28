"""Testes automatizados para os modulos do case Palavritas."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from src.load import load_sessions, load_attempts, load_user_profile, save_cleaned
from src.cleaning import DiagnosticLog, diagnosticar_sessions, diagnosticar_attempts, diagnosticar_profile
from src.cleaning import limpar_sessions, limpar_attempts, limpar_profile, rodar_diagnostico
from src.statistics import teste_z_proporcoes, ic_proporcao, ranking_correlacao, teste_t, teste_chi2


def test_load_files_exist():
    s = load_sessions()
    a = load_attempts()
    p = load_user_profile()
    assert len(s) > 0, "sessions vazio"
    assert len(a) > 0, "attempts vazio"
    assert len(p) > 0, "profile vazio"


def test_diagnostic_log():
    log = DiagnosticLog()
    log.log("teste")
    assert "teste" in log.relatorio()
    assert len(log.entries) == 1


def test_limpar_sessions():
    s = load_sessions()
    s_clean = limpar_sessions(s)
    assert len(s_clean) <= len(s), "limpeza deveria manter ou reduzir linhas"
    assert s_clean["device"].isin(["Android", "iOS"]).all(), "device nao normalizado"
    assert s_clean["attempts"].between(1, 6).all(), "tentativas fora do range"
    assert pd.api.types.is_datetime64_any_dtype(s_clean["word_date"]), "word_date nao e datetime"


def test_limpar_attempts():
    a = load_attempts()
    a_clean = limpar_attempts(a)
    assert a_clean["attempt_number"].between(1, 6).all()
    assert a_clean["correct_letters"].between(0, 5).all()
    assert a_clean["correct_positions"].between(0, 5).all()


def test_limpar_profile():
    p = load_user_profile()
    p_clean = limpar_profile(p)
    assert p_clean["orders_food_delivery"].dtype == bool
    assert p_clean["plays_other_word_games"].dtype == bool
    assert p_clean["newsletter_subscriber"].dtype == bool
    assert p_clean["food_delivery_freq_week"].dtype in (np.int32, np.int64)
    assert not p_clean["age_range"].isnull().any(), "age_range ainda tem nulos"
    assert not p_clean["salary_range"].isnull().any(), "salary_range ainda tem nulos"


def test_rodar_diagnostico():
    s, a, p = rodar_diagnostico()
    assert len(s) > 0
    assert len(a) > 0
    assert len(p) > 0
    assert s["device"].isin(["Android", "iOS"]).all()


def test_teste_z_proporcoes():
    r = teste_z_proporcoes(80, 100, 20, 100)
    assert "z" in r
    assert "p_valor" in r
    assert r["significativo"] is True or r["significativo"] == True


def test_ic_proporcao():
    r = ic_proporcao(50, 100)
    assert r["ic_inferior"] > 0
    assert r["ic_superior"] < 1


def test_ranking_correlacao():
    df = pd.DataFrame({
        "a": [1, 2, 3, 1, 2],
        "b": [2, 4, 6, 2, 4],
        "c": [5, 1, 3, 7, 2],
    })
    corr = df.corr()
    ranking = ranking_correlacao(corr, "a")
    assert ranking.iloc[0]["variavel"] == "b", "b deveria ter maior correlacao com a"
    assert ranking.iloc[0]["correlacao"] == 1.0


def test_save_cleaned(tmp_path):
    s = load_sessions().head(10)
    a = load_attempts().head(10)
    p = load_user_profile().head(10)
    import src.load as lm
    old_dir = lm.PROCESSED_DIR
    lm.PROCESSED_DIR = tmp_path
    save_cleaned(s, a, p)
    assert (tmp_path / "sessions_clean.csv").exists()
    assert (tmp_path / "attempts_clean.csv").exists()
    assert (tmp_path / "profile_clean.csv").exists()
    lm.PROCESSED_DIR = old_dir


if __name__ == "__main__":
    test_load_files_exist()
    print("OK: load_files_exist")
    test_diagnostic_log()
    print("OK: diagnostic_log")
    test_limpar_sessions()
    print("OK: limpar_sessions")
    test_limpar_attempts()
    print("OK: limpar_attempts")
    test_limpar_profile()
    print("OK: limpar_profile")
    test_rodar_diagnostico()
    print("OK: rodar_diagnostico")
    test_teste_z_proporcoes()
    print("OK: teste_z_proporcoes")
    test_ic_proporcao()
    print("OK: ic_proporcao")
    test_ranking_correlacao()
    print("OK: ranking_correlacao")
    print("\nTODOS OS TESTES PASSARAM!")
