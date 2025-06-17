SELECT 
  e.*,
  u.country,
  DATE(e.event_time) AS event_day,
  FORMAT_DATE('%G-W%V', DATE(e.event_time)) AS event_week,
  FORMAT_DATE('%Y-%m', DATE(e.event_time)) AS event_month,
  CASE 
    WHEN e.miles_amount IS NULL THEN 'engagement'
    ELSE 'miles_activity'
  END AS event_category
FROM {{ ref('fct_events') }} AS e
LEFT JOIN {{ ref('dim_users') }} AS u
  ON e.user_id = u.user_id
