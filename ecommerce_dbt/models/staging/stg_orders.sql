with source as (
    select * from {{source ('ecommerce', 'orders')}}
),
renamed as (
    select 
    id as order_id,
    customer_id,
    order_date,
    status,
    total_amount
    from source
)
select * from renamed