import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Load the datasets
ireland_data = pd.read_csv("export and import countries.csv")
world_data = pd.read_csv("ireland import and export value.csv")

# Set page title and layout
st.set_page_config(page_title="Import/Export Dashboard", layout="wide")

# Sidebar for selection
st.sidebar.header('Select Filters')

# Checkbox for selecting years
selected_years_ireland = st.sidebar.multiselect('Select years (Ireland)', ireland_data['Year'].unique())
selected_years_world = st.sidebar.multiselect('Select years (World)', world_data['Year'].unique())
selected_domain_ireland = st.sidebar.multiselect('Select domain (Ireland)', ireland_data['Domain'].unique())
selected_domain_world = st.sidebar.multiselect('Select domain (World)', world_data['Domain'].unique())
selected_area_ireland = st.sidebar.multiselect('Select area (world)', ireland_data['Area'].unique())
selected_area_world = st.sidebar.multiselect('Select area (ireland)', world_data['Area'].unique())

# Filter Ireland data based on selected filters
filtered_data_ireland = ireland_data[(ireland_data['Year'].isin(selected_years_ireland)) &
                                     (ireland_data['Domain'].isin(selected_domain_ireland)) &
                                     (ireland_data['Area'].isin(selected_area_ireland))]
filtered_data_world = world_data[(world_data['Year'].isin(selected_years_world)) &
                                 (world_data['Domain'].isin(selected_domain_world)) &
                                 (world_data['Area'].isin(selected_area_world))]

# Print lengths of filtered dataframes for debugging
print("Filtered Ireland Data Length:", len(filtered_data_ireland))
print("Filtered World Data Length:", len(filtered_data_world))

# Title for the app
st.title('Import/Export Dashboard')

# Layout for the first row
col1, col2 = st.columns(2)

# Ireland Dataset
with col1:
    st.header('Ireland Dataset')
    st.write(filtered_data_ireland.head(10))

# Worldwide Dataset
with col2:
    st.header('Worldwide Dataset')
    st.write(filtered_data_world.head(10))

# Descriptive Statistics
st.header('Descriptive Statistics')
st.write("Ireland Dataset:", filtered_data_ireland.describe())
st.write("Worldwide Dataset:", filtered_data_world.describe())

# Layout for the second row
col3, col4 = st.columns(2)

# Plot total import and export values over the selected filters for Ireland
with col3:
    st.header('Total Import/Export Values: Ireland')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Year', y='Value', data=filtered_data_ireland, palette='muted', ax=ax)
    ax.set_title('Total Import/Export Values: Ireland')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Value')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Plot total import and export values over the selected filters for World
with col4:
    st.header('Total Import/Export Values: World')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Year', y='Value', data=filtered_data_world, palette='muted', ax=ax)
    ax.set_title('Total Import/Export Values: World')
    ax.set_xlabel('Year')
    ax.set_ylabel('Total Value')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Layout for the fourth row
col6, col7 = st.columns(2)

# Line plot for Import Value Trend: Ireland
with col6:
    st.header('Import Value Trend: Ireland')
    fig_ireland = plt.figure(figsize=(10, 6))
    sns.lineplot(x='Year', y='Value', data=filtered_data_ireland, label='Ireland Import', marker='o', color='orange')
    plt.title('Import Value Trend: Ireland')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend()
    st.pyplot(fig_ireland)

# Line plot for Import Value Trend: Worldwide
with col7:
    st.header('Import Value Trend: Worldwide')
    fig_world = plt.figure(figsize=(10, 6))
    sns.lineplot(x='Year', y='Value', data=filtered_data_world, label='World Import', marker='o', color='green')
    plt.title('Import Value Trend: Worldwide')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend()
    st.pyplot(fig_world)

# Extract unique domains from the datasets
unique_domains_ireland = ireland_data['Domain'].unique()
unique_domains_world = world_data['Domain'].unique()

# Dropdown for selecting domain
selected_domain_pie = st.sidebar.selectbox('Select Domain for Pie Chart', unique_domains_ireland)

# Filter data based on selected domain for pie chart
filtered_data_pie = filtered_data_ireland if selected_domain_pie in selected_domain_ireland else filtered_data_world

# Group by area and sum the values for pie chart
area_values_pie = filtered_data_pie.groupby('Area')['Value'].sum().reset_index()

# Pie chart for selected domain
st.header(f'Import/Export Distribution by Area for {selected_domain_pie}')
fig_pie, ax_pie = plt.subplots()
ax_pie.pie(area_values_pie['Value'], labels=area_values_pie['Area'], autopct='%1.1f%%', startangle=140)
ax_pie.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax_pie.set_title(f'Import/Export Distribution by Area for {selected_domain_pie}')
st.pyplot(fig_pie)

# Filter for relevant columns and rows (Import and Export Values)
filtered_data_world = world_data[world_data['Element'].isin(['Import Value', 'Export Value'])]

# Group by area and sum the values for choropleth map
area_values_world = filtered_data_world.groupby('Area')['Value'].sum().reset_index()

# Normalize the Total Value if needed (optional)
area_values_world['Value'] = area_values_world['Value'] / 1000  # Example normalization

# Choropleth Map
st.header('Choropleth Map')

fig_choropleth = go.Figure(go.Choropleth(
    locations=area_values_world['Area'],
    locationmode='country names',
    z=area_values_world['Value'],
    colorscale='Plasma',
    marker_line_color='black',
    marker_line_width=0.5,
    colorbar_title='Total Value<br>(1000 USD)'
))

fig_choropleth.update_geos(projection_type="orthographic")

fig_choropleth.update_layout(
    title_text='Worldwide Import/Export Distribution by Area',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='orthographic'
    )
)

fig_choropleth.update_layout(height=700)

st.plotly_chart(fig_choropleth)

# New Matplotlib Scatter Plot
st.header('Import/Export Scatter Plot')

fig_scatter, ax_scatter = plt.subplots(figsize=(10, 6))
ax_scatter.scatter(filtered_data_ireland['Year'], filtered_data_ireland['Value'], color='blue', label='Ireland', alpha=0.6)
ax_scatter.scatter(filtered_data_world['Year'], filtered_data_world['Value'], color='red', label='World', alpha=0.6)
ax_scatter.set_title('Import/Export Values Scatter Plot')
ax_scatter.set_xlabel('Year')
ax_scatter.set_ylabel('Value')
ax_scatter.legend()
plt.xticks(rotation=45)
st.pyplot(fig_scatter)
