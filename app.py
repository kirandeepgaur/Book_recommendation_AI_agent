import streamlit as st
import google.generativeai as genai
import re

# Configure API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit UI
st.title("📚 Shelfie - Your Personal Book Curator")
st.subheader("Tell me your taste and I'll add my flavors to it.")
reader_type = st.radio("Reading level", ["First-time", "Occasional", "Seasoned"])
favorites = st.text_input("Favorite books or authors?")
genre = st.text_input("Preferred genres or themes (e.g., romance, fantasy, self-help, classical literature, thriller)?")
extras = st.text_input("Special requirements (e.g., uplifting, short, diverse voices, emotional, helpful, spiritual)?")

model = genai.GenerativeModel("gemini-2.0-flash")

# Function to get witty intro per book
def get_witty_intro(book_text):
    witty_prompt = f"""
You are Shelfie, the literary AI with charm and wit. Given the following book information, write a short, witty one-liner to introduce this book recommendation. Make it playful or intriguing depending on the genre.

Book details:
{book_text}
"""
    try:
        response = model.generate_content(witty_prompt)
        return response.text.strip().replace("\n", " ")
    except Exception:
        return "📌 A great read awaits..."

# Function to get and process book recommendations
def get_recommendations():
    main_prompt = f"""
You are Shelfie 📚, a personal literary curator and book recommendation agent.

Reader Type: {reader_type}
Favorite Books: {favorites}
Preferred Genres or Themes: {genre}
Special Notes or Needs: {extras}

Please recommend 5-7 books tailored to this reader. For each book, include:
- 📘 Title and Author
- 🗓 Year
- 📚 Genre
- ✍️ Summary
- ⭐ Ratings
- 🎧 Audiobook info
- ⚠️ Content warnings
- 🎥 Adaptation info
- 🔗 Clickable Goodreads or Amazon Link

Separate each recommendation clearly. Respond in markdown.
"""
    response = model.generate_content(main_prompt)
    return response.text

# Run on button click
if st.button("Get Recommendations"):
    with st.spinner("Shelfie is curating your perfect list..."):
        recommendations_text = get_recommendations()

        # Split recommendations by "###" or some consistent pattern
##        books = re.split(r"\*{3,}|\n(?=\ud83d\udcd8)|\n(?=\*\*Recommendation)\s*", recommendations_text)
##        for book in books:
##            if not book.strip():
##                continue

            # Split on markers like '📘 Title and Author'
        books = recommendations_text.split("📘")[1:]  # Skip initial empty
        for book in books:
            book_info = "📘" + book.strip()
            witty = get_witty_intro(book_info)
            st.markdown(f"### 💬 {witty}")
            st.markdown(book_info, unsafe_allow_html=False)
