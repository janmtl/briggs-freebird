WITH
constructor0 AS (
  SELECT
    comName,
    sciName,
    MIN(time) AS first_time_detected,
    COUNT(*) AS n_detections
  FROM freebirdDB."detectionsTBL"
  WHERE ((measure_name = 'Confidence') OR (measure_name = 'confidence'))
  GROUP BY 1, 2
)
SELECT
  first_time_detected,
  comName,
  sciName
FROM constructor0
WHERE n_detections >= 5
ORDER BY first_time_detected DESC
LIMIT 100