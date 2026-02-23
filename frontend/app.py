import streamlit as st
import requests

BACKEND_BASE_URL = "http://127.0.0.1:8001"

st.set_page_config(page_title="APA 7 - Next Gen AI", page_icon="🧬", layout="wide")

st.title("🧬 Next-Generation APA 7 Bibliography Assistant")
st.markdown(
    """
This tool helps you generate **APA 7** references and **BibTeX** from:

- Your local PDF files
- arXiv search results
- OpenAI GPT models

You get:
- A ready-to-use **Word (.docx)** bibliography
- A **BibTeX (.bib)** file for Zotero, Mendeley, LaTeX, etc.
"""
)

# --- SIDEBAR: MODEL & arXiv SETTINGS ---
with st.sidebar:
    st.header("🧠 Model & arXiv Settings")

    selected_model = st.selectbox(
        "Select OpenAI model:",
        options=[
            "gpt-4.1",
            "gpt-4o",
            "gpt-4o-mini",
            "gpt-4.1-mini",
        ],
        index=2,
        help="Choose a model depending on quality vs. speed/cost trade-offs.",
    )

    st.divider()

    st.subheader("🔎 arXiv Integration")
    arxiv_query = st.text_input(
        "arXiv search query (optional):",
        help="Example: 'photobiomodulation Alzheimer's', 'UV irradiation mushrooms vitamin D2', etc.",
    )
    arxiv_max_results = st.number_input(
        "Max arXiv results to include:",
        min_value=0,
        max_value=50,
        value=0,
        step=1,
        help="Set >0 to automatically fetch and include arXiv papers in the citation corpus.",
    )

    st.divider()
    st.success(f"Selected model: **{selected_model}**")
    if arxiv_query and arxiv_max_results > 0:
        st.info("arXiv search is enabled and will be added to your corpus.")
    else:
        st.info("arXiv search is currently disabled (no query or max results = 0).")

# --- MAIN AREA ---
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_files = st.file_uploader(
        "📂 Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDFs (articles, preprints, reports, etc.).",
    )

with col2:
    st.write("### ⚙️ Processing Panel")
    if uploaded_files:
        st.success(f"{len(uploaded_files)} file(s) ready.")
        process_btn = st.button("Prepare Bibliography (APA + BibTeX) ⚡", type="primary", use_container_width=True)
    else:
        st.info("Waiting for PDF files...")
        process_btn = False

# Session state to hold generated files
if "apa_bytes" not in st.session_state:
    st.session_state["apa_bytes"] = None
if "bib_bytes" not in st.session_state:
    st.session_state["bib_bytes"] = None

if process_btn and uploaded_files:
    with st.spinner(f"🚀 Preparing bibliography with model {selected_model}..."):
        try:
            files_payload = [
                ("files", (file.name, file.getvalue(), "application/pdf"))
                for file in uploaded_files
            ]

            data_payload = {
                "model_id": selected_model,
                "arxiv_query": arxiv_query,
                "arxiv_max_results": int(arxiv_max_results),
            }

            # 1. Call prepare endpoint
            prepare_url = f"{BACKEND_BASE_URL}/prepare-bibliography/"
            resp = requests.post(
                prepare_url,
                files=files_payload,
                data=data_payload,
                timeout=600,
            )

            if resp.status_code != 200:
                st.error(f"⚠️ Error from backend: {resp.status_code}")
                try:
                    st.json(resp.json())
                except Exception:
                    st.write(resp.text)
            else:
                data = resp.json()
                session_id = data.get("session_id")
                if not session_id:
                    st.error("No session_id returned from backend.")
                else:
                    # 2. Download APA
                    apa_url = f"{BACKEND_BASE_URL}/download/apa/{session_id}"
                    apa_resp = requests.get(apa_url, timeout=300)
                    if apa_resp.status_code == 200:
                        st.session_state["apa_bytes"] = apa_resp.content
                    else:
                        st.error("Failed to download APA Word file.")

                    # 3. Download BibTeX
                    bib_url = f"{BACKEND_BASE_URL}/download/bibtex/{session_id}"
                    bib_resp = requests.get(bib_url, timeout=300)
                    if bib_resp.status_code == 200:
                        st.session_state["bib_bytes"] = bib_resp.content
                    else:
                        st.error("Failed to download BibTeX file.")

                    if st.session_state["apa_bytes"] and st.session_state["bib_bytes"]:
                        st.balloons()
                        st.success("✅ Bibliography prepared successfully! You can now download APA + BibTeX.")

        except requests.exceptions.ConnectionError:
            st.error("🚨 Cannot reach backend! Is 'main.py' running in the terminal?")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

st.markdown("---")
st.subheader("📥 Downloads")

col_apa, col_bib = st.columns(2)

with col_apa:
    if st.session_state["apa_bytes"]:
        st.download_button(
            label="📥 Download APA 7 Word file",
            data=st.session_state["apa_bytes"],
            file_name="references_apa7.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True,
        )
    else:
        st.info("APA 7 Word file not available yet.")

with col_bib:
    if st.session_state["bib_bytes"]:
        st.download_button(
            label="📥 Download BibTeX (.bib)",
            data=st.session_state["bib_bytes"],
            file_name="references.bib",
            mime="application/x-bibtex",
            use_container_width=True,
        )
    else:
        st.info("BibTeX file not available yet.")
