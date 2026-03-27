with date_spine as (

    select generate_series(
        '2022-01-01'::date,
        '2026-12-31'::date,
        
        '1 day'::interval
    )::date as date_day

),

final as (

    select
        date_day,
        extract(year from date_day)::int as year,
        
        extract(month from date_day)::int as month,
        extract(day from date_day)::int as day,
        
        extract(quarter from date_day)::int as quarter,
        
        extract(dow from date_day)::int as day_of_week,
        
        to_char(date_day, 'Day') as day_name,
        to_char(date_day, 'Month') as month_name,
        
        to_char(date_day, 'Mon YYYY') as month_year,
        case
            when extract(dow from date_day) in (0, 6)
            then true else false
        end as is_weekend
    from date_spine

)

select * from final