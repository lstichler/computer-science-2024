import streamlit as st
import pandas as pd
import requests

def set_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://cdn.pixabay.com/photo/2016/10/20/20/47/background-1756615_1280.jpg");
            background-size: cover;
            background-position: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_image()

st.image("Logo Food Cirlce.png", width=150)

# API function to get restaurants by location
def get_restaurants(location):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": "Bearer 6fvAUhr3oMOOOEmGybAjxAoqlAmWx31FhbvGnWw5R8jIhAfvIZVSXmT4GFYMeJsGKwb-0zX_pfD_CMpIVtEzHBdZ10EZ-fvzHkb_PYhtiJ9BHx4Ng359IGfz8Ak-ZnYx",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
        "accept": "application/json"
    }
    params = {
        "term": "restaurants",
        "location": location
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if data and "businesses" in data:
        df = pd.DataFrame(data["businesses"])
        # Extract latitude and longitude if coordinates exist
        df['lat'] = df['coordinates'].apply(lambda x: x.get('latitude') if isinstance(x, dict) else None)
        df['lon'] = df['coordinates'].apply(lambda x: x.get('longitude') if isinstance(x, dict) else None)
        return df
    else:
        return pd.DataFrame()

# Main app
def main():
    st.title("FoodCircle")
    
    # Session state to store reviews
    if 'reviews' not in st.session_state:
        st.session_state.reviews = pd.DataFrame(columns=['Restaurant', 'Comment', 'Name', 'Rating', 'Restaurant ID'])

    # User selects a location
    location = st.text_input("Enter a location (e.g., 'San Francisco')", "")
    if location:
        # Fetch restaurants for the location
        restaurants_df = get_restaurants(location)
        if not restaurants_df.empty:
            # User selects a restaurant
            restaurant_choice = st.selectbox("Select a restaurant", restaurants_df['name'])
            restaurant_id = restaurants_df[restaurants_df['name'] == restaurant_choice]['id'].iloc[0]
            
            # User inputs
            name = st.text_input("Your name")
            comment = st.text_area("Your comment")
            rating = st.slider("Your rating", 1, 5, 1)
            
            # Submit review button
            submit_pressed = st.button("Submit Review")
            if submit_pressed:
                # Add the review to the DataFrame
                new_review = pd.DataFrame([{
                    'Restaurant': restaurant_choice,
                    'Comment': comment,
                    'Name': name,
                    'Rating': rating,
                    'Restaurant ID': restaurant_id
                }])
                st.session_state.reviews = pd.concat([st.session_state.reviews, new_review], axis=0)
                st.success("Review submitted successfully!")

                # Displaying the submitted review in a separate table
                st.subheader("Recently Submitted Review:")
                st.table(st.session_state.reviews.tail(1))  # Show only the last submitted review

            # Displaying all reviews in a table
            if not st.session_state.reviews.empty:
                st.subheader("All Reviews:")
                
                # Filter options
                filter_name = st.text_input("Filter by name")
                filter_rating = st.slider("Filter by rating", 1, 5, (1, 5), step=1)
                
                # Applying filters
                filtered_reviews = st.session_state.reviews
                if filter_name:
                    filtered_reviews = filtered_reviews[filtered_reviews['Name'].str.contains(filter_name, case=False)]
                filtered_reviews = filtered_reviews[(filtered_reviews['Rating'] >= filter_rating[0]) & (filtered_reviews['Rating'] <= filter_rating[1])]
                
                st.dataframe(filtered_reviews.drop('Restaurant ID', axis=1))
                coords = pd.DataFrame(columns=['lat', 'lon'])
                for restaurant_id in filtered_reviews['Restaurant ID']:
                    try:
                        # Extract latitude and longitude directly
                        restaurant_coords = restaurants_df[restaurants_df['id'] == restaurant_id][['lat', 'lon']].iloc[0]
                        coords.loc[len(coords)] = restaurant_coords
                    except Exception as e:
                        st.write(f"Failed to get coordinates for restaurant ID {restaurant_id}: {e}")
                        continue

                st.map(coords)
        else:
            st.write("No restaurants found in this location.")

if __name__ == "__main__":
    main()
