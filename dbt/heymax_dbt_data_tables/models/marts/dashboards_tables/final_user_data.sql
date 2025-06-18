{{ config(
    materialized='table'
) }}

SELECT 
  e.*,
  u.country
FROM {{ ref('fct_events') }} AS e
LEFT JOIN {{ ref('dim_users') }} AS u
  ON e.user_id = u.user_id
