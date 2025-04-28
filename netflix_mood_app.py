import streamlit as st
import pandas as pd

# Load your Netflix data
df = pd.read_csv('data/netflix_titles.csv')  # Make sure to adjust the path as per your data file

# Mood to Genres mapping
mood_to_genres = {
    'Happy': ['Comedies', 'Children & Family Movies', 'Stand-Up Comedy'],
    'Sad': ['Dramas', 'Tearjerkers'],
    'Adventurous': ['Action & Adventure', 'Thrillers'],
    'Romantic': ['Romantic Movies', 'Romantic TV Shows'],
    'Spooky': ['Horror Movies', 'Supernatural'],
}

# Recommendation function
def recommend_by_mood(mood, num_recommendations=5):
    if mood not in mood_to_genres:
        return []

    possible_genres = mood_to_genres[mood]
    mood_df = df[df['listed_in'].str.contains('|'.join(possible_genres), case=False, na=False)]

    if mood == 'Happy':
        mood_keywords = ['fun', 'happy', 'laugh', 'joy', 'smile']
    elif mood == 'Sad':
        mood_keywords = ['heartbreak', 'loss', 'emotional', 'cry']
    elif mood == 'Adventurous':
        mood_keywords = ['adventure', 'mission', 'quest', 'explore']
    elif mood == 'Romantic':
        mood_keywords = ['love', 'romance', 'relationship']
    elif mood == 'Spooky':
        mood_keywords = ['ghost', 'horror', 'fear', 'haunted']
    else:
        mood_keywords = []

    if mood_keywords:
        mood_df = mood_df[mood_df['description'].str.contains('|'.join(mood_keywords), case=False, na=False)]

    if len(mood_df) > 0:
        recommendations = mood_df.sample(n=min(num_recommendations, len(mood_df)))
    else:
        recommendations = df.sample(n=num_recommendations)
    
    return recommendations[['title', 'listed_in', 'description']]

# --- Streamlit App ---
st.title("🎬 Netflix Mood Recommender")

st.write("Choose your current mood and get the perfect Netflix picks!")

# Dropdown for mood selection
selected_mood = st.selectbox("What's your mood?", list(mood_to_genres.keys()))

# Number of recommendations
num_recs = st.slider("How many recommendations?", 1, 10, 5)

# Button to refresh
if st.button("Get Recommendations 🎯"):
    recs = recommend_by_mood(selected_mood, num_recs)
    for index, row in recs.iterrows():
        st.subheader(row['title'])
        st.caption(f"Genre: {row['listed_in']}")
        st.write(row['description'])
        st.markdown("---")
