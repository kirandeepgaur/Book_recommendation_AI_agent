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

Separate each recommendation clearly. Respond in markdown with two newlines between sections.
"""
    response = model.generate_content(main_prompt)
    return response.text

# Run on button click
if st.button("Get Recommendations"):
    with st.spinner("Shelfie is curating your perfect list..."):
        recommendations_text = get_recommendations()

        # Split recommendations
        books = re.split(r"\*{3,}|\n(?=📘)|\n(?=###)|\n(?=\*\*Recommendation)", recommendations_text)

        for book in books:
            book = book.strip()
            if not book:
                continue

            # Clean up markdown before display
            cleaned = re.sub(r'\!\[.*?\]\(.*?\)', '', book)  # remove image markdown
            cleaned = re.sub(r'https?://[\w./-]+', '', cleaned)  # remove bare URLs
            cleaned = re.sub(r"(📘|🗓|📚|✍️|⭐|🎧|⚠️|🎥|🔗)", r"\n\1", cleaned)  # line breaks for readability

            witty = get_witty_intro(cleaned)
            st.markdown(f"### 💬 {witty}\n", unsafe_allow_html=True)
            st.markdown(cleaned + "\n---\n", unsafe_allow_html=True)

            # Extract Goodreads or Amazon link
            link_match = re.search(r'https?://[\w./-]+', book)
            if link_match:
                st.markdown(f"[View on Goodreads or Amazon]({link_match.group(0)})")
