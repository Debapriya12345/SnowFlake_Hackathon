import streamlit as st
import pandas as pd
from collections import Counter

df1 =pd.read_csv("Black Spot_2019.csv")
df2 = pd.read_csv("Deathe_2019.csv",usecols=['State/Uts','Trucks/Lorries', 'Buses'])
df2["Total Accident Trucks/Lorries & Buses"] = df2['Trucks/Lorries'] + df2['Buses']
df3 = pd.read_csv("License_2019.csv",usecols=['States', 'Valid Permanent License - Number',
       'Valid Permanent License - Rank','Without Licence'])
df4 = pd.read_csv("Person Killed_2019.csv",usecols=['States/UTs','Persons Killed per 100 Accidents - 2019 - Numbers',
       'Persons Killed per 100 Accidents - 2019 - Ranks'])
df5 = pd.read_csv("State Wise Accident_2019.csv",usecols=['States/UTs','State/UT-Wise Total Number of Road Accidents during 2019 - Numbers',
       'State/UT-Wise Total Number of Road Accidents during 2019 - Rank','Total Number of  Road Accidents per 10,000 Vehicles - 2019'])
print(df3.head())

list1 = df1['States/Uts'].values
list2 = df2['State/Uts'].values

are_lists_same = Counter(list1) == Counter(list2)

print(f"Are both lists the same? {are_lists_same}")

if not are_lists_same:
    print("\nDifferences:")
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
print(df.columns)

df.drop(['States/UTs', 'States/Uts','State/Uts'], axis=1, inplace=True)


new_order = ['States', 'State/UT-Wise Total Number of Road Accidents during 2019 - Numbers',
       'State/UT-Wise Total Number of Road Accidents during 2019 - Rank',
       'Total Number of  Road Accidents per 10,000 Vehicles - 2019','Valid Permanent License - Number', 'Valid Permanent License - Rank',
       'Without Licence', 'Persons Killed per 100 Accidents - 2019 - Numbers',
       'Persons Killed per 100 Accidents - 2019 - Ranks',
       'Black spots on NH reported by the State as on 16/9/2020',
       'Trucks/Lorries', 'Buses', 'Total Accident Trucks/Lorries & Buses']

# Reorder the DataFrame columns
df = df[new_order]
#print(df.head())

text = input(" Enter the State : ")
chhattisgarh_row = df[df["States"]==text]

for column in chhattisgarh_row.columns:
    if column == 'States':
        continue
    value = chhattisgarh_row[column].values[0]
    print(f"{column}: {value}")

# # Define the options for the dropdown menu
# options = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
#        'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
#        'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala',
#        'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
#        'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim',
#        'Tamil Nadu', 'Telangana', 'Tripura', 'Uttarakhand',
#        'Uttar Pradesh', 'West Bengal', 'Andaman and Nicobar Islands',
#        'Chandigarh', 'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
#        'Lakshadweep', 'Puducherry', 'National Average']

# # Create the dropdown menu
# selected_option = st.selectbox('Choose an option:', options)

# # Display the selected option
# st.write(f'You selected: {selected_option}')

# # Add some conditional content based on the selection
# if selected_option == 'Option 1':
#     st.write('You chose the first option!')
# elif selected_option == 'Option 2':
#     st.write('You chose the second option!')
# else:
#     st.write('You chose the third option!')