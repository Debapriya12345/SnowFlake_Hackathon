import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
#from snowflake.snowpark import Session
import altair as alt
import plotly.express as px

df1 =pd.read_csv("Black Spot_2019.csv")
df2 = pd.read_csv("Deathe_2019.csv",usecols=['State/Uts','Trucks/Lorries', 'Buses'])
df2["Total Accident Trucks/Lorries & Buses"] = df2['Trucks/Lorries'] + df2['Buses']
df3 = pd.read_csv("License_2019.csv",usecols=['States', 'Valid Permanent License - Number',
       'Valid Permanent License - Rank','Without Licence'])
df4 = pd.read_csv("Person Killed_2019.csv",usecols=['States/UTs','Persons Killed per 100 Accidents - 2019 - Numbers',
       'Persons Killed per 100 Accidents - 2019 - Ranks'])
df5 = pd.read_csv("State Wise Accident_2019.csv",usecols=['State/UT-Wise Total Number of Road Accidents during 2016',
       'State/UT-Wise Total Number of Road Accidents during 2017',
       'State/UT-Wise Total Number of Road Accidents during 2018','States/UTs','State/UT-Wise Total Number of Road Accidents during 2019 - Numbers',
       'State/UT-Wise Total Number of Road Accidents during 2019 - Rank','Total Number of  Road Accidents per 10,000 Vehicles - 2019'])

list1 = df1['States/Uts'].values
list2 = df2['State/Uts'].values

are_lists_same = Counter(list1) == Counter(list2)


if not are_lists_same:
    diff1 = set(list1) - set(list2)
    diff2 = set(list2) - set(list1)
    
    if diff1:
        print("Elements in list1 but not in list2:", diff1)
    if diff2:
        print("Elements in list2 but not in list1:", diff2)

df1['States/Uts'] = df1['States/Uts'].replace({
    'Karnatka': 'Karnataka',
    'Uttarkhand': 'Uttarakhand',
    'Andaman and Nicobar Is.': 'Andaman and Nicobar Island',
    'Total ': 'Total',
    'Orrisa': 'Orissa',
    'Chattisgarh': 'Chhattisgarh',
    'Maharahtra': 'Maharashtra',
    'West Begal': 'West Bengal',
    'Telengana': 'Telangana'
})

order = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 
'Nagaland', 'Orissa', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand', 'Uttar Pradesh', 'West Bengal',
'Andaman and Nicobar Island', 'Chandigarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi', 'Lakshadweep', 'Puducherry', 'Total']
def reorder_df(df, column, order):
    df[column] = pd.Categorical(df[column], categories=order, ordered=True)
    return df.sort_values(column).reset_index(drop=True)

# Reorder both DataFrames
df1_ordered = reorder_df(df1, 'States/Uts', order)
df2_ordered = reorder_df(df2, 'State/Uts', order)

# Concatenate horizontally
df_result = pd.concat(([df1_ordered, df2_ordered]), axis=1)

#print(df_result)

df = pd.concat([df5,df3,df4,df_result],axis = 1)

df.drop(['States/UTs', 'States/Uts','State/Uts'], axis=1, inplace=True)

new_order = ['States', 'State/UT-Wise Total Number of Road Accidents during 2016',
       'State/UT-Wise Total Number of Road Accidents during 2017',
       'State/UT-Wise Total Number of Road Accidents during 2018','State/UT-Wise Total Number of Road Accidents during 2019 - Numbers',
       'State/UT-Wise Total Number of Road Accidents during 2019 - Rank',
       'Total Number of  Road Accidents per 10,000 Vehicles - 2019','Valid Permanent License - Number', 'Valid Permanent License - Rank',
       'Without Licence', 'Persons Killed per 100 Accidents - 2019 - Numbers',
       'Persons Killed per 100 Accidents - 2019 - Ranks',
       'Black spots on NH reported by the State as on 16/9/2020',
       'Trucks/Lorries', 'Buses', 'Total Accident Trucks/Lorries & Buses']

