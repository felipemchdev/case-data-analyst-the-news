SELECT 
    word,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate,
    ROUND(AVG(attempts), 2) AS media_tentativas,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions
GROUP BY word
HAVING sessoes >= 20
ORDER BY win_rate ASC
LIMIT 15;

SELECT 
    word,
    word_date,
    COUNT(*) AS jogadores,
    ROUND(AVG(CASE WHEN result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1
FROM palavritas_sessions
GROUP BY word, word_date
ORDER BY win_rate ASC
LIMIT 10;

WITH word_impact AS (
    SELECT
        word,
        COUNT(*) AS sessoes,
        ROUND(AVG(CASE WHEN result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate,
        ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1
    FROM palavritas_sessions
    GROUP BY word
    HAVING sessoes >= 30
)
SELECT
    CASE 
        WHEN win_rate < 0.70 THEN 'dificil'
        WHEN win_rate < 0.85 THEN 'media'
        ELSE 'facil'
    END AS dificuldade,
    COUNT(*) AS palavras,
    ROUND(AVG(sessoes), 0) AS sessoes_medias,
    ROUND(AVG(taxa_d1), 3) AS d1_media
FROM word_impact
GROUP BY
    CASE 
        WHEN win_rate < 0.70 THEN 'dificil'
        WHEN win_rate < 0.85 THEN 'media'
        ELSE 'facil'
    END
ORDER BY d1_media;
