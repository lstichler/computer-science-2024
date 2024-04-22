import streamlit as st
import pandas as pd
import requests

#Defining the four different pages, one "Welcome" page, one where
#you get the recipes, one where you get the cocktails and one where you can store 
#your favourite recipe
PAGES = {
    f"{welcome_emoji} Welcome": None,
    f"{food_emoji} Recipe Ideas": None,
    f"{cocktail_emoji} Cocktail Ideas": None,
    f"{favorite_emoji } Favorite Recipes": None,
}

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

# Function to add entry to the review DataFrame
def add_entry(df, restaurant, comment, name, rating, restaurant_id):
    return df.append({
        'Restaurant': restaurant,
        'Comment': comment,
        'Name': name,
        'Rating': rating,
        'Restaurant ID': restaurant_id
    }, ignore_index=True)

# Main app
def main():
    st.title("Restaurant Reviews")
    
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
                st.session_state.reviews = add_entry(st.session_state.reviews, restaurant_choice, comment, name, rating, restaurant_id)
                st.success("Review submitted successfully!")

                # Displaying the submitted review in a separate table
                st.subheader("Recently Submitted Review:")
                st.table(st.session_state.reviews.tail(1))  # Show only the last submitted review

            # Displaying all reviews in a table
            if not st.session_state.reviews.empty:
                st.subheader("All Reviews:")
                st.dataframe(st.session_state.reviews)
        else:
            st.write("No restaurants found in this location.")

if __name__ == "__main__":
    main()
