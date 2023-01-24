import pandas as pd
pd.options.display.max_columns = 50
pd.options.display.float_format = '{:.1f}'.format
pd.set_option('display.float_format', lambda x: '%.4f' % x)
pd.set_option('display.expand_frame_repr', False)

anime=pd.read_csv(r"C:\Users\ONUR\PycharmProjects\animiuul\anime_with_synopsis.csv")

rating=pd.read_csv(r"C:\Users\ONUR\PycharmProjects\animiuul\rating_complete.csv",
                  dtype={'user_id': 'int32',"anime_id":"int32","rating":"int8"})

user_anime_df = pd.read_csv(r"C:\Users\ONUR\PycharmProjects\animiuul\user_anime_df.csv")
recommend = pd.read_csv(r"C:\Users\ONUR\PycharmProjects\animiuul\item_based_recommendation.csv")
user_anime_df.columns=[int(col) if col!="user_id" else col for col in user_anime_df.columns]

anime.rename(columns={"MAL_ID":"anime_id"},inplace=True)
df=anime[["anime_id","Name"]].merge(rating,how="left",on="anime_id")
comment_counts=pd.DataFrame(df.Name.value_counts())

# Eşik değer 500
otakus=pd.DataFrame(df.user_id.value_counts()).rename(columns={"user_id": "number_of_rating"})
otaku_users=otakus[otakus["number_of_rating"]>500].index

common_animes=comment_counts[comment_counts.Name>5000].index
final_df = df[(df.user_id.isin(otaku_users)) & (df.Name.isin(common_animes))]
final_df.dropna(inplace=True)

rating=final_df[["user_id","anime_id","rating"]]
rating.user_id=rating.user_id.astype("int32")
rating.anime_id=rating.anime_id.astype("int32")
rating.rating=rating.rating.astype("int8")

def check_show(dataframe):
    while True:
        keyword=input("Which anime would you like to check in our database?\n\n")
        if [col for col in dataframe if keyword.lower() in col.lower()]==[]:
            print("----There is no such anime in this database. Try again please----")
        elif keyword=="":
            print("Please enter something valid")
        else:
            anime_list=pd.Series([col for col in dataframe if keyword.lower() in col.lower()])
            print(anime_list)
            return anime[anime["Name"]==anime_list.iloc[int(input("Which one would you like to choose from this list?"))]].anime_id.iloc[0]
# For individual queries
def item_based_recommender(anime, user_anime_df):
    anime_name=check_show(anime)
    anime_matrix = user_anime_df[anime_name]
    return user_anime_df.corrwith(anime_matrix).sort_values(ascending=False).head(10).index.tolist()
#For creating a recommendation database
def item_based_recommenders(anime_name, user_anime_df):
    name=anime[anime.Name==anime_name].anime_id.iloc[0]
    anime_matrix = user_anime_df[name]
    return user_anime_df.corrwith(anime_matrix).sort_values(ascending=False).head(10).index.tolist()

recommend=item_based_recommenders(common_animes,user_anime_df)
#recommend = pd.read_csv(r"animiuul\item_based_recommendation.csv")
