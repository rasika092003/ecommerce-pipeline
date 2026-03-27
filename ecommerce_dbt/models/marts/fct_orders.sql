with orders as (

    select * from {{ ref('stg_orders') }}

),

order_items as (

    select
        order_id,
        
        count(order_item_id) as total_items,
        sum(quantity) as total_quantity,
        
        sum(quantity * unit_price) as calculated_revenue
    from {{ ref('stg_order_items') }}
    group by order_id

),

customers as (

    select
        customer_id,
        customer_name,
        city,
        
        country,
        customer_segment
    from {{ ref('dim_customers') }}

),

final as (

    select
        o.order_id,
        o.customer_id,
        c.customer_name,
        c.city,
        c.country,
        c.customer_segment,
        o.order_date,
        
        date(o.order_date) as order_day,
        
        extract(month from o.order_date)::int as order_month,
        extract(year from o.order_date)::int as order_year,
        
        o.status,
        oi.total_items,
        
        oi.total_quantity,
        round(oi.calculated_revenue::numeric, 2) as revenue,
        round(o.total_amount::numeric, 2) as total_amount
    from orders o
    left join order_items oi on o.order_id = oi.order_id
    
    left join customers c on o.customer_id = c.customer_id

)

select * from final