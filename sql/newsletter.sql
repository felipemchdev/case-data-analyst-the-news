SELECT 
    s.newsletter_open_before_game,
    p.newsletter_subscriber,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN s.played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN s.active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions s
INNER JOIN user_profile p ON s.user_id = p.user_id
GROUP BY s.newsletter_open_before_game, p.newsletter_subscriber
ORDER BY s.newsletter_open_before_game, p.newsletter_subscriber;

SELECT 
    session_hour,
    COUNT(*) AS sessoes,
    ROUND(AVG(CASE WHEN played_next_day = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d1,
    ROUND(AVG(CASE WHEN active_d30 = 'True' THEN 1 ELSE 0 END), 3) AS taxa_d30
FROM palavritas_sessions
GROUP BY session_hour
ORDER BY session_hour;
