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
    IF(is_top_k = 1, raw_detections.comName, 'Other') AS comName,
    IF(is_top_k = 1, raw_detections.sciName, 'Other') AS sciName,
    COUNT(*) AS detections_cnt
  FROM freebirdDB."detectionsTBL" AS raw_detections
  LEFT JOIN top_recent_total_detections AS top_detections
    ON raw_detections.comName = top_detections.comName
   AND raw_detections.sciName = top_detections.sciName
  WHERE ((measure_name = 'Confidence') OR (measure_name = 'confidence'))
    AND time >= ago(365d)
  GROUP BY 1, 2, 3
)

SELECT
  time,
  comName,
  sciName,
  -- CAST(AVG(detections_cnt) OVER (PARTITION BY comName, sciName ORDER BY time ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS INT) AS detections_cnt
  detections_cnt
FROM daily_detections