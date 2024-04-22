import streamlit as st

def main():
    st.title("Displaying Text with Streamlit")
    st.header("St. Gallo")
    
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

# Streamlit layout
def main():
    st.title("Restaurant Finder and Reviewer")

    # User inputs for location
    location = st.sidebar.selectbox("Choose a location:", ["St. Gallen", "Zurich", "Geneva", "Basel"])
    if location:
        df = fetch_restaurants(location)
        
        # User selects a restaurant from the fetched data
        restaurant_choice = st.sidebar.selectbox("Choose a restaurant:", df['name'])
        
        # Filter data frame to get selected restaurant
        selected_restaurant = df[df['name'] == restaurant_choice]
        
        # User input for review
        name = st.sidebar.text_input("Enter your name:")
        comment = st.sidebar.text_area("Enter your comment:")
        rating = st.sidebar.slider("Rate the restaurant:", 1, 5, 1)
        
        # Button to submit review
        if st.sidebar.button("Submit Review"):
            # Display user review and restaurant info
            st.sidebar.success("Thank you for your review!")
            # Creating a DataFrame for displaying reviews
            review_data = {
                'Name': [name],
                'Comment': [comment],
                'Rating': [rating],
                'Restaurant': [restaurant_choice],
                'Address': [selected_restaurant.iloc[0]['address']],
                'Categories': [', '.join(selected_restaurant.iloc[0]['category_titles'])],
                'Image': [selected_restaurant.iloc[0]['image_url']]
            }
            review_df = pd.DataFrame(review_data)
            st.dataframe(review_df[['Name', 'Comment', 'Rating', 'Restaurant', 'Address', 'Categories']])
            
            # Option to view image
            if st.button('Show Image'):
                st.image(selected_restaurant.iloc[0]['image_url'], width=300)

if __name__ == "__main__":
    main()
