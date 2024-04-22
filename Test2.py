import streamlit as st
import pandas as pd
import requests
import pydeck as pdk

# Function to extract 'title' from categories
def extract_titles(categories):
    return [category['title'] for category in categories]

# Function to extract the first address line and coordinates
def extract_address_and_coords(location):
    return location.get('address1', ''), location.get('coordinate', {'latitude': 0, 'longitude': 0})

# Function to fetch and clean restaurant data
def fetch_restaurants(location):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": "Bearer EN2FsqhUn487c-Hh4FeZGlJKk9i6bCC1kW45fmc4TQx1zw2sQ8CNGM57G3olkT4OYLcDtHHU_PVyJKaIIboLtnlVledeI6-UAwAor6xhNLIZxxqQ-EgExHGMXDAlZnYx"}
    params = {"term": "restaurants", "location": location}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    df = pd.DataFrame(data["businesses"])
    df['category_titles'] = df['categories'].apply(extract_titles)
    df[['address', 'coords']] = df['location'].apply(lambda loc: pd.Series(extract_address_and_coords(loc)))
    df = df.drop(['categories', 'location'], axis=1)
    return df

# Initialize session state for reviews
if 'reviews' not in st.session_state:
    st.session_state['reviews'] = pd.DataFrame(columns=['Name', 'Comment', 'Rating', 'Restaurant', 'Address', 'Categories', 'Latitude', 'Longitude'])

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
        selected_restaurant = df[df['name'] == restaurant_choice].iloc[0]
        
        # User input for review
        name = st.sidebar.text_input("Enter your name:")
        comment = st.sidebar.text_area("Enter your comment:")
        rating = st.sidebar.slider("Rate the restaurant:", 1, 5, 1)
        
        # Button to submit review
        if st.sidebar.button("Submit Review"):
            new_review = {
                'Name': name,
                'Comment': comment,
                'Rating': rating,
                'Restaurant': restaurant_choice,
                'Address': selected_restaurant['address'],
                'Categories': ', '.join(selected_restaurant['category_titles']),
                'Latitude': selected_restaurant['coords']['latitude'],
                'Longitude': selected_restaurant['coords']['longitude']
            }
            # Add to session state
            st.session_state.reviews = st.session_state.reviews.append(new_review, ignore_index=True)
            st.sidebar.success("Thank you for your review!")

        # Display all reviews
        st.write("All Reviews:")
        st.dataframe(st.session_state.reviews.drop(['Latitude', 'Longitude'], axis=1))
        
        # Display reviews on a map
        st.write("Map of Reviewed Restaurants:")
        map_data = st.session_state.reviews[['Latitude', 'Longitude']].dropna()
        st.pydeck_chart(pdk.Deck(
             map_style='mapbox://styles/mapbox/light-v9',
             initial_view_state=pdk.ViewState(
                 latitude=map_data['Latitude'].mean(),
                 longitude=map_data['Longitude'].mean(),
                 zoom=11,
                 pitch=50,
             ),
             layers=[
                 pdk.Layer(
                    'ScatterplotLayer',
                    data=map_data,
                    get_position='[Longitude, Latitude]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,
                 ),
             ],
         ))

if __name__ == "__main__":
    main()
