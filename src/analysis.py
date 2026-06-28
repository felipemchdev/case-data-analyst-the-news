import pandas as pd
import numpy as np


def retencao_por_resultado(df: pd.DataFrame) -> pd.DataFrame:
    """Retencao D+1 e D30 agrupada por resultado (win/lose)."""
    return df.groupby("result").agg(
        sessoes=("session_id", "count"),
        d1_pct=("played_next_day", "mean"),
        d30_pct=("active_d30", "mean"),
        media_tentativas=("attempts", "mean"),
        media_tempo=("time_to_complete_sec", "mean"),
    ).reset_index()


def retencao_por_streak(df: pd.DataFrame) -> pd.DataFrame:
    """Retencao D+1 e D30 por dia da sequencia (streak_day)."""
    return df.groupby("streak_day").agg(
        sessoes=("session_id", "count"),
        d1_pct=("played_next_day", "mean"),
        d30_pct=("active_d30", "mean"),
    ).reset_index()


def retencao_por_hora(df: pd.DataFrame) -> pd.DataFrame:
    """Retencao D+1, D30 e win_rate por hora do dia."""
    return df.groupby("session_hour").agg(
        sessoes=("session_id", "count"),
        d1_pct=("played_next_day", "mean"),
        d30_pct=("active_d30", "mean"),
        win_rate=("result", lambda x: (x == "win").mean()),
    ).reset_index()


def retencao_por_device(df: pd.DataFrame) -> pd.DataFrame:
    """Retencao D+1, D30 e win_rate por dispositivo."""
    return df.groupby("device").agg(
        sessoes=("session_id", "count"),
        d1_pct=("played_next_day", "mean"),
        d30_pct=("active_d30", "mean"),
        win_rate=("result", lambda x: (x == "win").mean()),
    ).reset_index()


def retencao_por_newsletter(df: pd.DataFrame) -> pd.DataFrame:
    """Retencao D+1 e D30 cruzando abertura da newsletter antes do jogo."""
    return df.groupby("newsletter_open_before_game").agg(
        sessoes=("session_id", "count"),
        d1_pct=("played_next_day", "mean"),
        d30_pct=("active_d30", "mean"),
        win_rate=("result", lambda x: (x == "win").mean()),
    ).reset_index()


def dificuldade_por_palavra(df: pd.DataFrame) -> pd.DataFrame:
    """Dificuldade de cada palavra: win_rate, tentativas medias, retencao."""
    return df.groupby("word").agg(
        sessoes=("session_id", "count"),
        win_rate=("result", lambda x: (x == "win").mean()),
        media_tentativas=("attempts", "mean"),
        d1_pct=("played_next_day", "mean"),
        d30_pct=("active_d30", "mean"),
    ).reset_index().sort_values("win_rate")


def juntar_sessions_profile(sessions: pd.DataFrame, profile: pd.DataFrame) -> pd.DataFrame:
    """Merge entre sessions e user_profile (inner join)."""
    return sessions.merge(profile, on="user_id", how="inner")


def retencao_por_perfil(df: pd.DataFrame, variavel: str) -> pd.DataFrame:
    """Retencao D+1 e D30 agrupada por uma variavel categorica de perfil."""
    return df.groupby(variavel).agg(
        sessoes=("session_id", "count"),
        d1_pct=("played_next_day", "mean"),
        d30_pct=("active_d30", "mean"),
    ).reset_index().sort_values("sessoes", ascending=False)


def padrao_tentativas(attempts: pd.DataFrame, sessions: pd.DataFrame) -> pd.DataFrame:
    """Evolucao de correct_positions e correct_letters ao longo das tentativas, por resultado."""
    merged = attempts.merge(sessions[["session_id", "result"]], on="session_id")
    return (
        merged.groupby(["result", "attempt_number"])
        .agg(
            media_corretas=("correct_positions", "mean"),
            media_letras=("correct_letters", "mean"),
            contagem=("session_id", "count"),
        )
        .reset_index()
    )


