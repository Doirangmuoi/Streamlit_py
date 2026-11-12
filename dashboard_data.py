import pandas as pd


def filter_data(data, start, end, statuses, cities, categories):
    return data[
        data['order_date'].between(pd.Timestamp(start), pd.Timestamp(end))
        & data['status'].isin(statuses)
        & data['city'].isin(cities)
        & data['category_name'].isin(categories)
    ]


def summarize(data):
    revenue = data['revenue'].sum()
    orders = data['order_id'].nunique()
    return revenue, orders, revenue / orders if orders else 0, data['quantity'].sum()
