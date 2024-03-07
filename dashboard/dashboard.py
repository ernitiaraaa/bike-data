import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset
day_df = pd.read_csv("dashboard/all_data_day.csv")
day_df['date'] = pd.to_datetime(day_df['date'])

st.set_page_config(page_title="Bike-Sharing Dashboard",
                   layout="wide")

def create_seasonly_users_df(df):
    season_rent_df = df.groupby("season").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    season_rent_df = season_rent_df.reset_index()
    season_rent_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    season_rent_df.set_index('season', inplace=True)
    season_rent_df = season_rent_df.stack().reset_index()
    season_rent_df.columns = ['season', 'type_of_rides', 'count_rides']
    return season_rent_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby("weekday").agg({
        "casual": "sum",
        "registered": "sum",
        "count": "sum"
    })
    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        "count": "total_rides",
        "casual": "casual_rides",
        "registered": "registered_rides"
    }, inplace=True)
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'],
                                categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    weekday_users_df = weekday_users_df.sort_values('weekday')
    return weekday_users_df

# Make filter components
min_date = day_df["date"].min()
max_date = day_df["date"].max()

# Sidebar
with st.sidebar:
    st.image("dashboard/logo.png")
    st.sidebar.header("Filter:")
    start_date, end_date = st.date_input(
        label="Date Filter", min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = day_df[(day_df["date"] >= str(start_date)) & (day_df["date"] <= str(end_date))]

seasonly_users_df = create_seasonly_users_df(main_df)
weekday_rent_df = create_weekday_users_df(main_df)

st.header('Bike Data Sharing :sparkles:')

total_all_rides = main_df['count'].sum()
st.metric("Total Rides", value=total_all_rides)

st.subheader ('Season count Bike Share Riders ')

# Plot Season Count of Bikeshare Rides
plt.figure(figsize=(10, 6))
sns.lineplot(data=seasonly_users_df, x='season', y='count_rides', hue='type_of_rides',
            palette={"casual_rides": "skyblue", "registered_rides": "orange", "total_rides": "red"}, markers='o')
plt.title('Count of bikeshare rides by season')
plt.xlabel('Season')
plt.ylabel('Total Rides')
plt.legend(title='Type of Rides')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

st.subheader('Count of Bikeshare Rides by Weekday')

day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Plot Count of Bikeshare Rides by Weekday
plt.figure(figsize=(10, 6))

bar_width = 0.35
index = range(len(weekday_rent_df.index))
casual_bars = plt.bar(index, weekday_rent_df['casual_rides'], bar_width, color='skyblue', label='Casual')
registered_bars = plt.bar([i + bar_width for i in index], weekday_rent_df['registered_rides'], bar_width, color='orange', label='Registered')
plt.xlabel("Weekday")
plt.ylabel("Total Rides")
plt.title("Count of bikeshare rides by Weekday")
plt.xticks([i + bar_width/2 for i in index], day)
plt.legend()
st.pyplot(plt)
