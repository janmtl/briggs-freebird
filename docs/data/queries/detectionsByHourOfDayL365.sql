SELECT
  hour(time - interval '8' hour) AS hour_of_day,
  comName,
  sciName,
  COUNT(*) AS detections_cnt
FROM freebirdDB."detectionsTBL"
WHERE ((measure_name = 'Confidence') OR (measure_name = 'confidence'))
  AND time >= ago(365d)
GROUP BY 1, 2, 3