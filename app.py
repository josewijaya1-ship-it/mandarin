# 3. Respon Guru AI
    with st.chat_message("assistant"):
        with st.spinner("Guru sedang menulis..."):
            try:
                # --- GUARDRAIL & INSTRUKSI KETAT ---
                instruction = (
                    "TUGAS UTAMA: Kamu ADALAH Guru Bahasa spesialis Bahasa Indonesia dan Mandarin Taiwan (Traditional Chinese). "
                    "BATASAN KETAT: Kamu HANYA boleh menjawab pertanyaan tentang terjemahan, tata bahasa, atau budaya yang berkaitan dengan Bahasa Indonesia dan Mandarin Taiwan. "
                    "Jika user meminta menerjemahkan ke bahasa lain (seperti Inggris, Jepang, Korea, Arab, dll), "
                    "atau bertanya di luar topik bahasa/budaya Indo-Taiwan, jawablah dengan sopan: "
                    "'Maaf, saya adalah spesialis Bahasa Indonesia dan Mandarin Taiwan. Saya tidak dapat melayani permintaan di luar bidang tersebut.'"
                    "\n\nFORMAT JAWABAN:"
                    "1. Gunakan Traditional Chinese (bukan Simplified)."
                    "2. Sertakan Pinyin dan cara baca yang natural di Taiwan."
                    "3. Berikan konteks budaya jika relevan."
                )
                
                # Mengirim chat history ke Gemini
                history_data = st.session_state.all_chats[st.session_state.current_chat_id]
                
                # Gabungkan instruksi dengan history agar AI tetap ingat batasannya
                full_prompt = f"System Instruction: {instruction}\n\nChat History: {history_data}\n\nUser Question: {prompt}"
                
                response = model.generate_content(full_prompt)
                
                answer = response.text
                st.markdown(answer)
                
                # Simpan jawaban AI ke history
                st.session_state.all_chats[st.session_state.current_chat_id].append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Gagal memproses permintaan: {e}")
