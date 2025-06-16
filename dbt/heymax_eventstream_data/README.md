# Tables:

Table transformation logic found under `models/marts/`

## `heymax-kelvin-analytics.heymax_analytics.dim_users` – User Dimension Table
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw`

Contains metadata about each user in the system.

| **Column Name** | **Data Type** | **Description** |
|-----------------|---------------|------------------|
| `user_id`       | STRING        | Unique identifier for each user. Primary key of the table. |
| `country`       | STRING        | Country of the user, typically based on registration IP or profile information. |


## `heymax-kelvin-analytics.heymax_analytics.fct_events` – Events Table
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw`  

Captures user-generated events such as transactions and platform interactions.

| **Column Name**        | **Data Type** | **Description** |
|------------------------|---------------|------------------|
| `user_id`              | STRING        | Foreign key linking to `dim_users.user_id`. Identifies the user performing the event. |
| `utm_source`           | STRING        | UTM source from marketing attribution (e.g., "facebook", "google", "email"). |
| `transaction_category` | STRING        | Category of the transaction or event (e.g., "purchase", "redemption"). |
| `platform`             | STRING        | Platform on which the event occurred (e.g., "iOS", "Android", "Web"). |
| `event_type`           | STRING        | Type of event (e.g., "signup", "purchase", "login"). |
| `event_time`           | TIMESTAMP     | Timestamp indicating when the event occurred. |
| `miles_amount`         | FLOAT         | Amount of miles (or reward points) earned or spent during the event. |

