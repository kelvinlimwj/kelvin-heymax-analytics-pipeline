# Core Tables: 
Table transformation logic found under `models/marts/core_tables/`

## `heymax-kelvin-analytics.heymax_analytics.dim_users` – User Dimension Table
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw` 

> Description: Contains metadata about each user in the system. Only consists of user_id, country now. Should aim to include more dimensions such as name, phone_number, email, DOB, signup_date etc.

| **Column Name** | **Data Type** | **Description** |
|-----------------|---------------|------------------|
| `user_id`       | STRING        | Unique identifier for each user. Primary key of the table.|
| `country`       | STRING        | Country of the user, typically based on registration IP or profile information. |


## `heymax-kelvin-analytics.heymax_analytics.fct_events` – Events Table
> **Source Table:** `heymax-kelvin-analytics.heymax_analytics.event_stream_raw`  

> Description: Captures user-generated events, platform interactions and event miles accumulation.

| Column Name           | Data Type | Description                                                                                   |
|------------------------|-----------|-------------------------------|
| `user_id`              | STRING    | Unique identifier for the user who triggered the event|
| `event_time`           | TIMESTAMP | Exact timestamp when the event occurred|
| `event_day`            | DATE      | Calendar date of the event|
| `event_week`           | STRING    | ISO week string in the format `YYYY-Www` (e.g., `2025-W14`) for WAU analysis|
| `event_month`          | STRING    | Calendar month in the format `YYYY-MM` for MAU analysis|
| `event_type`           | STRING    | Type of event performed (e.g., `miles_earned`, `share`)|
| `platform`             | STRING    | Platform where the event occurred (e.g., `web`, `android`, `ios`)|
| `utm_source`           | STRING    | Marketing attribution source (e.g., `google`, `tiktok`, `organic`)|
| `transaction_category` | STRING    | Category of the transaction (e.g., `dining`, `ecommerce`, `others`)|
| `miles_amount`         | FLOAT     | Number of miles associated with the event|
| `event_category`       | STRING    | Classification of the event as either `'miles_activity'` or `'engagement'` |


# Analytics Tables:
Table transformation logic found under `models/marts/analytics_tables/`

## `heymax-kelvin-analytics.heymax_analytics.user_attrition_data` – User Attrition Data Table
> **Source Tables:** `heymax-kelvin-analytics.heymax_analytics.dim_users` / `heymax-kelvin-analytics.heymax_analytics.fct_events` 

Use Case: HeyMax User Activity and Attrition Dashboard https://lookerstudio.google.com/reporting/819c1ac8-762e-4fb9-ac34-94d2ef2c20ba/page/7uDOF

| Column Name   | Data Type | Description |
|---------------|-----------|-------------|
| `user_id`     | `STRING`  | Unique identifier of the user. |
| `event_week`  | `STRING`  | ISO-formatted year-week (e.g., `2025-W24`) representing the week the user was active. |
| `prev_week`   | `STRING`  | The previous week (`event_week`) in which the user was active. Calculated using `LAG()`. |
| `next_week`   | `STRING`  | The next week (`event_week`) in which the user was active. Calculated using `LEAD()`. |
| `user_status` | `STRING`  | Classification of the user’s activity status for the given week. Values:<br>• `New`: User appears for the first time this week.<br>• `Retained`: User was active last week and continues to be active this week.<br>• `Churned`: User was active last week but not in any future week.<br>• `Resurrected`: User was active in a past week, churned, and returned this week.<br>* |
