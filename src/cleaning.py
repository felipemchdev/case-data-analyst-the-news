import pandas as pd
from datetime import datetime


class DiagnosticLog:
    def __init__(self):
        self.entries = []

    def log(self, msg):
        self.entries.append(msg)
        print(msg)

    def relatorio(self):
        return "\n".join(self.entries)


def _parse_date(d):
    if isinstance(d, str):
        if "/" in d:
            parts = d.split("/")
            if len(parts[2]) == 4:
                return datetime(int(parts[2]), int(parts[1]), int(parts[0]))
            else:
                return datetime(int(parts[2]) + 2000, int(parts[1]), int(parts[0]))
        else:
            return datetime.strptime(d, "%Y-%m-%d")
    return pd.to_datetime(d)


def diagnosticar_sessions(df, log):
    log.log("=" * 60)
    log.log("DIAGNOSTICO - palavritas_sessions")
    log.log(f"Linhas originais: {len(df)}")

    dups = df.duplicated(subset="session_id").sum()
    log.log(f"session_id duplicados: {dups}")

    date_errors = 0
    for d in df["word_date"]:
        try:
            _parse_date(d)
        except (ValueError, TypeError):
            date_errors += 1
    log.log(f"Datas com formato inconsistente: {date_errors}")

    bad_attempts = df[~df["attempts"].between(1, 6)]
    log.log(f"Tentativas fora de 1-6: {len(bad_attempts)} valores={sorted(bad_attempts['attempts'].unique())}")

    bad_results = df[~df["result"].isin(["win", "lose"])]
    log.log(f"Resultados invalidos: {len(bad_results)}")

    devices_raw = df["device"].str.lower().str.strip().value_counts()
    unknown = {k: v for k, v in devices_raw.items() if k not in ("android", "ios")}
    log.log(f"Devices brutos: {devices_raw.to_dict()}")
    if unknown:
        log.log(f"Devices nao mapeados: {unknown}")

    bad_hours = df[~df["session_hour"].between(0, 23)]
    log.log(f"Horas invalidas: {len(bad_hours)}")

    q1 = df["time_to_complete_sec"].quantile(0.01)
    q99 = df["time_to_complete_sec"].quantile(0.99)
    outliers = df[(df["time_to_complete_sec"] < q1) | (df["time_to_complete_sec"] > q99)]
    log.log(f"Tempo min={df['time_to_complete_sec'].min()} max={df['time_to_complete_sec'].max()} media={df['time_to_complete_sec'].mean():.1f}")
    log.log(f"Outliers de tempo (P1={q1:.0f} P99={q99:.0f}): {len(outliers)}")

    log.log(f"played_next_day: {df['played_next_day'].value_counts().to_dict()}")
    log.log(f"active_d30: {df['active_d30'].value_counts().to_dict()}")
    log.log(f"newsletter_open: {df['newsletter_open_before_game'].value_counts().to_dict()}")
    log.log(f"streak_day: {df['streak_day'].value_counts().sort_index().to_dict()}")


def limpar_sessions(df):
    df = df.drop_duplicates(subset="session_id").copy()

    dates = []
    errors = 0
    for d in df["word_date"]:
        try:
            dates.append(_parse_date(d))
        except (ValueError, TypeError):
            errors += 1
            dates.append(None)
    df["word_date"] = dates
    df = df.dropna(subset=["word_date"])
    df["word_date"] = pd.to_datetime(df["word_date"])

    df = df[df["attempts"].between(1, 6)]
    df = df[df["result"].isin(["win", "lose"])]

    df["device"] = df["device"].str.lower().str.strip()
    df["device"] = df["device"].replace({
        "android": "Android",
        "ios": "iOS",
    })
    unknown_devices = df[~df["device"].isin(["Android", "iOS"])]
    if len(unknown_devices) > 0:
        df.loc[unknown_devices.index, "device"] = "Android"

    return df


def diagnosticar_attempts(df, log):
    log.log("")
    log.log("=" * 60)
    log.log("DIAGNOSTICO - palavritas_attempts")
    log.log(f"Linhas originais: {len(df)}")

    bad_att = df[~df["attempt_number"].between(1, 6)]
    log.log(f"attempt_number fora de 1-6: {len(bad_att)}")

    bad_cl = df[~df["correct_letters"].between(0, 5)]
    log.log(f"correct_letters fora de 0-5: {len(bad_cl)}")

    bad_cp = df[~df["correct_positions"].between(0, 5)]
    log.log(f"correct_positions fora de 0-5: {len(bad_cp)}")

    sum_bad = df[df["correct_letters"] + df["correct_positions"] > 5]
    log.log(f"letters + positions > 5: {len(sum_bad)}")

    sessions_com_attempts = df["session_id"].nunique()
    log.log(f"Sessions com attempts: {sessions_com_attempts}")


