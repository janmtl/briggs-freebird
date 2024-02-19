WITH
daily_sums_l28 AS (
  SELECT
    bin(time - interval '8' hour, 1d) AS time,
    comName,
    sciName,
    COUNT(*) AS detections_cnt
  FROM freebirdDB."detectionsTBL"
  WHERE ((measure_name = 'Confidence') OR (measure_name = 'confidence'))
    AND time >= ago(14d)
  GROUP BY 1, 2, 3
),
ranked_daily_sums_l28 AS (
  SELECT
    time,
    comName,
    sciName,
    detections_cnt,
    RANK() OVER (PARTITION BY time ORDER BY detections_cnt DESC) AS sum_rank
  FROM daily_sums_l28
)
SELECT *
FROM ranked_daily_sums_l28
WHERE sum_rank <= ${TOP_K}

 