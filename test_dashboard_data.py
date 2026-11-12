import pandas as pd
from dashboard_data import filter_data, summarize


def test_filters_and_order_count():
    data = pd.DataFrame([
        (1, '2026-09-01', 'Completed', 'Ha Noi', 'Electronics', 2, 50),
        (1, '2026-09-01', 'Completed', 'Ha Noi', 'Clothing', 1, 20),
        (2, '2026-09-02', 'Pending', 'HCM', 'Electronics', 1, 100),
    ], columns=['order_id', 'order_date', 'status', 'city', 'category_name', 'quantity', 'revenue'])
    data['order_date'] = pd.to_datetime(data['order_date'])
    selected = filter_data(data, '2026-09-01', '2026-09-02', ['Completed'], ['Ha Noi'], ['Electronics', 'Clothing'])
    assert summarize(selected) == (70, 1, 70, 3)
    assert summarize(filter_data(data, '2026-09-01', '2026-09-01', ['Pending'], ['HCM'], ['Electronics'])) == (0, 0, 0, 0)