def limpar_attempts(df):
    df = df[df["attempt_number"].between(1, 6)]
    df = df[df["correct_letters"].between(0, 5)]
    df = df[df["correct_positions"].between(0, 5)]
    df = df[df["correct_letters"] + df["correct_positions"] <= 5]
    return df


def diagnosticar_profile(df, log):
    log.log("")
    log.log("=" * 60)
    log.log("DIAGNOSTICO - user_profile")
    log.log(f"Linhas originais: {len(df)}")

    dups = df.duplicated(subset="user_id").sum()
    log.log(f"user_id duplicados: {dups}")

    nulls = df.isnull().sum()
    log.log(f"Nulos por coluna:\n{nulls[nulls > 0].to_dict()}")

    log.log(f"age_range: {sorted(df['age_range'].dropna().unique())}")

    state_vals = df["state"].dropna().unique()
    long_states = [s for s in state_vals if isinstance(s, str) and len(str(s)) > 2]
    log.log(f"Estados por extenso: {long_states}")

    log.log(f"salary_range: {sorted(df['salary_range'].dropna().unique())}")

    food_vals = df["orders_food_delivery"].str.lower().str.strip().value_counts()
    log.log(f"orders_food_delivery bruto: {food_vals.to_dict()}")

    log.log(f"newsletter_subscriber: {df['newsletter_subscriber'].value_counts().to_dict()}")
    log.log(f"plays_other_word_games: {df['plays_other_word_games'].value_counts().to_dict()}")
    log.log(f"typical_play_time: {df['typical_play_time'].value_counts().to_dict()}")
    log.log(f"food_delivery_platform: {df['food_delivery_platform'].value_counts().to_dict()}")


def limpar_profile(df):
    df["age_range"] = df["age_range"].fillna("Nao informado")
    df["salary_range"] = df["salary_range"].fillna("Nao informado")
    df["state"] = df["state"].fillna("Nao informado")
    df["city"] = df["city"].fillna("Nao informado")

    food_normalized = df["orders_food_delivery"].astype(str).str.lower().str.strip()
    df["orders_food_delivery"] = food_normalized.map({
        "true": True, "sim": True, "yes": True,
        "false": False, "nao": False, "no": False, "não": False,
    }).fillna(False)

    df["plays_other_word_games"] = df["plays_other_word_games"].astype(str).str.lower().str.strip().map({
        "true": True, "sim": True, "yes": True,
        "false": False, "nao": False, "no": False, "não": False,
    }).fillna(False)

    df["newsletter_subscriber"] = df["newsletter_subscriber"].astype(str).str.lower().str.strip().map({
        "true": True, "sim": True, "yes": True,
        "false": False, "nao": False, "no": False, "não": False,
    }).fillna(False)

    df["food_delivery_freq_week"] = pd.to_numeric(df["food_delivery_freq_week"], errors="coerce").fillna(0).astype(int)

    df["food_delivery_platform"] = df["food_delivery_platform"].fillna("Nenhum")
    df["job_role"] = df["job_role"].fillna("Nao informado")
    df["sector"] = df["sector"].fillna("Nao informado")
    df["company_size"] = df["company_size"].fillna("Nao informado")
    df["typical_play_time"] = df["typical_play_time"].fillna("Nao informado")

    return df


def rodar_diagnostico():
    from src.load import load_all
    log = DiagnosticLog()
    sessions, attempts, profile = load_all()

    diagnosticar_sessions(sessions, log)
    diagnosticar_attempts(attempts, log)
    diagnosticar_profile(profile, log)

    sessions = limpar_sessions(sessions)
    attempts = limpar_attempts(attempts)
    profile = limpar_profile(profile)

    log.log("")
    log.log("=" * 60)
    log.log(f"RESUMO POS-LIMPEZA: sessions={len(sessions)} attempts={len(attempts)} profile={len(profile)}")

    return sessions, attempts, profile
