import pandas as pd
import streamlit as st
import mysql.connector

from dashboard_data import filter_data, summarize

st.set_page_config(page_title='Phân tích doanh số E-Commerce', page_icon='📊', layout='wide')
st.title('📊 Phân tích doanh số E-Commerce')
st.caption('Theo dõi doanh thu và hành vi mua hàng theo dữ liệu EcommerceDB')

with st.sidebar:
    st.header('Kết nối MySQL')
    host = st.text_input('Máy chủ', value='localhost')
    port = st.number_input('Cổng', min_value=1, max_value=65535, value=3306)
    user = st.text_input('Tên người dùng', value='root')
    password = st.text_input('Mật khẩu', type='password')
    database = st.text_input('Cơ sở dữ liệu', value='EcommerceDB')
    connect = st.button('Kết nối / Làm mới', type='primary')

if connect:
    try:
        connection = mysql.connector.connect(host=host, port=int(port), user=user, password=password, database=database, connection_timeout=5)
        try:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute('''SELECT o.order_id, o.order_date, o.status, c.customer_name, c.city,
                    p.product_id, p.product_name, cat.category_name, od.quantity, od.unit_price
                    FROM Orders o
                    JOIN Customers c ON c.customer_id = o.customer_id
                    JOIN OrderDetails od ON od.order_id = o.order_id
                    JOIN Products p ON p.product_id = od.product_id
                    LEFT JOIN Categories cat ON cat.category_id = p.category_id''')
                rows = cursor.fetchall()
                columns = cursor.column_names
            finally:
                cursor.close()
        finally:
            connection.close()
        data = pd.DataFrame(rows, columns=columns)
        data['order_date'] = pd.to_datetime(data['order_date'])
        data['category_name'] = data['category_name'].fillna('Chưa phân loại')
        data['unit_price'] = pd.to_numeric(data['unit_price'])
        data['revenue'] = data['quantity'] * data['unit_price']
        st.session_state['sales_data'] = data
    except (mysql.connector.Error, ValueError) as exc:
        st.session_state.pop('sales_data', None)
        st.error(f'Không thể tải dữ liệu MySQL: {exc}')

if 'sales_data' not in st.session_state:
    st.info('Nhập thông tin MySQL ở thanh bên và chọn Kết nối / Làm mới.')
    st.stop()

data = st.session_state['sales_data']
if data.empty:
    st.info('Cơ sở dữ liệu chưa có chi tiết đơn hàng để hiển thị.')
    st.stop()

with st.sidebar:
    st.header('Bộ lọc')
    minimum, maximum = data['order_date'].min().date(), data['order_date'].max().date()
    dates = st.date_input('Khoảng ngày đặt hàng', value=(minimum, maximum), min_value=minimum, max_value=maximum)
    statuses = st.multiselect('Trạng thái đơn', ['Completed', 'Pending', 'Cancelled'], default=['Completed'])
    city_options = sorted(data['city'].dropna().unique().tolist())
    cities = st.multiselect('Thành phố', city_options, default=city_options)
    category_options = sorted(data['category_name'].unique().tolist())
    categories = st.multiselect('Danh mục', category_options, default=category_options)

if len(dates) != 2:
    st.info('Vui lòng chọn cả ngày bắt đầu và ngày kết thúc.')
    st.stop()

filtered = filter_data(data, dates[0], dates[1], statuses, cities, categories)
revenue, orders, aov, quantity = summarize(filtered)
st.caption('Các chỉ số tính trên những dòng sản phẩm khớp bộ lọc; AOV = doanh thu / số đơn hàng khác nhau. Đơn vị tiền theo dữ liệu nguồn.')
for column, label, value in zip(st.columns(4), ['Tổng doanh thu', 'Số đơn hàng', 'Giá trị trung bình / đơn', 'Sản phẩm bán ra'], [f'{revenue:,.2f}', f'{orders:,}', f'{aov:,.2f}', f'{quantity:,.0f}']):
    column.metric(label, value)

if filtered.empty:
    st.info('Không có dữ liệu phù hợp với bộ lọc.')
else:
    left, right = st.columns(2)
    with left:
        st.subheader('Doanh thu theo ngày')
        daily = filtered.groupby('order_date')['revenue'].sum().reindex(pd.date_range(dates[0], dates[1]), fill_value=0)
        st.line_chart(daily)
    with right:
        st.subheader('Top 5 sản phẩm theo số lượng')
        top = filtered.groupby(['product_id', 'product_name'], as_index=False)['quantity'].sum().sort_values(['quantity', 'product_name'], ascending=[False, True]).head(5)
        top['product'] = top['product_name'] + ' (#' + top['product_id'].astype(str) + ')'
        st.bar_chart(top.set_index('product')['quantity'])

st.subheader('Chi tiết đơn hàng')
st.dataframe(filtered, hide_index=True)
st.download_button('Tải CSV', filtered.to_csv(index=False).encode('utf-8-sig'), 'chi_tiet_don_hang.csv', 'text/csv')

