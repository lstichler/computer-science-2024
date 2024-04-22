import pandas as pd
import json
import requests
from IPython.display import display, Image
import streamlit as st



#Defining the emojis for the Website
clock_emoji = "⏰"
food_emoji = "🍔"
cocktail_emoji = "🍹"
favorite_emoji = "🌟"
welcome_emoji = "👋"

#Defining the four different pages, one "Welcome" page, one where
#you get the recipes, one where you get the cocktails and one where you can store 
#your favourite recipe
PAGES = {
    f"{welcome_emoji} Welcome": None,
    f"{food_emoji} Recipe Ideas": None,
    f"{cocktail_emoji} Cocktail Ideas": None,
    f"{favorite_emoji } Favorite Recipes": None,
}





#Defining a nice text format

def display_nice_text(title, text, font_size='24px'):
        st.markdown("---")
        st.markdown(f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)
        st.markdown("---")
        st.write(text)
        st.markdown("---")


#defining the welcome page
def welcome_page():

    #Setting up our logo in the middle
    logo_path = "images/Unknown.jpeg"
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(logo_path, width=250)
    
    

# Text for the welcome page
    welcome_text = """
Are you feeling hungry and looking for delicious recipes and cocktail ideas? You're in the right place! 
Explore a variety of recipes, find creative cocktail suggestions, and save your favorite dishes. 
Let's embark on a culinary adventure together!
"""

    display_nice_text(f"{welcome_emoji} Welcome to RECIPII!", welcome_text, font_size="32px")

    
    

    


    
    
#defining one function, where the code for the recipe ideas is stored
def recipe_ideas_page():

