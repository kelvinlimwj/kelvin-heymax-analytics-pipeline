WITH ranked_users AS (
  SELECT
    user_id,
    country,
    ROW_NUMBER() OVER (
      PARTITION BY user_id
      ORDER BY event_time DESC
    ) AS rn
  FROM {{ ref('stg_event_stream') }}
)

SELECT
  user_id,
  country
FROM ranked_users
WHERE rn = 1