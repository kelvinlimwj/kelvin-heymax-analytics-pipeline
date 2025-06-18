{{ config(
    materialized='table'
) }}

WITH user_data AS (
    SELECT 
  e.*,
  u.country
FROM {{ ref('fct_events') }} AS e
LEFT JOIN {{ ref('dim_users') }} AS u
  ON e.user_id = u.user_id
),

user_activity_by_week AS (
  SELECT
    user_id,
    event_week
  FROM user_data
  GROUP BY user_id, event_week
),

activity_with_lag AS (
  SELECT
    user_id,
    event_week,
    LAG(event_week) OVER (PARTITION BY user_id ORDER BY event_week) AS prev_week,
    LEAD(event_week) OVER (PARTITION BY user_id ORDER BY event_week) AS next_week
  FROM user_activity_by_week
),

labeled_users AS (
  SELECT
    user_id,
    event_week,
    prev_week,
    next_week,
    CASE
      WHEN prev_week IS NULL THEN 'New'
      WHEN prev_week IS NOT NULL AND next_week IS NOT NULL THEN 'Retained'
      WHEN prev_week IS NULL AND next_week IS NOT NULL THEN 'New'
      WHEN prev_week IS NOT NULL AND next_week IS NULL THEN 'Churned'
      WHEN prev_week IS NOT NULL AND event_week NOT IN (SELECT event_week FROM user_activity_by_week WHERE user_id = ua.user_id) THEN 'Resurrected'
    END AS user_status
  FROM activity_with_lag ua
)

SELECT * FROM labeled_users