#initializing sessions state for the different variables, where they get stored

    def initialize_session_state():
        if 'number_of_servings' not in st.session_state:
            st.session_state.number_of_servings = " "
        if 'ingredient_1' not in st.session_state:
            st.session_state.ingredient_1 = " "
        if 'ingredient_2' not in st.session_state:
            st.session_state.ingredient_2 = " "
        if 'ingredient_3' not in st.session_state:
            st.session_state.ingredient_3 = " "
        if 'intolerances' not in st.session_state:
            st.session_state.intolerances = []
        if 'max_time_to_make' not in st.session_state:
            st.session_state.max_time_to_make = 20
        if 'selected_recipe_info' not in st.session_state:
            st.session_state.selected_recipe_info = None
        if 'selected_recipe' not in st.session_state:
            st.session_state.selected_recipe = None
        
        if 'favorite_recipes' not in st.session_state:
            st.session_state.favorite_recipes = []
        if 'sustainable' not in st.session_state:
            st.session_state.sustainability = " "
        

    initialize_session_state()

    # User input section
    # User can enter ingredients, cooking time, number of servings, intolerances
    st.sidebar.header("Enter your preferences")
    st.session_state.ingredient_1 = st.sidebar.text_input("Enter your first ingredient", value=st.session_state.ingredient_1)
    st.session_state.ingredient_2 = st.sidebar.text_input("Enter your second ingredient", value=st.session_state.ingredient_2)
    st.session_state.ingredient_3 = st.sidebar.text_input("Enter your third ingredient", value=st.session_state.ingredient_3)
    st.session_state.intolerances = st.sidebar.multiselect("Select intolerances", ["dairy", "egg", "gluten", "peanut", "sesame", "seafood", "shellfish", "sulfite", "soy", "tree nut", "wheat"], st.session_state.intolerances)
    st.session_state.max_time_to_make = st.sidebar.slider("Cooking time", min_value=20, max_value=100, value=st.session_state.max_time_to_make)
    st.session_state.number_of_servings = st.sidebar.number_input("Number of servings", min_value=1, step=1)

    # getting the recipe ideas with following function
    def get_recipe_idea_intolerance(ingredient_1, ingredient_2, ingredient_3, max_time_to_make, intolerances):

    # getting API
        url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

        querystring = {"includeIngredients":f"{ingredient_1}, {ingredient_2}, {ingredient_3}","type":"main course","intolerances":f"{intolerances}","instructionsRequired":"true","fillIngredients":"true","addRecipeInformation":"false","maxReadyTime":f"{max_time_to_make}","ignorePantry":"false"}
        headers = {
	"X-RapidAPI-Key": "574ead9772msha3420c23b9426d4p102917jsne4924e4d737d",
	"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}
        response = requests.get(url, headers=headers, params=querystring)

    #making the json file to a dataframe, based on results key
        json_testing = response.json()


        print("JSON Response:", json_testing)

    # Check if the 'results' key exists in the JSON response
        if "results" in json_testing:
            df_testing = pd.DataFrame(json_testing["results"])
        # ... (rest of your code)
        else:
            st.info("Try different ingredients.")
       
    # making a dataframe with only the columns we want 
        final_df = df_testing[["title", "usedIngredients", "image","id", "missedIngredientCount"]]

    # making sure the recommendation is most likely based on all the ingredients you have in your fridge 
        final_df = final_df.sort_values(by = ["missedIngredientCount"], ascending = True)

    #dropping all double food ideas
    #making final dataframe with the columns we need
        receipe_idea = pd.DataFrame(final_df[["title", "image", "id"]].drop_duplicates())
    
    #returning the final dataframe 
        return receipe_idea

        return df_testing

    df_from_function = get_recipe_idea_intolerance(st.session_state.ingredient_1, st.session_state.ingredient_2, st.session_state.ingredient_3, st.session_state.max_time_to_make, st.session_state.intolerances)

    st.session_state.selected_recipe_info = df_from_function    

    #Text for the recipe page
    recipe_text = """Discover exciting new recipes based on your preferences! Enter your favorite ingredients, set your cooking time, and explore a world of culinary delights. From main courses to desserts, we have something for every taste."""
    
    display_nice_text(f"{food_emoji} Recipe Ideas", recipe_text)

    #checking whethet the user entered ingredients
    if st.session_state.ingredient_1.strip() != "" or st.session_state.ingredient_2.strip() != "" or st.session_state.ingredient_3.strip() != "":
        #if the user entered ingredients, following will happen: 

        if st.session_state.selected_recipe_info is not None and not st.session_state.selected_recipe_info.empty:
            #Based on the ingredients, the user can choose from a selection of recipes
            selected_recipe_titles = st.session_state.selected_recipe_info['title'].tolist()
            st.markdown("<h4 style='margin-bottom: 5px; '>Select a Recipe:</h4>", unsafe_allow_html=True)
            selected_recipe = st.selectbox(" ", selected_recipe_titles, key="key_recipes")
            #BAsed on the selected recipe displaying the image
            if selected_recipe:
                selected_recipe_info = st.session_state.selected_recipe_info[st.session_state.selected_recipe_info['title'] == selected_recipe]
                for index, image in enumerate(selected_recipe_info['image']):
                    st.markdown(f"<h4 style='margin-bottom: 5px;'>{selected_recipe}</h4>", unsafe_allow_html=True)
                    st.image(image,  width = 400)

                #getting the ID from the selected recipe, to get later on the actual recipe
                ID= selected_recipe_info['id']
                ID= int(ID)
                st.session_state.number_of_servings = int(st.session_state.number_of_servings)

 
        
        
        def get_actual_recipe(ID, number_of_servings):
    
    #calling the API
            url = f"https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{ID}/information"

            headers = {
	            "X-RapidAPI-Key": "574ead9772msha3420c23b9426d4p102917jsne4924e4d737d",
	            "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
}

            response_receipe = requests.get(url, headers=headers)
    
            response_receipe = response_receipe.json()
    
    #returning the json file
            return response_receipe

        def get_food_instructions(response_receipe):
            return response_receipe['instructions']

#Sustainability
        def get_sustainability(response_receipe):
            return response_receipe['sustainable']

    ## total time
        #get preparation minutes
        def get_preparation_time(response_receipe):
            return response_receipe['preparationMinutes']

    #cooking time
        def get_cooking_time(response_receipe):
            return response_receipe["cookingMinutes"]

    #preparation + cooking
        def get_total_time(preparation_time, cooking_time):
            return preparation_time+cooking_time

        def calculate_expression(lst):
    # Joining list elements to form a string
            expression = ''.join(lst)
            try:
        # Evaluating the expression using eval()
                result = eval(expression)
                return result
            except (SyntaxError, ZeroDivisionError):
                return None  # Return None for invalid expressions or division by zero
    
    

        def det_adjusted_ingredient_quantity(response_receipe):
    
    ## making a dataframe out of the extended Ingredients, so that we can clean and prepare them in the next step
            df_ingredients= pd.DataFrame(response_receipe["extendedIngredients"])
    
    #extracting all ingredients and removing duplicates 
            list_of_ingredients = []
            for i in df_ingredients.index:
                list_of_ingredients.append(df_ingredients["original"][i])
                result = list(set(list_of_ingredients))
    
    # transforming the result list into a dataframe
            result_df = pd.DataFrame(result)
            result_df.rename(columns = {0: "ingredients"}, inplace = True)
    
    #extracting all numbers from column
            result_df['Numbers'] = result_df['ingredients'].str.findall(r'[\d+*/-]')
    
    #removing the "[]" and "," and calculating the result of the quantity
            result_df['Numbers'] = result_df['Numbers'].apply(calculate_expression)
    
    #calculating the adjusted quantity based on the amount of servings wanted
            servings = response_receipe["servings"]
            result_df['Adjusted Ingredient Quantity'] = (result_df['Numbers']/servings) * st.session_state.number_of_servings
    
    #filling the missing values, they are missing as the quantity should be a personal choice
            result_df['Adjusted Ingredient Quantity'] = result_df['Adjusted Ingredient Quantity'].fillna("As much as you desire")
    
    #extracting the text and putting in a new column 
            result_df['Ingredient'] = result_df['ingredients'].str.replace(r'[^A-Za-z\s]', '', regex=True)
    
    #only selecting the columns we want to display 
            final_df = result_df[["Adjusted Ingredient Quantity", "Ingredient"]]
    
    #returning the final dataframe 
            return final_df

        
## Calling the functions and assigning the values/dataframes so that they can later be deployed on streamlit 

#calling API function to get receipe for chosen idea
        receip_json = get_actual_recipe(ID, st.session_state.number_of_servings)

        sustainability = get_sustainability(receip_json)

# calling function to get the instructions for the receip
        food_instructions = get_food_instructions(receip_json)

# calling function to get the preparation time 
        preparation_time = get_preparation_time(receip_json)

# calling the function to get the cooking time
        cooking_time = get_cooking_time(receip_json)

# calling the function to get the total time needed
        total_time = get_total_time(preparation_time, cooking_time)

#calling the function that asjusts the quantities based on how many servings one wants
        Ingredient_quantities = det_adjusted_ingredient_quantity(receip_json)  
        
 

#Checking whether the user entered ingredients
    if st.session_state.ingredient_1.strip() != "" or st.session_state.ingredient_2.strip() != "" or st.session_state.ingredient_3.strip() != "":
            # Calling functions and assigning values/dataframes
        receip_json = get_actual_recipe(ID, st.session_state.number_of_servings)
        food_instructions = get_food_instructions(receip_json)
        preparation_time = get_preparation_time(receip_json)
        cooking_time = get_cooking_time(receip_json)
        total_time = get_total_time(preparation_time, cooking_time)
        Ingredient_quantities = det_adjusted_ingredient_quantity(receip_json)
        sustainability = get_sustainability(receip_json)

        
        #If the user entered ingredients following be displayed
        st.markdown("<h4 style='margin-bottom: 1px; '>Ingredients:</h4>", unsafe_allow_html=True)
        st.table(Ingredient_quantities)
        
        st.markdown("<h4 style='margin-bottom: 1px; '>Cooking Time:</h4>", unsafe_allow_html=True)
        st.write(f"{clock_emoji} The preparation time is: {preparation_time} minutes")
        st.write(f"{clock_emoji} The cooking time is: {cooking_time} minutes")
        st.write(f"{clock_emoji} The total Cooking Time is: {total_time} minutes")
        st.write(f"The recipe is sustainable: {sustainability}")

        #Possibility to add the recipe to your favorite database
        if st.button("Add to Favorites"):
            favorite_recipes = st.session_state.get("favorite_recipes", [])
            favorite_recipes.append({
                "title": selected_recipe,
                "ingredients": Ingredient_quantities.to_dict(),
                "preparation_time": preparation_time,
                "cooking_time": cooking_time,
                "total_time": total_time,
                "instructions": food_instructions
            })
            st.session_state.favorite_recipes = favorite_recipes
            st.success(f"{selected_recipe} has been added to your favorites!")

        #If the user wants to see the Instructions
        if st.checkbox("Show Cooking Instructions"):
            st.markdown(food_instructions)


   
        

    #otherwise, following warning will occur
    else:
            st.info("Please enter ingredients to get recipe ideas.")

###COCKTAIL IDEAS###
#Defining one function for cocktail ideas
def cocktail_ideas():
#Text for cocktail page
    cocktail_text = """ Thirsty for a refreshing drink? Enter your preferred type of alcohol, and we'll serve you a selection of delightful cocktail recipes. Whether it's a classic or a unique concoction, find the perfect drink to elevate your spirits. """
    display_nice_text(f"{cocktail_emoji} Cocktail Ideas", cocktail_text)

    #initializing the session state for the variables for the cocktails
    def initialize_session_state():
        if 'type_of_alcohol' not in st.session_state:
            st.session_state.type_of_alcohol = " "
        if 'selected cocktails' not in st.session_state:
            st.session_state.selected_cocktails = " "

    initialize_session_state()

    # User input section
    st.sidebar.header("Enter your preferences")
    st.session_state.type_of_alcohol = st.sidebar.text_input("Enter your type of alcohol", value=st.session_state.type_of_alcohol)

    #Checking if the user entered any type of alcohol
    if st.session_state.type_of_alcohol.strip() != "":

        def get_cocktail_idea(type_of_alcohol):
    #calling API
            url = "https://the-cocktail-db.p.rapidapi.com/search.php"

            querystring = {"s":f"{type_of_alcohol}"}

            headers = {
	        "X-RapidAPI-Key": "574ead9772msha3420c23b9426d4p102917jsne4924e4d737d",
	        "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
}
            response = requests.get(url, headers=headers, params=querystring)
            cocktails = response.json()

            
    
    #transforming everything under the drinks key into a dataframe
            df_cocktails = pd.DataFrame(cocktails["drinks"])
            df_cocktails = df_cocktails[["strDrink", "idDrink"]]
            
            return df_cocktails

        df_cocktail_idea = get_cocktail_idea(st.session_state.type_of_alcohol)

        st.session_state.cocktail_idea = df_cocktail_idea

    #User chooses his cocktail, based on the given ideas, based on the type of alcohol (user input)
        st.session_state.selected_cocktails = st.selectbox("Select a Cocktail", st.session_state.cocktail_idea['strDrink'], key="key_cocktails")


# SOURCE: 
# - how to call API, copy code from website: https://rapidapi.com/thecocktaildb/api/the-cocktail-db/

    
        #Checking whether the user entered type of alcohol
        #If the user entered alcohol based on a given selection, the ID for this cocktail will be stored
        if st.session_state.selected_cocktails:
            selected_cocktails_info = st.session_state.cocktail_idea[st.session_state.cocktail_idea["strDrink"] == st.session_state.selected_cocktails]

        ID = selected_cocktails_info['idDrink']
        ID_cock = int(ID)
    

        pd.set_option('display.max_colwidth', None)


#this function was built to call the API 
        def get_cocktail_info_API(ID_cock):
    
    #calling API
            url = "https://the-cocktail-db.p.rapidapi.com/lookup.php"

            querystring = {"i":f"{ID_cock}"}

            headers = {
	        "X-RapidAPI-Key": "574ead9772msha3420c23b9426d4p102917jsne4924e4d737d",
	        "X-RapidAPI-Host": "the-cocktail-db.p.rapidapi.com"
}

            response = requests.get(url, headers=headers, params=querystring)
            cocktails_ing = response.json()
    
    #Making json file from API into a Dataframe, but only based on the drinks key
            cocktails_ing_df = pd.DataFrame(cocktails_ing["drinks"])
    
    #returning Dataframe
            return cocktails_ing_df   



#This function was made to get a list of all the ingredients used
        def get_cock_ingredients(df):
    
    # a list of all column names 
            cock_ing_list = ["strIngredient1", "strIngredient2", "strIngredient3", "strIngredient4", "strIngredient5", "strIngredient6", "strIngredient7", "strIngredient8", "strIngredient9", "strIngredient10", "strIngredient11", "strIngredient12", "strIngredient13", "strIngredient14", "strIngredient15"]
    
    #making an empty list to then append all columnnames that include values
            cock_ing_list_counting = []

    # for loop to find all the non-null values, meaning we only want use the ingredientn column if it also includes
    # ingredients, because many of them are empty, depending on how many ingredients are needed. 
            for i in cock_ing_list:
                non_null_count = df[i].notnull().sum() 
                if non_null_count == 1:
                    cock_ing_list_counting.append(i)
    
    #making an empty dataframe to then add all the columns that do actually include ingredients
            ing_df = pd.DataFrame()

    #looping throught the original dataframe with the list of columns whose rows include data, to then add them
    # to the final dataframe
            for i in cock_ing_list_counting:
                ing_df[i] = df[i]
    
    #returning the final dataframe    
            return ing_df
    

#This function was made count the total ingredients used, so that we can later only take the same amount of the 
# measurement columns 
        def get_cock_ingredients_amount(df):
    
    # a list of all column names 
            cock_ing_list = ["strIngredient1", "strIngredient2", "strIngredient3", "strIngredient4", "strIngredient5", "strIngredient6", "strIngredient7", "strIngredient8", "strIngredient9", "strIngredient10", "strIngredient11", "strIngredient12", "strIngredient13", "strIngredient14", "strIngredient15"]
    
    #making an empty list to then append all columnnames that include values
            cock_ing_list_counting = []

    # for loop to find all the non-null values, meaning we only want use the ingredientn column if it also includes
    # ingredients, because many of them are empty, depending on how many ingredients are needed. 
            for i in cock_ing_list:
                non_null_count = df[i].notnull().sum() 
                if non_null_count == 1:
                    cock_ing_list_counting.append(i)
    
    #making an empty dataframe to then add all the columns that do actually include ingredients
            ing_df = pd.DataFrame()

    #looping throught the original dataframe with the list of columns whose rows include data, to then add them
    # to the final dataframe
            for i in cock_ing_list_counting:
                ing_df[i] = df[i]
        
            amount_of_ingredients = ing_df.shape[1]
    
    #returning the final dataframe    
            return amount_of_ingredients


#function to a dataframe with the measurements for the ingredients 
        def get_measurements(df):
    
    # using the function that counts the amount of ingredients the cocktail has
            amount = get_cock_ingredients_amount(step_1_get_cock_info_API)
    
    #a list of all the column names that could include measurements 
            cock_ing_list_mes = ['strMeasure1', 'strMeasure2',
       'strMeasure3', 'strMeasure4', 'strMeasure5', 'strMeasure6',
       'strMeasure7', 'strMeasure8', 'strMeasure9', 'strMeasure10',
       'strMeasure11', 'strMeasure12', 'strMeasure13', 'strMeasure14',
       'strMeasure15']
    
    #slicing the list to only the columns that have measurements. 
    # disclaimer: it is expected that there will only be a value in the strMeasuren column if there is also one in 
    # strIngredientn column. 
            columns_filled = cock_ing_list_mes[:amount]
    
    #making empty dataframe to store dataframe with ingredients 
            ing_df_mes = pd.DataFrame()

    #foor loop to make a final dataframe with only the measurement columns that include measurements 
            for i in columns_filled:
                ing_df_mes[i] = step_1_get_cock_info_API[i]
    
    #returning the final measurement dataframe
                return ing_df_mes


#function to get the cocktail instructions
        def get_instructions(df):
            return df['strInstructions']

#function to get the type of glass needed for the cocktail
        def get_type_of_glass(df):
            return df['strGlass']


## Calling on all the functions and assigning them, so that they can be deployed on streamlit

#using the function to call the API
        step_1_get_cock_info_API = get_cocktail_info_API(ID_cock)

#using the function to get the ingredient dataframe
        cock_ingredient_dataframe = get_cock_ingredients(step_1_get_cock_info_API)

#using the function for getting the instructions
        cock_instructions = get_instructions(step_1_get_cock_info_API)

#using the function for getting the type of glass needed
        cock_glass = get_type_of_glass(step_1_get_cock_info_API)

#using the function for getting the measurements for the ingredients 
        get_measurements(step_1_get_cock_info_API)

#If user entered Alcohol, following will be displayed
        
        st.markdown("<h2>Ingredients</h2>", unsafe_allow_html=True)
        cock_ingredient_dataframe.columns = cock_ingredient_dataframe.columns.str.replace(r'^str', '', regex=True)

        st.table(cock_ingredient_dataframe)
        st.markdown("<h2>Cocktail Instruction</h2>", unsafe_allow_html=True)  
        import re
        cleaned_instructions = re.sub(r'^\d+\s+', '', cock_instructions.iloc[0]).strip()
        st.markdown(cleaned_instructions)

        st.markdown("<h2>Cocktail Glass </h2>", unsafe_allow_html=True)  
        st.markdown(f"The needed cocktail glass is: {cock_glass.iloc[0]}")
        st.markdown(f"These are the needed measurements {get_measurements(step_1_get_cock_info_API)}")

#otherwise following warning will occur
    else:
        st.info("Please enter types of alcohol to get cocktail ideas.")

#defining one function, where the favourite recipes will be displayed
def favorite_recipes():
    
#Text for favorite recipe page
    favorite_text = """ Curate your collection of favorite recipes! Save the dishes you love, revisit cooking instructions, and share your culinary triumphs. Your personalized cookbook awaits with all the recipes that have won your heart. """
    display_nice_text(f"{favorite_emoji} Favorite Recipes", favorite_text)
    
    favorite_recipes = st.session_state.get("favorite_recipes", [])

#checking if user entered any favorite recipes
    if not favorite_recipes:
        st.info("You haven't added any recipes to your favorites yet.")
#Otherwise the favorite recipe will be displayed in the following way
    else:
        # Create a selectbox to choose a recipe
        selected_recipe = st.selectbox("Select a Recipe", [recipe["title"] for recipe in favorite_recipes])

        # Display details of the selected recipe
        for recipe in favorite_recipes:
            if recipe["title"] == selected_recipe:
                st.subheader(recipe["title"])
                st.markdown("<h4 style='margin-bottom: 1px; '>Ingredients:</h4>", unsafe_allow_html=True)
                st.table(recipe["ingredients"])
                st.markdown("<h4 style='margin-bottom: 1px; '>Cooking Time:</h4>", unsafe_allow_html=True)
                st.write(f"{clock_emoji}The preparation time is: {recipe['preparation_time']}")
                st.write(f"{clock_emoji}The cooking time is: {recipe['cooking_time']}")
                st.write(f"{clock_emoji}The total Cooking Time is: {recipe['total_time']}")
                
                st.markdown("<h4 style='margin-bottom: 1px; '>Instructions:</h4>", unsafe_allow_html=True)
                if st.checkbox("Show Cooking Instructions"):
                    st.write(recipe["instructions"])


#Setting up the selectbox on the sidebar to navigate through the pages
def main():
    
    # Create a sidebar for navigation
    page = st.sidebar.selectbox("Select a page", list(PAGES.keys()))

    # Display the selected page
    if page == f"{welcome_emoji} Welcome":
        welcome_page()
    elif page == f"{food_emoji} Recipe Ideas":
        recipe_ideas_page()
    elif page == f'{cocktail_emoji} Cocktail Ideas':
        cocktail_ideas()
    elif page == f'{favorite_emoji} Favorite Recipes':
        favorite_recipes()

if __name__ == "__main__":
    main()




