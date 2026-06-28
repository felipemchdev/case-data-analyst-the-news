SELECT 
    result,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30,
    ROUND(AVG(attempts), 2) AS media_tentativas
FROM palavritas_sessions
GROUP BY result;

SELECT 
    streak_day,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions
GROUP BY streak_day
ORDER BY streak_day;

SELECT 
    session_hour,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30,
    ROUND(AVG(CASE WHEN result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate
FROM palavritas_sessions
GROUP BY session_hour
ORDER BY session_hour;

SELECT 
    device,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30,
    ROUND(AVG(CASE WHEN result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate
FROM palavritas_sessions
GROUP BY device;

SELECT 
    newsletter_open_before_game,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions
GROUP BY newsletter_open_before_game;

-- Segmentacao de usuarios por frequencia de jogo (heavy/medium/light)
WITH user_retention AS (
    SELECT
        user_id,
        COUNT(*) AS total_sessoes,
        ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
        ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30,
        ROUND(AVG(CASE WHEN result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate,
        MAX(streak_day) AS streak_max,
        ROUND(AVG(CASE WHEN newsletter_open_before_game = 'True' THEN 1 ELSE 0 END), 3) AS newsletter_rate
    FROM palavritas_sessions
    GROUP BY user_id
)
SELECT
    CASE
        WHEN total_sessoes >= 6 THEN 'heavy'
        WHEN total_sessoes >= 2 THEN 'medium'
        ELSE 'light'
    END AS segmento,
    COUNT(*) AS usuarios,
    ROUND(AVG(taxa_d1), 3) AS d1_medio,
    ROUND(AVG(taxa_d30), 3) AS d30_medio,
    ROUND(AVG(win_rate), 3) AS win_rate_medio,
    ROUND(AVG(streak_max), 1) AS streak_max_medio
FROM user_retention
GROUP BY
    CASE
        WHEN total_sessoes >= 6 THEN 'heavy'
        WHEN total_sessoes >= 2 THEN 'medium'
        ELSE 'light'
    END
ORDER BY d30_medio DESC;
