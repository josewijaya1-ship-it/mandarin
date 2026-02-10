import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Tutor Indo-Jerman AI", page_icon="🇩🇪", layout="wide")

# --- KONFIGURASI API ---
try:
    # Mengambil API Key dari .streamlit/secrets.toml
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key tidak ditemukan di Secrets! Pastikan konfigurasi sudah benar.")
    st.stop()

model = genai.GenerativeModel("gemini-2.5-flash")

# --- SISTEM PENYIMPANAN SESSION ---
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {} 

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# --- FUNGSI BUAT JUDUL OTOMATIS ---
def generate_chat_title(user_input):
    try:
        prompt_judul = f"Buat judul chat singkat (max 3 kata) tentang bahasa Jerman/Indo: {user_input}"
        response = model.generate_content(prompt_judul)
        return response.text.strip()
    except:
        return "Sesi Deutsch Baru"

# --- SIDEBAR: RIWAYAT CHAT ---
with st.sidebar:
    st.title("🇩🇪 Menu Belajar")
    st.caption("Fokus: Indonesia - Deutsch")
    
    if st.button("+ Chat Baru", use_container_width=True):
        st.session_state.current_chat_id = None
        st.rerun()

    st.write("---")
    st.subheader("Riwayat Percakapan")
    
    for chat_id in st.session_state.all_chats.keys():
        if st.button(f"📖 {chat_id}", key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# --- TAMPILAN UTAMA ---
st.title("🎓 Guru Bahasa Indo-Jerman")
st.markdown("Selamat datang! Saya akan membantu kamu menguasai **Bahasa Jerman** dengan penjelasan yang mudah dimengerti.")

if st.session_state.current_chat_id:
    messages = st.session_state.all_chats[st.session_state.current_chat_id]
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
else:
    st.info("Halo! Coba tanyakan sesuatu, misalnya: 'Bagaimana cara menggunakan der, die, das?'")

# --- LOGIKA INPUT DAN AI ---
if prompt := st.chat_input("Tanya guru di sini..."):
    
    # 1. Judul Otomatis untuk Sesi Baru
    if st.session_state.current_chat_id is None:
        new_title = generate_chat_title(prompt)
        if new_title in st.session_state.all_chats:
            new_title = f"{new_title} ({len(st.session_state.all_chats)})"
        
        st.session_state.all_chats[new_title] = []
        st.session_state.current_chat_id = new_title

    # 2. Simpan Pesan User
    st.session_state.all_chats[st.session_state.current_chat_id].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Respon Guru AI
    with st.chat_message("assistant"):
        with st.spinner("Guru sedang merespons dalam bahasa Jerman..."):
            try:
                # Instruksi khusus untuk spesialis Jerman
                instruction = (
                    "Kamu adalah Guru Bahasa yang ahli dalam Bahasa Indonesia dan Bahasa Jerman (Deutsch). "
                    "Tugasmu: Menerjemahkan kalimat, menjelaskan tata bahasa Jerman yang kompleks "
                    "(seperti konjugasi verba, kasus nominativ/akkusativ/dativ, dan artikel), "
                    "serta memberikan contoh penggunaan dalam percakapan sehari-hari di Jerman. "
                    "Berikan nada bicara yang menyemangati dan profesional."
                )
                
                history_context = st.session_state.all_chats[st.session_state.current_chat_id]
                response = model.generate_content(f"{instruction}\n\nPercakapan:\n{history_context}\n\nSiswa: {prompt}")
                
                answer = response.text
                st.markdown(answer)
                
                st.session_state.all_chats[st.session_state.current_chat_id].append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
    
    st.rerun()
