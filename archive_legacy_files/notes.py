"""
Notes page — rich text notes, save/download in multiple formats
"""
import streamlit as st
import json
from datetime import datetime
from db.database import save_note, get_notes, update_note, delete_note, add_badge
from utils.styles import inject_css

def show_notes():
    inject_css()
    uid = st.session_state.user["id"]

    st.markdown("""
    <h1>📝 Notes</h1>
    <p style="color:#94a3b8">Write, save, and download your study notes in any format.</p>
    """, unsafe_allow_html=True)

    # Init state
    if "note_title" not in st.session_state:
        st.session_state.note_title = ""
    if "note_content" not in st.session_state:
        st.session_state.note_content = ""
    if "editing_note_id" not in st.session_state:
        st.session_state.editing_note_id = None

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### ✍️ Write Note")
        title = st.text_input("Note Title", value=st.session_state.note_title, placeholder="e.g. Binary Search Pattern")
        content = st.text_area(
            "Content",
            value=st.session_state.note_content,
            height=350,
            placeholder="Write your notes here...\n\nSupports markdown!\n\n# Heading\n- Bullet point\n**Bold** and *italic*\n```python\ncode blocks\n```"
        )

        col_s, col_c = st.columns(2)
        with col_s:
            if st.button("💾 Save Note", use_container_width=True):
                if not title.strip():
                    st.error("Title is required.")
                elif not content.strip():
                    st.error("Content is required.")
                else:
                    if st.session_state.editing_note_id:
                        update_note(st.session_state.editing_note_id, title, content)
                        st.success("Note updated!")
                        st.session_state.editing_note_id = None
                    else:
                        save_note(uid, title, content)
                        st.success("Note saved!")
                        add_badge(uid, "note_taker")
                    st.session_state.note_title = ""
                    st.session_state.note_content = ""
                    st.rerun()
        with col_c:
            if st.button("🆕 New Note", use_container_width=True):
                st.session_state.note_title = ""
                st.session_state.note_content = ""
                st.session_state.editing_note_id = None
                st.rerun()

        if content.strip():
            st.markdown("---")
            st.markdown("### 👁️ Preview")
            st.markdown(content)

    with col2:
        st.markdown("### 📚 Saved Notes")
        notes = get_notes(uid)

        if not notes:
            st.info("No notes yet. Write your first note!")
        else:
            for note in notes:
                with st.expander(f"📄 {note['title'][:35]}{'…' if len(note['title'])>35 else ''}", expanded=False):
                    st.markdown(f'<span style="color:#64748b; font-size:0.75rem;">Updated: {note["updated_at"][:10]}</span>', unsafe_allow_html=True)
                    st.markdown(note["content"][:300] + ("…" if len(note["content"]) > 300 else ""))

                    # Actions
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if st.button("✏️ Edit", key=f"edit_{note['id']}"):
                            st.session_state.note_title = note["title"]
                            st.session_state.note_content = note["content"]
                            st.session_state.editing_note_id = note["id"]
                            st.rerun()
                    with col_b:
                        if st.button("🗑️ Delete", key=f"del_{note['id']}"):
                            delete_note(note["id"])
                            st.rerun()
                    with col_c:
                        fmt = st.selectbox("Format", ["txt", "md", "json"], key=f"fmt_{note['id']}", label_visibility="collapsed")

                    # Download
                    if fmt == "txt":
                        dl_data = f"{note['title']}\n{'='*len(note['title'])}\n\n{note['content']}"
                        mime = "text/plain"
                        ext = "txt"
                    elif fmt == "md":
                        dl_data = f"# {note['title']}\n\n{note['content']}"
                        mime = "text/markdown"
                        ext = "md"
                    else:
                        dl_data = json.dumps({"title": note["title"], "content": note["content"], "created": note["created_at"]}, indent=2)
                        mime = "application/json"
                        ext = "json"

                    st.download_button(
                        "⬇️ Download",
                        data=dl_data,
                        file_name=f"{note['title'][:30].replace(' ','_')}.{ext}",
                        mime=mime,
                        key=f"dl_{note['id']}_{ext}",
                        use_container_width=True,
                    )

    # Bulk export
    st.markdown("---")
    st.markdown("### 📤 Export All Notes")
    notes_all = get_notes(uid)
    if notes_all:
        all_json = json.dumps([
            {"title": n["title"], "content": n["content"], "created": n["created_at"]}
            for n in notes_all
        ], indent=2)
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.download_button(
                "⬇️ Export All as JSON",
                data=all_json,
                file_name=f"faang_notes_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True,
            )
        with col_e2:
            all_md = "\n\n---\n\n".join(f"# {n['title']}\n\n{n['content']}" for n in notes_all)
            st.download_button(
                "⬇️ Export All as Markdown",
                data=all_md,
                file_name=f"faang_notes_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
