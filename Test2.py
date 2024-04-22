import streamlit as st
import pandas as pd
import requests

# Function to extract 'title' from categories
def extract_titles(categories):
    return [category['title'] for category in categories]

# Function to extract the first address line and coordinates
def extract_address_and_coords(location):
    address = location.get('address1', '')
    coords = location.get('coordinates', {'latitude': 0, 'longitude': 0})
    return address, coords['latitude'], coords['longitude']

# Function to fetch and clean restaurant data
def fetch_restaurants(location):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": "Bearer EN2FsqhUn487c-Hh4FeZGlJKk9i6bCC1kW45fmc4TQx1zw2sQ8CNGM57G3olkT4OYLcDtHHU_PVyJKaIIboLtnlVledeI6-UAwAor6xhNLIZxxqQ-EgExHGMXDAlZnYx"}
    params = {"term": "restaurants", "location": location}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    df = pd.DataFrame(data["businesses"])
    df['category_titles'] = df['categories'].apply(extract_titles)
    df[['address', 'latitude', 'longitude']] = df['location'].apply(lambda loc: pd.Series(extract_address_and_coords(loc)))
    df = df.drop(['categories', 'location'], axis=1)
    return df

# Initialize session state for reviews
if 'reviews' not in st.session_state:
    st.session_state['reviews'] = pd.DataFrame(columns=['Name', 'Comment', 'Rating', 'Restaurant', 'Address', 'Categories', 'Latitude', 'Longitude'])

def main():
    st.title("Restaurant Finder and Reviewer")
    
    # Step 1: Let the user select a location
    location = st.selectbox("Choose a location:", ["St. Gallen", "Zurich", "Geneva", "Basel"], key='location')
    df = fetch_restaurants(location)
    
    # Step 2: Let the user select a restaurant
    restaurant_choice = st.selectbox("Choose a restaurant:", df['name'], key='restaurant')
    
    # Step 3: Let the user enter his or her name
    name = st.text_input("Enter your name:", key='name')
    
    # Step 4: Let the user give a comment
    comment = st.text_area("Enter your comment:", key='comment')
    
    # Step 5: Let the user give a rating of 1 to 5 stars
    rating = st.slider("Rate the restaurant:", 1, 5, 1, key='rating')
    
    # Submit button for the review
if st.button("Submit Review"):
    selected_restaurant = df[df['name'] == restaurant_choice].iloc[0]
    new_review = {
        'Name': name,
        'Comment': comment,
        'Rating': rating,
        'Restaurant': restaurant_choice,
        'Address': selected_restaurant['address'],
        'Categories': ', '.join(selected_restaurant['category_titles']),
        'Latitude': selected_restaurant['latitude'],
        'Longitude': selected_restaurant['longitude']
    }
    # Append to session state
    st.session_state.reviews = pd.concat([st.session_state.reviews, pd.DataFrame([new_review])], ignore_index=True)
    st.success("Thank you for your review!")


    # Display all reviews
    st.write("All Reviews:")
    st.dataframe(st.session_state.reviews.drop(['Latitude', 'Longitude'], axis=1))

if __name__ == "__main__":
    main()
