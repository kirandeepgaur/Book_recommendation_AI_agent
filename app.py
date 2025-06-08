import streamlit as st
import google.generativeai as genai

# Configure API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit UI
st.title("📚 Shelfie - Your Personal Book Curator")
st.subheader("Tell me your taste and I'll add my flavors to it.")
reader_type = st.radio("Reading level", ["First-time", "Occasional", "Seasoned"])
favorites = st.text_input("Favorite books or authors?")
genre = st.text_input("Preferred genres or themes(like romance, fantasy, self-help, classical literature, Thriller)?")
extras = st.text_input("Special requirements (like uplifting, short, diverse voices, emotional, helpful, spiritual)?")

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
    except Exception as e:
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
- 📖 Genre
- ✍️ Summary
- ⭐ Ratings
- 🎧 Audiobook info
- ⚠️ Content warnings
- 🎥 Adaptation info

Separate each recommendation clearly.
"""
    response = model.generate_content(main_prompt)
    return response.text

# Run on button click
if st.button("Get Recommendations"):
    with st.spinner("Shelfie is curating your perfect list..."):
        recommendations_text = get_recommendations()
        
        # Split on markers like 'Recommendation' or '📘'
        books = recommendations_text.split("📘")[1:]  # Skip first empty split
        for book in books:
            book_info = "📘" + book.strip()
            witty = get_witty_intro(book_info)
            st.markdown(f"### 💬 {witty}")
            st.markdown(f"```markdown\n{book_info}\n```")
