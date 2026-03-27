with source as (
    select * from {{ source ('ecommerce', 'products')}}
),
renamed as (
    select 
    id as product_id,
    name as product_name,
    category_id,
    price,
    stock_qty
    from source
)
select * from renamed
