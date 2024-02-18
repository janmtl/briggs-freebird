SELECT
  hour(time) AS hour_of_day,
  comName,
  sciName,
  COUNT(*) AS detections_cnt
FROM freebirdDB."detectionsTBL"
WHERE measure_name = 'Confidence'
  AND time >= ago(365d)
GROUP BY 1, 2, 3