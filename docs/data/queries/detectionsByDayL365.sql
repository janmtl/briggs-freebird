WITH
recent_total_detections AS (
  SELECT
    comName,
    sciName,
    COUNT(*) AS detections_cnt
  FROM freebirdDB."detectionsTBL"
  WHERE ((measure_name = 'Confidence') OR (measure_name = 'confidence'))
    AND time >= ago(365d)
  GROUP BY 1, 2
),
top_recent_total_detections AS (
  SELECT
    comName,
    sciName,
    1 AS is_top_k
  FROM recent_total_detections
  ORDER BY detections_cnt DESC
  LIMIT ${TOP_K}
),
daily_detections AS (
  SELECT
    bin(time - interval '8' hour, 1day) AS time,
    comName,
    sciName,
    COUNT(*) AS detections_cnt
  FROM freebirdDB."detectionsTBL" AS raw_detections
  INNER JOIN top_recent_total_detections AS top_detections
  USING (comName, sciName)
  WHERE ((measure_name = 'Confidence') OR (measure_name = 'confidence'))
    AND time >= ago(365d)
  GROUP BY 1, 2, 3
)

SELECT
  time,
  comName,
  sciName,
  SUM(detections_cnt) OVER (PARTITION BY comName, sciName ORDER BY time ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS detections_cnt
FROM daily_detections