with customers as (

    select * from {{ ref('stg_customers') }}

),

ord as (

    select
        customer_id,
        count(order_id) as total_orders,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        sum(total_amount) as lifetime_value
    from {{ ref('stg_orders') }}
    where status = 'completed'
    group by customer_id

),

final as (

    select
        customers.customer_id,
        customers.customer_name,
        customers.email,
        customers.city,
        customers.country,
        customers.signup_date,
        coalesce(ord.total_orders, 0) as total_orders,
        coalesce(ord.lifetime_value, 0) as lifetime_value,
        ord.first_order_date,
        ord.last_order_date,
        case
            when coalesce(ord.lifetime_value, 0) >= 10000 then 'VIP'
            when coalesce(ord.lifetime_value, 0) >= 5000  then 'High Value'
            when coalesce(ord.lifetime_value, 0) >= 1000  then 'Mid Value'
            else 'Low Value'
        end as customer_segment
    from customers
    left join ord on customers.customer_id = ord.customer_id

)

select * from final
