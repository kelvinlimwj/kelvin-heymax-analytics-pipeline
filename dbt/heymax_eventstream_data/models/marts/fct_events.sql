SELECT
  user_id,
  event_time,
  DATE(event_time) AS event_day,
  FORMAT_DATE('%G-W%V', DATE(event_time)) AS event_week,
  FORMAT_DATE('%Y-%m', DATE(event_time)) AS event_month,
  event_type,
  platform,
  utm_source,
  transaction_category,
  miles_amount,
  CASE 
    WHEN miles_amount IS NULL THEN 'engagement'
    ELSE 'miles_activity'
  END AS event_category
FROM {{ ref('stg_event_stream') }}
