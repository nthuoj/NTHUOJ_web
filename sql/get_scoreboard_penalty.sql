CREATE DEFINER=`%s`@`%%%%` PROCEDURE `get_scoreboard_penalty`(scoreboard_id INT,freeze BOOL)
BEGIN
    DROP TEMPORARY TABLE IF EXISTS board;
    DROP TEMPORARY TABLE IF EXISTS contest_user;
    DROP TEMPORARY TABLE IF EXISTS contest_range;
    DROP TEMPORARY TABLE IF EXISTS first_ac;
    DROP TEMPORARY TABLE IF EXISTS contest_range_with_first_ac;
    DROP TEMPORARY TABLE IF EXISTS have_ac_penalty;
    
    CREATE TEMPORARY TABLE contest_user(
        SELECT user_id
        FROM contest_contestant
        WHERE contest_id=scoreboard_id
    );
    CREATE TEMPORARY TABLE board(
        SELECT user_id,problem_id,testcase
        FROM contest_user u
        JOIN (
            SELECT pt.problem_id,COUNT(*) testcase
            FROM contest_contest_problem ccp 
            JOIN problem_testcase pt
            ON ccp.problem_id=pt.problem_id
            WHERE contest_id=scoreboard_id
            GROUP BY pt.problem_id
        ) p
    );
    SELECT start_time, end_time, freeze_time
    INTO @start_time, @end_time,@freeze_time
    FROM contest_contest
    WHERE id=scoreboard_id;
    
    SELECT IF(freeze, @end_time-INTERVAL @freeze_time MINUTE, @end_time)
    INTO @end_time;

    CREATE TEMPORARY TABLE contest_range(
        SELECT id,problem_id,ps.user_id,ps.status,ps.submit_time
        FROM problem_submission ps
        JOIN contest_user cu
        ON ps.user_id=cu.user_id
        WHERE (submit_time BETWEEN @start_time AND @end_time)
    );
    CREATE TEMPORARY TABLE first_ac(
        SELECT user_id,problem_id,MIN(submit_time) AS ac_time
        FROM contest_range
        WHERE status='AC'
        GROUP BY user_id,problem_id
    );
    CREATE TEMPORARY TABLE contest_range_with_first_ac(
        SELECT cr.user_id,cr.problem_id,cr.status,cr.submit_time,fa.ac_time
        FROM contest_range cr
        LEFT JOIN first_ac fa
        ON cr.user_id=fa.user_id
        AND cr.problem_id=fa.problem_id
    );
    CREATE TEMPORARY TABLE have_ac_penalty(
        SELECT user_id,problem_id,count(*) times,ac_time
        FROM contest_range_with_first_ac
        WHERE submit_time<=ac_time
        AND (not status='JUDGING' AND not status='WAIT' AND not status='JE')
        OR ac_time IS NULL
        GROUP BY user_id,problem_id
    );
    
    SELECT b.user_id,b.problem_id,
    CASE
        WHEN lj.AC is null THEN 0
        ELSE lj.AC
    END total_AC,
    b.testcase,
    CASE
        WHEN ha.times is null THEN '--'
        ELSE ha.times
    END times,
    CASE
        WHEN ha.ac_time is null THEN '--'
        ELSE FLOOR((UNIX_TIMESTAMP(ha.ac_time)-UNIX_TIMESTAMP(@start_time))/60 + 20*(ha.times-1))
    END penalty,
    CASE
        WHEN ha.ac_time is null THEN '--'
        ELSE FLOOR((UNIX_TIMESTAMP(ha.ac_time)-UNIX_TIMESTAMP(@start_time))/60)
    END first_ac_time
    FROM board b
    LEFT JOIN have_ac_penalty ha ON b.user_id=ha.user_id AND b.problem_id=ha.problem_id
    LEFT JOIN (
        SELECT user_id,problem_id,MAX(AC) AC
        FROM (
            SELECT user_id,problem_id,count(verdict) AC
            FROM problem_submissiondetail ps
            JOIN (
                SELECT cr.user_id,problem_id,id
                FROM contest_range cr
                JOIN contest_user cu
                ON cr.user_id=cu.user_id
            ) gg ON ps.sid_id=gg.id
            WHERE verdict='AC'
            GROUP BY sid_id
        ) ca
        GROUP BY user_id,problem_id
    ) lj
    ON b.user_id=lj.user_id
    AND b.problem_id=lj.problem_id;
    
    DROP TEMPORARY TABLE IF EXISTS board;
    DROP TEMPORARY TABLE IF EXISTS contest_user;
    DROP TEMPORARY TABLE IF EXISTS contest_range;
    DROP TEMPORARY TABLE IF EXISTS first_ac;
    DROP TEMPORARY TABLE IF EXISTS contest_range_with_first_ac;
    DROP TEMPORARY TABLE IF EXISTS have_ac_penalty;
END
