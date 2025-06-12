SELECT
  user_id,
  event_time,
  event_type,
  platform,
  utm_source,
  transaction_category,
  miles_amount
FROM {{ ref('stg_event_stream') }}