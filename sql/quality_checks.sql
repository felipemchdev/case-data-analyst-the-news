SELECT COUNT(*) AS total_linhas FROM palavritas_sessions;

SELECT COUNT(DISTINCT session_id) AS sessions_unicas FROM palavritas_sessions;

SELECT session_id, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY session_id
HAVING COUNT(*) > 1;

SELECT word_date, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY word_date
ORDER BY word_date
LIMIT 10;

SELECT attempts, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY attempts
ORDER BY attempts;

SELECT result, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY result;

SELECT device, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY device;

SELECT session_hour, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY session_hour
ORDER BY session_hour;

SELECT 
    MIN(time_to_complete_sec) AS minimo,
    MAX(time_to_complete_sec) AS maximo,
    AVG(time_to_complete_sec) AS media
FROM palavritas_sessions;

SELECT 
    played_next_day, 
    active_d30,
    COUNT(*) AS n
FROM palavritas_sessions
GROUP BY played_next_day, active_d30;

SELECT newsletter_open_before_game, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY newsletter_open_before_game;

SELECT streak_day, COUNT(*) AS n
FROM palavritas_sessions
GROUP BY streak_day
ORDER BY streak_day;
