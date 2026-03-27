with products as (

    select * from {{ ref('stg_products') }}

),

categories as (

    select * from {{ ref('stg_categories') }}

),

order_items as (

    select
        product_id,
        sum(quantity) as total_units_sold,
        
        sum(quantity * unit_price) as total_revenue
    
    from {{ ref('stg_order_items') }}
    
    group by product_id

),

final as (

    select
        p.product_id,
        p.product_name,
        c.category_name,
        p.price,
        p.stock_qty,
        
        coalesce(oi.total_units_sold, 0) as total_units_sold,
        coalesce(oi.total_revenue, 0) as total_revenue,
        case
            when p.stock_qty = 0    then 'Out of Stock'
            when p.stock_qty < 10   then 'Critical'
            when p.stock_qty < 50   then 'Low Stock'
            else 'In Stock'
        end as stock_status
    from products p
    
    
    left join categories c on p.category_id = c.category_id
    
    left join order_items oi on p.product_id = oi.product_id

)

select * from final