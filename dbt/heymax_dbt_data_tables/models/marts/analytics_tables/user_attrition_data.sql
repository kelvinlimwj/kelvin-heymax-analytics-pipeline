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
    country,
    event_week
  FROM user_data
  GROUP BY user_id, country, event_week
),

activity_with_lag AS (
  SELECT
    user_id,
    country,
    event_week,
    LAG(event_week) OVER (PARTITION BY user_id ORDER BY event_week) AS prev_week,
    LEAD(event_week) OVER (PARTITION BY user_id ORDER BY event_week) AS next_week
  FROM user_activity_by_week
),

labeled_users AS (
  SELECT
    user_id,
    country,
    event_week,
    prev_week,
    next_week,
    CASE
      WHEN next_week IS NULL THEN 'Churned'
      WHEN prev_week IS NULL THEN 'New'
      WHEN DATE_DIFF(PARSE_DATE('%G-W%V', event_week), PARSE_DATE('%G-W%V', prev_week), WEEK) = 1 THEN 'Retained'
      WHEN DATE_DIFF(PARSE_DATE('%G-W%V', event_week), PARSE_DATE('%G-W%V', prev_week), WEEK) > 1 THEN 'Resurrected'
    END AS user_status
  FROM activity_with_lag
)

SELECT * FROM labeled_users