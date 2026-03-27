with source as (
    select * from {{source ('ecommerce', 'customers')}}
),
renamed as (
    select
    id as customer_id,
    name as customer_name,
    email,
    city,
    country,
    signup_date
    from source
)
select * from renamed
