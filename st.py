import streamlit as st
import pandas as pd
from PIL import Image
###################
common_animes = pd.read_csv(r"common_animes.csv", index_col="Unnamed: 0")
recommendations = pd.read_csv(r"item_based_recommendation.csv")
anime=pd.read_csv(r"anime_with_synopsis.csv")
top_anime = pd.read_csv(r"top_anime.csv")
top_anime.rename(columns={"rank":"number of members"},inplace=True)
anime.rename(columns={"MAL_ID":"anime_id"},inplace=True)
beginner = pd.read_csv(r"beginner_path.csv", index_col="Unnamed: 0")
beginner.index = [1,2,3,4,5]
######################

import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        opacity: 2;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )




# function to make predictions based on user input
def check_show(keyword):
    while True:
        common_anime_list = createList(common_animes)
        if [col for col in common_anime_list if keyword.lower() in col.lower()]==[]:
            print("----There is no such anime in this database. Try again please----")
        elif keyword=="":
            print("Please enter something valid")
        else:
            anime_list=pd.Series([col for col in common_anime_list if keyword.lower() in col.lower()])
            print(anime_list)
            return anime_list.iloc[int(input("Which one would you like to choose from this list?"))]
def createList(common_animes):
    common_animes_list = []
    for i in range(2448):
        common_animes_list.append(common_animes.iloc[i][0])
    common_animes_list.insert(0,"")
    return common_animes_list
def predict_anime(animeName):
    animeID = recommendations[animeName].values.tolist()
    return anime[anime.anime_id.isin(animeID)][["Name","sypnopsis"]].set_index("Name")
def showRecommend(columns):
    return beginner[[columns]]
st.set_page_config(page_title="Anime Recommendations", page_icon="💂", layout="wide")

image = Image.open('logo.PNG')

st.image(image, width=150)

#st.image("anime-720x420.png", width=1200)
left_col, right_col = st.columns([6,6])
# left column - top voted animes
left_col.header("Top Voted Animes")
left_col.table(top_anime[["Name","rating"]])


# right column - anime suggestion for newcomers
right_col.header("Anime Suggestion for Newcomers")
right_col.caption("Please choose category")
category = right_col.selectbox('',beginner.columns)

if category:
    showCategory = showRecommend(category)
    right_col.table(showCategory)

with st.container():
   st.header("Anime Prediction")

# middle column - input for anime predictions

#user_input = middle_col.text_input("Enter an anime name:", value="")
#common_animes_list = createList(common_animes)
user_input = st.selectbox('', createList(common_animes))

if user_input:
    predictions = predict_anime(user_input)
    st.header("Predictions:")
    st.checkbox("Click to maximize the table view", value=False, key="use_container_width")
    st.dataframe(predictions, use_container_width=st.session_state.use_container_width)

#add_bg_from_local('anime.png')