# Reorder the DataFrame columns
df = df[new_order]
# Define the options for the dropdown menu
options = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
       'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
       'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
       'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
       'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim',
       'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand',
       'Uttar Pradesh', 'West Bengal', 'Andaman and Nicobar Islands',
       'Chandigarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
       'Lakshadweep', 'Puducherry']
print(df)
# # Create the dropdown menu
selected_option = st.selectbox('Choose an option:', options)
print(selected_option)
# Display the selected option
if selected_option:
    st.write(f'You selected: {selected_option}')

    # # text = input(" Enter the State : ")
    selected_row = df[df["States"]==selected_option]

    for column in selected_row.columns:
        if column == 'States':
            continue
        value = selected_row[column].values[0]
        st.write(f"{column}: {value}")


if selected_option:
    if selected_option in df['States'].values:
        row_index = df[df['States'] == selected_option].index[0]
        column_index = df.columns.get_loc('State/UT-Wise Total Number of Road Accidents during 2019 - Rank')
        row_to_plot = df.iloc[row_index, 1:column_index]

        # Create a new DataFrame for the bar chart
        chart_data = pd.DataFrame({
            'Year': row_to_plot.index,
            'Accident Count': row_to_plot.values
        })

        # Define a color mapping for the years (assuming you have 4 years)
        colors = ['#88C273', '#FFE700', '#4CC9FE', '#FF8A8A']
        chart_data['Color'] = colors[:len(chart_data)]  # Assign colors based on the number of bars

        # Create the bar chart using Altair
        chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('Year:N', sort=None),  # 'N' for nominal (categorical) data
            y='Accident Count:Q',  # 'Q' for quantitative data
            color=alt.Color('Color:N', scale=None),  # Use custom colors without a scale
            tooltip=['Year', 'Accident Count']
        ).properties(
            title=f'Road Accident Statistics for {selected_option}',
            width=500,
            height=700
        )

        # Add text labels on top of each bar
        text = chart.mark_text(
            align='center',
            baseline='bottom',
            fontSize=20,
            dy=-5  # Nudges text to the top of the bar
        ).encode(
            text='Accident Count:Q'
        )

        # Combine the chart and text
        final_chart = (chart + text).interactive()

        # Display the chart in Streamlit
        st.altair_chart(final_chart, use_container_width=True)

        # Display the data in a table below the chart
        st.write("Data:")
        st.dataframe(chart_data)
    temp = row_to_plot
    accidentList =[]
    for i in range(1,len(temp)):
        diff = temp[i] - temp[i-1]
        diff = (diff/temp[i])*100
        accidentList.append(diff)
    markdown_list = "\n".join(f"- {item}" for item in accidentList)
    message = f"<h3 style='color: yellow;'>The Rate% of the Accident from 2016 -'19 for the State: {selected_option}</h3>"
    st.markdown(message, unsafe_allow_html=True)
    st.markdown(markdown_list)
else:
    st.error("Selected state not found in the data.")



df10 = pd.read_csv("professional_2019.csv",usecols=['STATES / Uts',
       'Professional - Authorised to drive public Service Vehicles - Total','Non professional - Total'])
#print(df10.head())
df10['Professional - Authorised to drive public Service Vehicles - Total'] = df10['Professional - Authorised to drive public Service Vehicles - Total'].fillna(0)
df10['Non professional - Total'] = df10['Non professional - Total'].fillna(0)

df10['Non_Professional vs Professional'] = df10['Non professional - Total'] // df10['Professional - Authorised to drive public Service Vehicles - Total']
#df10['Non_Professiinal vs Professional'].fillna(0)
df10['Non_Professional vs Professional Authorised Driver'] = df10['Non_Professional vs Professional'].fillna(0).replace([np.inf, -np.inf], 0)

