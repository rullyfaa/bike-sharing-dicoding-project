import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


day_data = pd.read_csv(
    "/Users/pro2015/belajar/dicoding project /Dashboard/day_df.csv")
hour_data = pd.read_csv(
    "/Users/pro2015/belajar/dicoding project /Dashboard/hour_df.csv")

# day_data = pd.read_csv('/Users/pro2015/dicoding project/Dashboard/day_df.csv')
# hour_data = pd.read_csv('/Users/pro2015/dicoding project/Dashboard/hour_df.csv')


def create_mean_user_holiday(day_data):
    mean_user_holiday = day_data.groupby(by='holiday').agg({
        'instant': 'nunique',
        'casual': 'mean',
        'registered': 'mean',
        'cnt': 'mean'
    })

    return mean_user_holiday


def create_user_per_time(hour_data):
    user_per_time = hour_data.groupby(by='time_category').agg({
        'casual': 'mean',
        'registered': 'mean'
    })

    return user_per_time


hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
min_date = hour_data['dteday'].min()
max_date = hour_data['dteday'].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_hour_df = hour_data[(hour_data['dteday'] >= str(start_date)) &
                         (hour_data['dteday'] <= str(end_date))]

main_day_df = day_data[(day_data['dteday'] >= str(start_date)) &
                       (day_data['dteday'] <= str(end_date))]

mean_user_holiday = create_mean_user_holiday(main_day_df)
user_per_time = create_user_per_time(main_hour_df)

st.header('Bike Sharing')

st.subheader('Perbandingan User Pada Hari Libur dan Non Libur')

col1, col2 = st.columns(2)

with col1:
    hari_libur = mean_user_holiday.index
    jumlah_hari_libur = mean_user_holiday['instant']

fig, ax = plt.subplots()
ax.bar(hari_libur, jumlah_hari_libur)
for i, v in enumerate(jumlah_hari_libur):
    ax.text(i, v, str(v), ha='center', va='bottom')

ax.set_xticks(range(len(hari_libur)))
ax.set_xticklabels(['Non-Holiday', 'Holiday'])

ax.set_xlabel('Kategori Hari Libur')
ax.set_ylabel('Jumlah Hari Libur')
ax.set_title('Jumlah Hari Libur vs Bukan Hari Libur')
st.pyplot(fig)

with col2:
    casual = mean_user_holiday['casual']
    registered = mean_user_holiday['registered']
    hari_libur = mean_user_holiday.index

fig, ax = plt.subplots()
ax.bar(hari_libur, casual, label='Casual Users')
ax.bar(hari_libur, registered, bottom=casual, label='Registered Users')


ax.set_xticks(hari_libur)
ax.set_xticklabels(['Non-Holiday', 'Holiday'])

ax.set_xlabel('hari_libur')
ax.set_ylabel('Number of Users')
ax.legend()
ax.set_title('Casual and Registered Holiday vs not Holiday')

st.pyplot(fig)


st.subheader('rata rata peminjam sepeda pada waktu tertentu')
casual = user_per_time['casual']
registered = user_per_time['registered']
time_category = user_per_time.index
fig, ax = plt.subplots()


ax.bar(time_category, casual, label='Casual Users')
ax.bar(time_category, registered, bottom=casual, label='Registered Users')

ax.set_xlabel('time_category')
ax.set_ylabel('Number of Users')
ax.legend()
ax.set_title('Casual and Registered Users per Time Category')
st.pyplot(fig)


# Function to calculate RFM metrics
def calculate_rfm_metrics(hour_data):
    rfm_data = hour_data.groupby('instant').agg({
        'dteday': 'max',
        'cnt': 'sum',  # Assuming 'cnt' represents monetary value
        'instant': 'nunique'  # Assuming 'instant' is a unique identifier for each transaction
    }).rename(columns={'instant': 'frequency', 'cnt': 'monetary'})

    # Calculate recency
    max_date = rfm_data['dteday'].max()
    rfm_data['recency'] = (max_date - rfm_data['dteday']).dt.days

    return rfm_data[['recency', 'frequency', 'monetary']]


# Calculate RFM metrics
rfm_data = calculate_rfm_metrics(hour_data)

# Display RFM data
st.subheader('RFM Analysis')
st.write(rfm_data.head())

# Visualize RFM metrics
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Recency
sns.histplot(rfm_data['recency'], bins=20, kde=True, ax=axes[0])
axes[0].set_title('Recency')

# Frequency
sns.histplot(rfm_data['frequency'], bins=20, kde=True, ax=axes[1])
axes[1].set_title('Frequency')

# Monetary
sns.histplot(rfm_data['monetary'], bins=20, kde=True, ax=axes[2])
axes[2].set_title('Monetary')

# Show plots
st.pyplot(fig)
