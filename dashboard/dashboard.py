import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

# Theme setup for plotting based on user choice or default (optional, to make it premium)
sns.set_theme(style="whitegrid")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

df = load_data()

# Header
st.title("🛒 E-Commerce Data Dashboard")
st.markdown("This dashboard provides an interactive analysis of the E-Commerce Public Dataset, uncovering insights into product performance, monthly order trends, customer geography, and segmentation.")

# Sidebar - Filter
st.sidebar.header("Filter Configuration")
year_list = df['order_purchase_timestamp'].dt.year.unique().tolist()
year_list.sort()
selected_years = st.sidebar.multiselect("Select Year(s):", options=year_list, default=[2018])

if not selected_years:
    st.error("Please select at least one year.")
    st.stop()
    
# Filtered dataframe
filtered_df = df[df['order_purchase_timestamp'].dt.year.isin(selected_years)]

# Main KPIs
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Orders", f"{filtered_df['order_id'].nunique():,}")
with col2:
    st.metric("Total Revenue", f"${filtered_df['price'].sum():,.2f}")
with col3:
    st.metric("Total Customers", f"{filtered_df['customer_unique_id'].nunique():,}")
with col4:
    st.metric("Average Transaction", f"${(filtered_df['price'].sum() / filtered_df['order_id'].nunique() if filtered_df['order_id'].nunique() > 0 else 0):,.2f}")

st.divider()

# Question 1: Best and Worst Performing Categories
st.subheader("Berdasarkan Pertanyaan 1: Produk Kategori Apa yang Paling Banyak dan Sedikit Terjual?")
category_sales = filtered_df.groupby('product_category_name')['order_id'].count().reset_index()
category_sales = category_sales.sort_values(by='order_id', ascending=False)

fig1, ax1 = plt.subplots(1, 2, figsize=(18, 6))
# Best
sns.barplot(
    x="order_id", y="product_category_name", data=category_sales.head(5), 
    palette=["#72BCD4"] + ["#D3D3D3"] * 4, ax=ax1[0]
)
ax1[0].set_title("Top 5 Best Performing Product Categories")
ax1[0].set_ylabel(None)
ax1[0].set_xlabel("Number of Orders")

# Worst
sns.barplot(
    x="order_id", y="product_category_name", data=category_sales.tail(5).sort_values('order_id', ascending=True), 
    palette=["#D3D3D3"] * 4 + ["#72BCD4"], ax=ax1[1]
)
ax1[1].set_title("Top 5 Worst Performing Product Categories")
ax1[1].set_ylabel(None)
ax1[1].set_xlabel("Number of Orders")
ax1[1].invert_xaxis()
ax1[1].yaxis.tick_right()

st.pyplot(fig1)

st.divider()

# Question 2: Monthly Orders Trend
st.subheader("Berdasarkan Pertanyaan 2: Performa Penjualan Per Bulan")
monthly_orders = filtered_df.groupby(filtered_df['order_purchase_timestamp'].dt.to_period('M'))['order_id'].count().reset_index()
monthly_orders['order_purchase_timestamp'] = monthly_orders['order_purchase_timestamp'].dt.to_timestamp()

fig2, ax2 = plt.subplots(figsize=(12, 5))
plt.plot(monthly_orders['order_purchase_timestamp'], monthly_orders['order_id'], marker='o', linewidth=2, color="#72BCD4")
plt.title("Number of Orders over Time", fontsize=16)
plt.xlabel("Month-Year")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
st.pyplot(fig2)

st.divider()

# Analisis Lanjutan
st.subheader("🚀 Analisis Lanjutan")

tab_rfm, tab_geo = st.tabs(["RFM Analysis", "Geospatial Analysis"])

with tab_rfm:
    st.markdown("### Segmentasi Pelanggan via RFM")
    st.markdown("**(Recency, Frequency, Monetary)** mengukur kapan pelanggan terakhir kali berbelanja, seberapa sering, dan seberapa banyak transaksinya.")
    recent_date = filtered_df['order_purchase_timestamp'].max()
    rfm_df = filtered_df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (recent_date - x.max()).days,
        'order_id': 'nunique',
        'price': 'sum'
    }).reset_index()
    rfm_df.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']
    
    st.dataframe(rfm_df.head(10))
    
    col_a, col_b, col_c = st.columns(3)
    
    fig_r, ax_r = plt.subplots()
    sns.histplot(rfm_df['Recency'], bins=30, kde=True, ax=ax_r, color="#72BCD4")
    ax_r.set_title("Recency Distribution")
    col_a.pyplot(fig_r)

    fig_f, ax_f = plt.subplots()
    sns.histplot(rfm_df[rfm_df['Frequency'] < 10]['Frequency'], bins=10, kde=False, ax=ax_f, color="#90EE90")
    ax_f.set_title("Frequency Distribution")
    col_b.pyplot(fig_f)

    fig_m, ax_m = plt.subplots()
    sns.histplot(rfm_df[rfm_df['Monetary'] < 1000]['Monetary'], bins=30, kde=True, ax=ax_m, color="#FFB6C1")
    ax_m.set_title("Monetary Distribution")
    col_c.pyplot(fig_m)


with tab_geo:
    st.markdown("### Sebaran Pelanggan (Geospatial Analysis by State)")
    state_counts = filtered_df['customer_state'].value_counts().reset_index()
    state_counts.columns = ['State', 'Customer Count']
    
    fig_geo, ax_geo = plt.subplots(figsize=(10, 5))
    sns.barplot(x='State', y='Customer Count', data=state_counts, palette="viridis", ax=ax_geo)
    ax_geo.set_title("Customer Demographics - By Top States")
    st.pyplot(fig_geo)

st.caption("Dicoding Data Analytics Final Project Submission")