def matriz_correlacao(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz de correlacao de Pearson entre variaveis numericas e binarias do jogo."""
    vars_df = df[[
        "attempts", "time_to_complete_sec", "session_hour", "streak_day",
        "played_next_day", "active_d30", "newsletter_open_before_game"
    ]].copy()
    vars_df["win"] = (df["result"] == "win").astype(int)
    return vars_df.corr()


def tabela_features(sessions: pd.DataFrame, profile: pd.DataFrame) -> pd.DataFrame:
    """Tabela unificada com dummies de device e horario para ranking de correlacoes."""
    df = sessions.merge(profile, on="user_id", how="left")

    dummies = pd.get_dummies(df["device"], prefix="device")
    time_dummies = pd.get_dummies(df["typical_play_time"].fillna("desconhecido"), prefix="horario")

    salary_map = {
        "ate R$2k": 1, "R$2k-R$4k": 2, "R$4k-R$6k": 3,
        "R$6k-R$10k": 4, "acima de R$10k": 5,
        "Nao informado": 0,
    }

    features = pd.DataFrame({
        "tentativas": df["attempts"],
        "tempo_total": df["time_to_complete_sec"],
        "hora": df["session_hour"],
        "streak": df["streak_day"],
        "vitoria": (df["result"] == "win").astype(int),
        "abriu_newsletter": df["newsletter_open_before_game"].astype(int),
        "jogou_dia_seguinte": df["played_next_day"].astype(int),
        "ativo_d30": df["active_d30"].astype(int),
        "salario_rank": df["salary_range"].map(salary_map).fillna(0),
        "joga_outros": df["plays_other_word_games"].fillna(False).astype(int),
        "assinante_news": df["newsletter_subscriber"].fillna(False).astype(int),
        "pede_comida": df["orders_food_delivery"].fillna(False).astype(int),
    })

    features = pd.concat([features, dummies, time_dummies], axis=1)
    return features


def analise_coorte(sessions: pd.DataFrame) -> pd.DataFrame:
    """Tabela de retencao por coorte semanal (semana de primeira sessao)."""
    user_first = sessions.groupby("user_id")["word_date"].min().reset_index()
    user_first.columns = ["user_id", "cohort_week"]
    user_first["cohort_week"] = user_first["cohort_week"].dt.to_period("W")

    df = sessions.merge(user_first, on="user_id")
    df["session_week"] = df["word_date"].dt.to_period("W")
    df["week_number"] = (df["session_week"] - df["cohort_week"]).apply(lambda x: x.n if hasattr(x, 'n') else 0)

    cohort_size = user_first.groupby("cohort_week")["user_id"].nunique().reset_index()
    cohort_size.columns = ["cohort_week", "tamanho"]

    retention = df.groupby(["cohort_week", "week_number"])["user_id"].nunique().reset_index()
    retention.columns = ["cohort_week", "week_number", "ativos"]

    cohort_table = retention.merge(cohort_size, on="cohort_week")
    cohort_table["retencao"] = cohort_table["ativos"] / cohort_table["tamanho"]

    return cohort_table


def curva_retencao(sessions: pd.DataFrame) -> pd.DataFrame:
    """Curva de retencao global: % de usuarios ativos a cada dia desde a primeira sessao."""
    user_first = sessions.groupby("user_id")["word_date"].min().reset_index()
    user_first.columns = ["user_id", "primeira_data"]

    df = sessions.merge(user_first, on="user_id")
    df["dia"] = (df["word_date"] - df["primeira_data"]).dt.days

    total_users = sessions["user_id"].nunique()
    retention_days = df.groupby("dia")["user_id"].nunique().reset_index()
    retention_days.columns = ["dia", "ativos"]
    retention_days["retencao"] = retention_days["ativos"] / total_users
    retention_days = retention_days[retention_days["dia"] <= 30]

    return retention_days


def retencao_por_usuario(sessions: pd.DataFrame) -> pd.DataFrame:
    """Metricas de retencao a nivel de usuario: total de sessoes, win_rate, streak_max, dias ativo."""
    return sessions.groupby("user_id").agg(
        total_sessoes=("session_id", "count"),
        win_rate=("result", lambda x: (x == "win").mean()),
        streak_max=("streak_day", "max"),
        dias_entre_primeira_e_ultima=("word_date", lambda x: (x.max() - x.min()).days),
        d30_medio=("active_d30", "mean"),
        d1_medio=("played_next_day", "mean"),
        newsletter_rate=("newsletter_open_before_game", "mean"),
    ).reset_index()


def segmentar_usuarios(user_metrics: pd.DataFrame) -> pd.DataFrame:
    """Segmenta usuarios em heavy (6+ sessoes), medium (2-5) e light (1)."""
    conds = [
        user_metrics["total_sessoes"] >= 6,
        user_metrics["total_sessoes"] >= 2,
    ]
    choices = ["heavy", "medium"]
    user_metrics["segmento"] = np.select(conds, choices, default="light")
    return user_metrics


def funil_newsletter_jogo(sessions: pd.DataFrame) -> pd.DataFrame:
    """Funil de engajamento a nivel de sessao: sessao -> abriu newsletter -> ganhou -> voltou D+1."""
    total = len(sessions)
    abriu = int(sessions["newsletter_open_before_game"].sum())
    ganhou = int((sessions["result"] == "win").sum())
    voltou = int(sessions["played_next_day"].sum())

    etapas = pd.DataFrame({
        "etapa": ["Sessoes totais", "Abriu newsletter", "Ganhou", "Voltou D+1"],
        "sessoes": [total, abriu, ganhou, voltou],
    })
    etapas["taxa_etapa_anterior"] = etapas["sessoes"] / etapas["sessoes"].shift(1)
    etapas["taxa_etapa_anterior"] = etapas["taxa_etapa_anterior"].fillna(1.0)
    return etapas


def metrica_stickiness(sessions: pd.DataFrame) -> pd.DataFrame:
    """Calcula DAU, WAU, MAU e stickiness (DAU/MAU) medio no periodo."""
    daily = sessions.groupby("word_date")["user_id"].nunique().reset_index()
    daily.columns = ["data", "dau"]

    daily["semana"] = daily["data"].dt.to_period("W")
    daily["mes"] = daily["data"].dt.to_period("M")

    wau = daily.groupby("semana")["dau"].sum().mean()
    mau = daily.groupby("mes")["dau"].sum().mean()
    dau_medio = daily["dau"].mean()

    stickiness = dau_medio / mau if mau > 0 else 0

    return pd.DataFrame({
        "metrica": ["DAU medio", "WAU medio (soma)", "MAU medio (soma)", "Stickiness (DAU/MAU)"],
        "valor": [round(dau_medio), round(wau), round(mau), f"{stickiness:.1%}"],
    })