# Display the selected option
if selected_option:
    #st.write(f'You selected: {selected_option}')

    # # text = input(" Enter the State : ")
    selected_row = df10[df10["STATES / Uts"]==selected_option]

    # for column in selected_row.columns:
    #     if column == 'STATES / Uts':
    #         continue
    #     value = selected_row[column].values[0]
    #     st.write(f"{column}: {value}")

def plot_driver_distribution(text):
    row = df10[df10['STATES / Uts'] == text].iloc[0]

    # Extract the values to plot
    values = [row['Professional - Authorised to drive public Service Vehicles - Total'], row['Non professional - Total']]
    categories = ['Professional', 'Non-professional']

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 6))
    bars = ax.bar(categories, values, color=['skyblue', 'lightgreen'])
    ax.set_title(f'Driver Distribution in {text}', fontsize=16)
    ax.set_ylabel('Number of Drivers', fontsize=10)
    ax.tick_params(axis='x', labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

    # Add value labels on the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + max(values) * 0.01,
                f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    
    return fig

# Streamlit app
st.title('Driver Distribution by State/UT')
for column in selected_row.columns:
    if column == 'STATES / Uts':
        continue
    value = selected_row[column].values[0]
    st.write(f"{column}: {value}")

# Plot the chart
if selected_option:
    chart = plot_driver_distribution(selected_option)
    st.pyplot(chart)
df6 = pd.read_csv("TotalRoadsVsPopulation16-17.csv",usecols=['Name of the States','Total road Length', 'Total Population','Road length per \'000 pop'])
df6_new_names = {
    'Total road Length': 'Total road Length 2017',
    'Total Population': 'Total Population 2017',
    'Road length per \'000 pop': 'Road length per \'000 pop 2017'
}
df6.rename(columns=df6_new_names, inplace=True)
#print(df6.head())
df7 = pd.read_csv("TotalRoadVsPopulation_17-18.csv",usecols=['Total road Length', 'Total Population','Road length per \'000 pop'])
df7_new_names = {
    'Total road Length': 'Total road Length 2018',
    'Total Population': 'Total Population 2018',
    'Road length per \'000 pop': 'Road length per \'000 pop 2018'
}
df7.rename(columns=df7_new_names, inplace=True)
df7.head()
df8 = pd.read_csv("TotalRoadVsPopulation_18-19.csv",usecols=['Total road Length', 'Total Population','Road length per \'000 pop'])
df8_new_names = {
    'Total road Length': 'Total road Length 2019',
    'Total Population': 'Total Population 2019',
    'Road length per \'000 pop': 'Road length per \'000 pop 2019'
}
df8.rename(columns=df8_new_names, inplace=True)
df8.head()
df9 = pd.concat([df6,df7,df8],axis = 1)
#print(df9.head())
new_order1 = ['Name of the States','Road length per \'000 pop 2017','Road length per \'000 pop 2018','Road length per \'000 pop 2019',
                'Total road Length 2017','Total road Length 2018','Total road Length 2019','Total Population 2017','Total Population 2018',
                'Total Population 2019']
df9 = df9[new_order1]



def create_bar_plot(df):
    # Create the horizontal bar plot
    df11 = df.sort_values('Non_Professional vs Professional Authorised Driver').tail(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(df11['STATES / Uts'], df11['Non_Professional vs Professional Authorised Driver'])

    # Customize the plot
    ax.set_title('Non_Professional vs Professional Authorised Driver', fontsize=16)
    ax.set_xlabel('Number of Non_Professional driver for 1(one) Professional Driver', fontsize=12)
    ax.set_ylabel('Top 10 Worst States/UTs', fontsize=12)

    # Add value labels at the end of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, f'{width:.2f}',
                ha='left', va='center')

    # Adjust layout to prevent cutting off labels
    plt.tight_layout()

    return fig

# Streamlit app
st.title('Non-Professional vs Professional Authorised Driver by State/UT')

# Create and display the plot
fig = create_bar_plot(df10)
st.pyplot(fig)

def plot_road_length(text):
    row_index = df9[df9['Name of the States'] == text].index[0]
    column_index = df9.columns.get_loc('Total road Length 2017')
    # Select the first row (index 0) and exclude the 'Category' column
    row_to_plot = df9.iloc[row_index, 1:column_index]

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(5, 5))

    # Define colors for each bar
    colors = ['#e74c3c','#21618c','#1e8449']  # Light Red, Light Blue, Light Green

    # Plot bars with different colors
    ax.set_xticks([])
    bars = ax.bar(row_to_plot.index, row_to_plot.values, color=colors)

    # Customize the plot
    ax.set_title(f'Values for the State {text}', fontsize=16)
    ax.set_xlabel('Year Wise 2017-2019', fontsize=12)
    ax.set_ylabel('Road length per 1000 population', fontsize=15)

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}', ha='center', va='bottom', fontsize=10)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    
    return fig

