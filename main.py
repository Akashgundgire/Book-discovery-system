import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Read data
final_rating = pd.read_csv("final.csv")
book_pivot = final_rating.pivot_table(columns='User-ID', index='Book-Title', values='Book-Rating')
book_pivot.fillna(0, inplace=True)
score = cosine_similarity(book_pivot)
final_rating.drop_duplicates(['Book-Title'], inplace=True)

def recommend(book_name):
    recommended_books = []

    try:
        index = np.where(book_pivot.index == book_name)[0][0]
        similar_items = sorted(list(enumerate(score[index])), key=lambda x: x[1], reverse=True)[1:6]

        for i in similar_items:
            recommended_books.append(book_pivot.index[i[0]])

        filtered_data = final_rating[final_rating['Book-Title'].isin(recommended_books)]

        for index, row in filtered_data.iterrows():
            # Display small image
            st.markdown(f'<img src="{row["Image-URL-M"]}" alt="Book Cover" style="width:100px; height:150px;">',
                        unsafe_allow_html=True)
            st.write("Book Title:", row['Book-Title'])
            st.write("Book Author:", row['Book-Author'])
            st.write("Year of Publication:", row['Year-Of-Publication'])
            st.write("Publisher:", row['Publisher'])
            st.write("Book-Rating:", row['Book-Rating'])
            st.write("-------------------------------")

    except IndexError:
        st.success("That book is not available.")

# Streamlit UI
tab1, tab2 = st.tabs(["Recommendation", "Trending Books"])

with tab1:
    st.title("Discover Your Next Favorite Book")
    st.write(
        "Welcome to the Book Discovery App! 📚✨\n\n"
        "Discovering your favorite book can be an exciting journey. Whether you're into "
        "mysteries, fantasies, or heartwarming stories, this app is designed to help you "
        "find the perfect read. Simply enter a book name in the input box and click 'Recommend'. "
        "Explore the recommendations and who knows, your next favorite book might be just a click away!"
    )
    # User input for book name
    book_name_input = st.text_input("Enter Book Name:")
    if st.button("Recommend"):
        recommend(book_name_input)

with tab2:
    st.title("Trending Books")
    x = final_rating[final_rating['Book-Rating'] > 5].head(50)
    for index, row in x.iterrows():
        st.markdown(f'<img src="{row["Image-URL-M"]}" alt="Book Cover" style="width:100px; height:150px;">',
                    unsafe_allow_html=True)
        st.write("Book Title:", row['Book-Title'])
        st.write("Book Author:", row['Book-Author'])
        st.write("Year of Publication:", row['Year-Of-Publication'])
        st.write("Publisher:", row['Publisher'])
        st.write("Book-Rating:", row['Book-Rating'])
        st.write("-------------------------------")
