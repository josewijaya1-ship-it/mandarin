import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Tutor Indo-Taiwan", page_icon="🇹🇼", layout="wide")

# --- KONFIGURASI API ---
try:
    # Membaca API Key dari .streamlit/secrets.toml
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key belum terpasang di Secrets!")
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
        # Meminta Gemini membuat judul singkat berdasarkan input pertama
        prompt_judul = f"Buat judul chat sangat singkat (max 3 kata) tentang: {user_input}"
        response = model.generate_content(prompt_judul)
        return response.text.strip()
    except:
        return "Percakapan Baru"

# --- SIDEBAR: DAFTAR RIWAYAT ---
with st.sidebar:
    st.title("🇹🇼 Riwayat Belajar")
    st.caption("Fokus: Indonesia & Taiwan (Traditional Chinese)")
    
    if st.button("+ Chat Baru", use_container_width=True):
        st.session_state.current_chat_id = None
        st.rerun()

    st.write("---")
    # Menampilkan daftar judul chat yang pernah dibuat
    for chat_id in st.session_state.all_chats.keys():
        if st.button(f"📄 {chat_id}", key=chat_id, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# --- TAMPILAN UTAMA ---
st.title("🎓 Guru Bahasa Indo-Taiwan")
st.markdown("Spesialis penerjemah dan penjelasan tata bahasa **Indonesia** dan **Mandarin Taiwan (Traditional Chinese)**.")

if st.session_state.current_chat_id:
    # Tampilkan pesan dari chat yang sedang aktif
    messages = st.session_state.all_chats[st.session_state.current_chat_id]
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
else:
    st.info("Halo! Ketik kalimat yang mau kamu pelajari atau terjemahkan di bawah ini.")

# --- INPUT USER & LOGIKA AI ---
if prompt := st.chat_input("Tanya guru (contoh: 'Apa kabar dalam bahasa Taiwan?')..."):
    
    # 1. Jika ini chat baru, buatkan judul otomatis
    if st.session_state.current_chat_id is None:
        new_title = generate_chat_title(prompt)
        if new_title in st.session_state.all_chats:
            new_title = f"{new_title} ({len(st.session_state.all_chats)})"
        
        st.session_state.all_chats[new_title] = []
        st.session_state.current_chat_id = new_title

    # 2. Simpan pesan user
    st.session_state.all_chats[st.session_state.current_chat_id].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Respon Guru AI
    with st.chat_message("assistant"):
        with st.spinner("Guru sedang menulis..."):
            try:
                # Instruksi sistem agar fokus ke Indonesia dan Taiwan
                instruction = (
                    "Kamu adalah Guru Bahasa yang ahli dalam Bahasa Indonesia dan Bahasa Mandarin (khusus penggunaan di Taiwan). "
                    "Gunakan aksara Traditional Chinese (Zhongwen) untuk tulisan Mandarinnya. "
                    "Berikan terjemahan yang natural, jelaskan cara bacanya (Pinyin atau Zhuyin jika perlu), "
                    "dan berikan penjelasan konteks sosial atau budaya di Taiwan. "
                    "Gunakan nada bicara yang sopan dan mendidik."
                )
                
                # Mengirim chat history ke Gemini
                history_data = st.session_state.all_chats[st.session_state.current_chat_id]
                response = model.generate_content(f"{instruction}\n\nPercakapan:\n{history_data}\n\nUser: {prompt}")
                
                answer = response.text
                st.markdown(answer)
                
                # Simpan jawaban AI ke history
                st.session_state.all_chats[st.session_state.current_chat_id].append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Gagal memproses permintaan: {e}")
    
    st.rerun()