# Streamlit app
st.title('Road Length per 1000 Population by State')



# Plot the chart
if selected_option:
    chart = plot_road_length(selected_option)
    st.pyplot(chart)
df = pd.read_csv("StateWise_AQI_2019.csv")
val= df[df["States/UTs"]==selected_option]["AQI Index"].values
#print(df.head())

df12 = df1.nlargest(10, 'Black spots on NH reported by the State as on 16/9/2020')
# Assuming df12 is your DataFrame
df12 = df12.sort_values('Black spots on NH reported by the State as on 16/9/2020')

# Create the base bar chart
base = alt.Chart(df12).encode(
    y=alt.Y('States/Uts:N', sort='-x', title='States/UTs'),
    x=alt.X('Black spots on NH reported by the State as on 16/9/2020:Q', title='Number of Black Spots')
)

# Create bars
bars = base.mark_bar().properties(
    width=600,
    height=400,
    title='Top 10 States where most number of Black Spots on National Highways Reported by States/UTs'
)

# Add colored text labels to the end of each bar
text = base.mark_text(
    align='left',
    baseline='middle',
    dx=3,  # Adjust the position of the text
    color='white'  # Set the color of the text labels
).encode(
    text='Black spots on NH reported by the State as on 16/9/2020:Q'
)

# Combine the chart and text
final_chart = (bars + text).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16
)

# Display the chart in Streamlit
st.altair_chart(final_chart, use_container_width=True)


st.title('AQI Index by State/UT')

# Dropdown to select State/UT
states = df['States/UTs'].unique()
x_highlight = selected_option#st.selectbox('Select a State/UT to highlight', states)

# Create the scatter plot
fig = px.scatter(df, x='States/UTs', y='AQI Index', 
                 title=f'Scatter Plot of AQI Index by State/UT',
                 labels={'States/UTs': 'States Names', 'AQI Index': 'AQI Index'},
                 hover_data=['States/UTs', 'AQI Index'])

# Customize the layout
fig.update_layout(
    xaxis_tickangle=-45,
    xaxis_title='States Names',
    yaxis_title='AQI Index',
    showlegend=True,
    height=600,
    width=1000
)

# Highlight the selected state
highlighted_point = df[df['States/UTs'] == x_highlight]
if not highlighted_point.empty:
    fig.add_trace(px.scatter(highlighted_point, x='States/UTs', y='AQI Index',
                             color_discrete_sequence=['red'])
                  .data[0])

# Add the AQI value for the highlighted state to the title
val = highlighted_point['AQI Index'].values
if len(val) > 0:
    fig.update_layout(title=f'Scatter Plot with Highlighted State {x_highlight} (AQI: {val[0]:.2f})')

# Display the plot
st.plotly_chart(fig)

# Display the AQI value for the highlighted state
if len(val) > 0:
    st.write(f"The AQI Index for {x_highlight} is: {val[0]:.2f}")