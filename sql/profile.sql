SELECT 
    p.age_range,
    COUNT(*) AS sessoes,
    COUNT(DISTINCT s.user_id) AS jogadores,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30,
    ROUND(AVG(CASE WHEN s.result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY p.age_range
ORDER BY taxa_d30 DESC;

SELECT 
    p.salary_range,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY p.salary_range
ORDER BY taxa_d30 DESC;

SELECT 
    p.sector,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY p.sector
ORDER BY sessoes DESC;

SELECT 
    p.plays_other_word_games,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY p.plays_other_word_games;

SELECT 
    p.typical_play_time,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY p.typical_play_time
ORDER BY taxa_d30 DESC;

SELECT 
    p.orders_food_delivery,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY p.orders_food_delivery;

SELECT 
    p.newsletter_subscriber,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30,
    ROUND(AVG(CASE WHEN s.result = 'win' THEN 1 ELSE 0 END), 3) AS win_rate
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY p.newsletter_subscriber;
