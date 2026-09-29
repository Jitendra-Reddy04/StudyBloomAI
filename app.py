import streamlit as st

from rag.generate import answer
from rag.ingest import chunk_pages, load_pdf
from rag.store import VectorStore


# PAGE CONFIG

st.set_page_config(
    page_title="StudyBloom AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)


# PINK THEME

st.markdown("""
<style>

 

    .stApp {
        background: linear-gradient(
            135deg,
            #fff7fb 0%,
            #fdf2f8 50%,
            #faf5ff 100%
        );
    }




    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #50024f 0%,
            #831843 55%,
            #9d174d 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }



    h1 {
        color: #831843 !important;
        font-size: 42px !important;
        font-weight: 800 !important;
    }

    h2, h3 {
        color: #9d174d !important;
    }



    .stApp p,
    .stApp li {
        color: #3f3f46;
    }



    .stButton > button {
        background: linear-gradient(
            90deg,
            #ec4899,
            #be185d
        );

        color: white !important;

        border: none;
        border-radius: 12px;

        font-weight: 700;

        min-height: 42px;

        box-shadow:
            0 5px 15px rgba(236, 72, 153, 0.25);

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #db2777,
            #9d174d
        );

        transform: translateY(-2px);
    }




    [data-testid="stChatMessage"] {
        border-radius: 20px;

        margin-bottom: 15px;

        padding: 15px 18px;

        box-shadow:
            0 5px 18px rgba(157, 23, 77, 0.10);

        border: 1px solid #fbcfe8;
    }



    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) {
        background: linear-gradient(
            135deg,
            #ec4899,
            #be185d
        );

        border: none;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) p,
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) span,
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-user"]
    ) div {
        color: white !important;
    }




    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) {
        background: white;

        border: 1px solid #f9a8d4;
    }

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) p,
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) li {
        color: #be185d !important;
    }


    /* AI headings */

    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) h1,
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) h2,
    [data-testid="stChatMessage"]:has(
        [data-testid="chatAvatarIcon-assistant"]
    ) h3 {
        color: #831843 !important;
    }



    [data-testid="stChatInput"] {
        background: #ffffff;

        border: 2px solid #f9a8d4;

        border-radius: 20px;

        box-shadow:
            0 5px 20px rgba(236, 72, 153, 0.12);
    }




    [data-testid="stChatInput"] textarea {
        color: #831843 !important;

        font-size: 16px !important;
    }




    [data-testid="stChatInput"] textarea::placeholder {
        color: #be7aa0 !important;
        opacity: 1 !important;
    }



    [data-testid="stExpander"] {
        background: #fff7fb;

        border: 1px solid #fbcfe8;

        border-radius: 14px;
    }

    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li {
        color: #831843 !important;
    }


    [data-testid="stFileUploader"] {
        border: 2px dashed #f9a8d4;

        border-radius: 15px;

        background: rgba(255,255,255,0.08);
    }



    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    .stSlider {
        padding-bottom: 10px;
    }
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# SESSION STATE

if "messages" not in st.session_state:
    st.session_state.messages = []

if "indexed" not in st.session_state:
    st.session_state.indexed = False


# SIDEBAR

with st.sidebar:

    st.markdown("# 🌸 StudyBloom AI")

    st.caption("Your AI-powered study companion")

    st.divider()


    # PDF UPLOAD

    st.subheader("📚 Upload Notes")

    files = st.file_uploader(
        "Upload your study PDFs",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed"
    )


    # SETTINGS

    st.subheader("⚙️ Settings")

    size = st.slider(
        "Chunk size (words)",
        100,
        400,
        200,
        50
    )

    k = st.slider(
        "Passages to retrieve (k)",
        1,
        8,
        6
    )


    # BUILD INDEX

    if st.button(
        "🌸 Build Knowledge Index",
        use_container_width=True,
        type="primary",
        disabled=not files
    ):

        with st.spinner("🌷 Reading your notes..."):

            pages = [
                page
                for file in files
                for page in load_pdf(file, file.name)
            ]

            chunks = chunk_pages(
                pages,
                size=size,
                overlap=size // 5
            )

            if chunks:

                st.session_state.store = VectorStore(chunks)

                st.session_state.indexed = True

                st.session_state.messages = []

                st.success(
                    f"✨ {len(chunks)} passages indexed successfully!"
                )

            else:

                st.error(
                    "No text found in the PDF."
                )


    # STATUS

    if st.session_state.indexed:

        st.success(
            "🟢 StudyBloom AI is ready!"
        )


    st.divider()

    st.caption(
        "🌸 Learn smarter with StudyBloom AI"
    )


# MAIN TITLE

st.title("🌸 StudyBloom AI")

st.write(
    "✨ Ask questions from your notes and get "
    "answers based on your uploaded documents."
)

st.divider()


# CHAT HISTORY

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👩‍🎓"
        ):

            st.markdown(message["content"])

    else:

        with st.chat_message(
            "assistant",
            avatar="🌸"
        ):

            st.markdown(message["content"])

            # Show sources

            if message.get("sources"):

                with st.expander("📚 View Sources"):

                    for source in message["sources"]:

                        st.markdown(
                            f"**📄 {source['source']} — "
                            f"Page {source['page']}**"
                        )

                        st.write(
                            source["text"][:500] + "..."
                        )

                        st.divider()


# CHAT INPUT

question = st.chat_input(
    "✨ Ask anything about your notes..."
)


# PROCESS QUESTION

if question:

    # Check index

    if "store" not in st.session_state:

        st.warning(
            "🌸 Please upload a PDF and click "
            "**Build Knowledge Index** first."
        )

    else:

        # Save user question

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )


        # Search + Answer

        with st.spinner(
            "🌷 StudyBloom AI is thinking..."
        ):

            hits = st.session_state.store.search(
                question,
                k=k
            )

            try:

                reply = answer(
                    question,
                    hits
                )

            except Exception as e:

                reply = (
                    f"LLM error: {e}. "
                    "Please check your .env configuration."
                )


        # Save AI answer

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply,
                "sources": hits
            }
        )


        # Refresh

        st.rerun()


# FOOTER

st.divider()

st.caption(
    "🌸 StudyBloom AI • Your personal AI study companion"
)