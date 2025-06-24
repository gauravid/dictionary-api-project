import streamlit as st
import requests

# Sidebar theme toggle
theme = st.sidebar.radio("🌗 Theme", ("Light", "Dark"))

# Inject CSS for full theme override
def apply_theme(theme):
    if theme == "Dark":
        st.markdown("""
            <style>
            html, body, [class*="css"] {
                background-color: #111 !important;
                color: #EEE !important;
            }
            .stApp {
                background-color: #111 !important;
                color: #EEE !important;
            }
            input, textarea {
                background-color: #333 !important;
                color: white !important;
            }
            .stButton>button {
                background-color: #444 !important;
                color: white !important;
            }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            html, body, [class*="css"] {
                background-color: #FFF !important;
                color: #000 !important;
            }
            .stApp {
                background-color: #FFF !important;
                color: #000 !important;
            }
            input, textarea {
                background-color: #FFF !important;
                color: #000 !important;
            }
            .stButton>button {
                background-color: #EEE !important;
                color: #000 !important;
            }
            </style>
        """, unsafe_allow_html=True)

apply_theme(theme)
st.title("📚 Dictionary App")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# Input field with persistent value
word = st.text_input(
    "Enter a word:",
    value="" if st.session_state.clear_input else st.session_state.get("word_input", ""),
    key="word_input"
)

# Reset clear_input flag after applying it
if st.session_state.clear_input:
    st.session_state.clear_input = False

# Meaning function
def get_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        st.subheader(f"📘 Word: {data[0]['word']}")

        # Phonetic text
        phonetic = data[0].get('phonetic', '')
        if phonetic:
            st.markdown(f"**🔊 Pronunciation (text):** _{phonetic}_")

        # Audio pronunciation
        audio_url = next((p.get("audio") for p in data[0].get("phonetics", []) if p.get("audio")), None)
        if audio_url:
            st.markdown("**▶️ Pronunciation (audio):**")
            st.audio(audio_url)

        # Meanings
        for meaning in data[0]['meanings']:
            st.markdown("---")
            st.markdown(f"**🔹 Part of Speech:** {meaning['partOfSpeech']}")
            st.markdown(f"**📖 Meaning:** {meaning['definitions'][0]['definition']}")
            example = meaning['definitions'][0].get('example', 'No example available.')
            st.markdown(f"**💬 Example:** {example}")

            synonyms = meaning['definitions'][0].get('synonyms', [])
            if synonyms:
                st.markdown(f"**🔁 Synonyms:** {', '.join(synonyms[:5])}")

    except Exception as e:
        st.error("❌ Word not found or an error occurred.")

# Show result and track history
if word:
    if word not in st.session_state.history:
        st.session_state.history.append(word)
    get_meaning(word)

# Search history
if st.session_state.history:
    st.markdown("## 📜 Search History")
    for w in reversed(st.session_state.history[-5:]):
        st.write(f"🔸 {w}")

# Reset button
if st.button("🔄 Clear"):
    st.session_state.history = []
    st.session_state.clear_input = True
    st.rerun()
