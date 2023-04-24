{{ config(materialized='view') }}

select * from {{ source("staging", "jena_climate") }}