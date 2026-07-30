import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Multimodal RAG Platform — Education", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "current_room" not in st.session_state:
    st.session_state.current_room = None


def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def login_page():
    st.title("Multimodal RAG Platform — Education")
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            resp = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
            if resp.status_code == 200:
                st.session_state.token = resp.json()["access_token"]
                st.session_state.page = "rooms"
                st.rerun()
            else:
                st.error(resp.json().get("detail", "Login failed"))

    with tab_register:
        username = st.text_input("Username", key="reg_username")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Register"):
            resp = requests.post(
                f"{API_URL}/auth/register",
                json={"username": username, "email": reg_email, "password": reg_password},
            )
            if resp.status_code == 201:
                st.success("Registered! Please log in.")
            else:
                st.error(resp.json().get("detail", "Registration failed"))


def room_list_page():
    st.title("Your Chat Rooms")

    if st.button("Logout"):
        st.session_state.token = None
        st.session_state.page = "login"
        st.rerun()

    with st.form("create_room"):
        st.subheader("Create a new room")
        name = st.text_input("Room name")
        description = st.text_input("Description")
        submitted = st.form_submit_button("Create Room")
        if submitted and name:
            resp = requests.post(
                f"{API_URL}/rooms",
                json={"name": name, "description": description},
                headers=auth_headers(),
            )
            if resp.status_code == 201:
                st.success("Room created!")
                st.rerun()
            else:
                st.error("Could not create room")

    st.subheader("Existing rooms")
    resp = requests.get(f"{API_URL}/rooms", headers=auth_headers())
    if resp.status_code == 200:
        rooms = resp.json()
        if not rooms:
            st.info("No rooms yet. Create one above.")
        for room in rooms:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{room['name']}** — {room.get('description') or 'No description'}")
            with col2:
                if st.button("Enter", key=f"enter_{room['id']}"):
                    st.session_state.current_room = room
                    st.session_state.page = "room_view"
                    st.rerun()
    else:
        st.error("Could not load rooms")


def room_view_page():
    room = st.session_state.current_room
    st.title(f"Room: {room['name']}")

    if st.button("← Back to rooms"):
        st.session_state.page = "rooms"
        st.session_state.current_room = None
        st.rerun()

    sidebar_col, chat_col = st.columns([1, 2])

    with sidebar_col:
        st.subheader("Upload a file")
        uploaded = st.file_uploader(
            "Choose a file",
            type=["pdf", "docx", "csv", "md", "txt", "pptx", "png", "jpg", "jpeg", "mp3", "wav", "m4a", "mp4", "mov"],
        )
        if uploaded is not None:
            if st.button("Upload"):
                files = {"file": (uploaded.name, uploaded.getvalue())}
                with st.spinner("Processing file... this can take a while for audio/video."):
                    resp = requests.post(
                        f"{API_URL}/upload/{room['id']}", files=files, headers=auth_headers()
                    )
                if resp.status_code == 200:
                    data = resp.json()
                    st.success(f"✅ {uploaded.name} — {data['chunks_created']} chunks — status: {data['status']}")
                else:
                    st.error(f"❌ Upload failed: {resp.json().get('detail', 'Unknown error')}")

    with chat_col:
        st.subheader("Chat")

        history_resp = requests.get(f"{API_URL}/chat/{room['id']}/history", headers=auth_headers())
        if history_resp.status_code == 200:
            messages = history_resp.json()
            for msg in messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
                    if msg["role"] == "assistant":
                        sources = msg.get("sources") or []
                        with st.expander(f"Sources ({len(sources)})"):
                            if not sources:
                                st.write("No sources found")
                            else:
                                for src in sources:
                                    st.markdown(
                                        f"**{src['filename']}** ({src['file_type']}, chunk {src['chunk_index']})"
                                    )
                                    st.caption(src["excerpt"])

        query = st.chat_input("Ask a question about your uploaded files...")
        if query:
            with st.spinner("Thinking..."):
                resp = requests.post(
                    f"{API_URL}/chat/{room['id']}", json={"query": query}, headers=auth_headers()
                )
            if resp.status_code == 200:
                st.rerun()
            else:
                st.error("Failed to get a response")


if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "rooms":
    room_list_page()
elif st.session_state.page == "room_view":
    room_view_page()