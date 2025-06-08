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
- 🖼️ Book Cover Image (as a direct image link)
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
        books = re.split(r"\*{3,}|\n(?=\ud83d\udcd8)|\n(?=\*\*Recommendation)\s*", recommendations_text)
        for book in books:
            if not book.strip():
                continue

            witty = get_witty_intro(book)
            st.markdown(f"### 💬 {witty}")

            # Extract image URL
            image_match = re.search(r'\!\[.*?\]\((.*?)\)', book)
            image_url = image_match.group(1) if image_match else None

            # Extract Goodreads or Amazon link
            link_match = re.search(r'https?://[\w./-]+', book)
            link = link_match.group(0) if link_match else None

            if image_url:
                st.image(image_url, width=160)

            if link:
                st.markdown(f"[View on Goodreads or Amazon]({link})")

            # Clean up markdown and show rest
            cleaned = re.sub(r'https?://[\w./-]+', '', cleaned)  # remove duplicate link
            st.markdown(cleaned)
