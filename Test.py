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
        "Authorization": "Bearer EN2FsqhUn487c-Hh4FeZGlJKk9i6bCC1kW45fmc4TQx1zw2sQ8CNGM57G3olkT4OYLcDtHHU_PVyJKaIIboLtnlVledeI6-UAwAor6xhNLIZxxqQ-EgExHGMXDAlZnYx"
    }
    params = {
        "term": "restaurants",
        "location": location
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if data and "businesses" in data:
        return pd.DataFrame(data["businesses"])
    else:
        return pd.DataFrame()

def main():
    st.title("FoodCircle")
    
    # Session state to store reviews
    if 'reviews' not in st.session_state:
        st.session_state.reviews = pd.DataFrame(columns=['Restaurant', 'Comment', 'Name', 'Rating', 'Restaurant ID', 'Address', 'Category'])

    # User selects a location
    location = st.text_input("Enter a location (e.g., 'San Francisco')", "")
    if location:
        restaurants_df = get_restaurants(location)
        if not restaurants_df.empty:
            restaurant_choice = st.selectbox("Select a restaurant", restaurants_df['name'])
            restaurant_id = restaurants_df[restaurants_df['name'] == restaurant_choice]['id'].iloc[0]

            name = st.text_input("Your name")
            comment = st.text_area("Your comment")
            rating = st.slider("Your rating", 1, 5, 1)

            submit_pressed = st.button("Submit Review")
            if submit_pressed:
                new_review = pd.DataFrame([{
                    'Restaurant': restaurant_choice,
                    'Comment': comment,
                    'Name': name,
                    'Rating': rating,
                    'Restaurant ID': restaurant_id
                }])
                st.session_state.reviews = pd.concat([st.session_state.reviews, new_review], axis=0)
                st.success("Review submitted successfully!")
                st.subheader("Recently Submitted Review:")
                st.table(st.session_state.reviews.tail(1))

            # Filters for displaying reviews
            st.subheader("Filter Reviews:")
            filter_name = st.text_input("Filter by name")
            filter_location = st.text_input("Filter by location")
            filter_rating = st.slider("Filter by rating", 1, 5, 1)

            filtered_reviews = st.session_state.reviews
            if filter_name:
                filtered_reviews = filtered_reviews[filtered_reviews['Name'].str.contains(filter_name)]
            if filter_location:
                filtered_reviews = filtered_reviews[filtered_reviews['Restaurant'].str.contains(filter_location)]
            if filter_rating:
                filtered_reviews = filtered_reviews[filtered_reviews['Rating'] == filter_rating]

            st.subheader("Filtered Reviews:")
            st.dataframe(filtered_reviews)

        else:
            st.write("No restaurants found in this location.")

if __name__ == "__main__":
    main()
