import streamlit as st

def main():
    st.title("Displaying Text with Streamlit")
    st.header("St. Gallo")
    
if __name__ == "__main__":
    main()

import streamlit as st

def main():
    # Custom style for the dark green box
    st.markdown("""
    <style>
    .dark-green-box {
        background-color: #004225;  /* Dark green color */
        color: white;               /* White text color */
        padding: 10px;              /* Padding inside the box */
        border-radius: 10px;        /* Rounded corners */
    }
    </style>
    """, unsafe_allow_html=True)

    # Creating a container with the custom style
    with st.container():
        st.markdown('<div class="dark-green-box">This is a dark green box in Streamlit!</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()


import streamlit as st
import pandas as pd
import requests

# Function to extract 'title' from categories
def extract_titles(categories):
    return [category['title'] for category in categories]

# Function to extract the first address line
def extract_address(location):
    return location.get('address1', '')

# Function to fetch and clean restaurant data
def fetch_restaurants(location):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": "Bearer EN2FsqhUn487c-Hh4FeZGlJKk9i6bCC1kW45fmc4TQx1zw2sQ8CNGM57G3olkT4OYLcDtHHU_PVyJKaIIboLtnlVledeI6-UAwAor6xhNLIZxxqQ-EgExHGMXDAlZnYx"}
    params = {"term": "restaurants", "location": location}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    df = pd.DataFrame(data["businesses"])
    df['category_titles'] = df['categories'].apply(extract_titles)
    df['address'] = df['location'].apply(extract_address)
    df = df.drop(['categories', 'location'], axis=1)
    return df

# Display function for restaurant images
def display_restaurant_image(df, restaurant_id=None, restaurant_name=None):
    if restaurant_id:
        matching_rows = df[df['id'] == restaurant_id]
    elif restaurant_name:
        matching_rows = df[df['name'].str.contains(restaurant_name, case=False, na=False)]
    else:
        st.error("No restaurant specified!")
        return

    if matching_rows.empty:
        st.warning("No matching restaurant found.")
    else:
        for _, row in matching_rows.iterrows():
            st.image(row['image_url'], caption=row['name'])

# Streamlit layout
def main():
    st.title("Restaurant Finder")
    location = st.sidebar.text_input("Enter a location (e.g., St. Gallen):")
    
    if location:
        df = fetch_restaurants(location)
        st.dataframe(df[['name', 'category_titles', 'address']])
        
        restaurant_name = st.sidebar.selectbox("Choose a restaurant to view:", df['name'])
        if st.sidebar.button("Show Image"):
            display_restaurant_image(df, restaurant_name=restaurant_name)

if __name__ == "__main__":
    main()
