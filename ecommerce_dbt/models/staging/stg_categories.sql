with source as (

    select * from {{ source('ecommerce', 'categories') }}

),

renamed as (

    select
        id as category_id,
        name as category_name
    from source

)

select * from renamed