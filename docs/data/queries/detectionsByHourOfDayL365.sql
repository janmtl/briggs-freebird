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
)

SELECT
  hour(time - interval '8' hour) AS hour_of_day,
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