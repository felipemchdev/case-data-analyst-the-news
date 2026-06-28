from src.load import load_sessions, load_attempts, load_user_profile, load_all, save_cleaned
from src.cleaning import limpar_sessions, limpar_attempts, limpar_profile, rodar_diagnostico, DiagnosticLog
from src.analysis import (
    retencao_por_resultado, retencao_por_streak, retencao_por_hora,
    retencao_por_device, retencao_por_newsletter, dificuldade_por_palavra,
    juntar_sessions_profile, retencao_por_perfil, padrao_tentativas,
    matriz_correlacao, tabela_features, analise_coorte, curva_retencao,
    retencao_por_usuario, segmentar_usuarios, funil_newsletter_jogo,
    metrica_stickiness, exportar_dataset_looker
)
from src.statistics import (
    teste_chi2, teste_t, teste_z_proporcoes, ranking_correlacao,
    teste_anova, ic_proporcao, correcao_bonferroni, tamanho_efeito_cohen
)
from src.plots import (
    grafico_retencao_resultado, grafico_retencao_streak, grafico_retencao_hora,
    grafico_palavras, grafico_heatmap, grafico_perfil, grafico_ranking,
    grafico_curva_retencao, grafico_coorte
)
