import os
import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])


st.title("📚 Shelfie - Your AI Book Curator")
reader_type = st.radio("Reading level", ["First-time", "Occasional", "Seasoned"])
favorites = st.text_input("Favorite books or authors?")
genre = st.text_input("Preferred genres or themes?")
extras = st.text_input("Special requirements (e.g., uplifting, short, diverse voices)?")

model = genai.GenerativeModel("gemini-2.0-flash")

if st.button("Get Recommendations"):
    prompt = f"""
You are Shelfie 📚, a personal literary curator and book recommendation agent.

Reader Type: {reader_type}
Favorite Books: {favorites}
Preferred Genres or Themes: {genre}
Special Notes or Needs: {extras}

Please recommend 5-7 books tailored to this reader. Include:
- 📘 Title and Author
- 🗓 Year
- 📖 Genre
- ✍️ Summary
- ⭐ Ratings
- 🎧 Audiobook info
- ⚠️ Content warnings
- 🎥 Adaptation info
"""

    with st.spinner("Thinking..."):
        response = model.generate_content(prompt)
        st.markdown(response.text)
