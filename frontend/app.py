import streamlit as st
import requests

# SETTINGS
BACKEND_URL = "http://127.0.0.1:8001/generate-bibliography/"

st.set_page_config(page_title="APA 7 - Next Gen AI", page_icon="🧬", layout="wide")

st.title("🧬 Next-Generation APA 7 Bibliography Assistant")
st.markdown(
    """
This tool helps you generate **APA 7** references from your PDFs and from **arXiv** papers.

1. Upload your local PDFs (articles, reports, preprints).
2. Optionally specify an **arXiv search query** to automatically include relevant papers.
3. Choose an OpenAI model.
4. Download a ready-to-edit **Word file** with your references.
"""
)

# --- SIDEBAR: MODEL & ARXIV SETTINGS ---
with st.sidebar:
    st.header("🧠 Model & arXiv Settings")

    selected_model = st.selectbox(
        "Select OpenAI model:",
        options=[
            "gpt-4.1",
            "gpt-4o",
            "gpt-4o-mini",   # good default / fallback
            "gpt-4.1-mini",
        ],
        index=2,
        help="Choose a model depending on quality vs. speed/cost trade-offs.",
    )

    st.divider()

    st.subheader("🔎 arXiv Integration")
    arxiv_query = st.text_input(
        "arXiv search query (optional):",
        help="Example: 'large language models for scientific writing' or 'quantum error correction'.",
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
        process_btn = st.button("Generate APA 7 Bibliography ⚡", type="primary", use_container_width=True)
    else:
        st.info("Waiting for PDF files...")
        process_btn = False

if process_btn and uploaded_files:
    with st.spinner(f"🚀 Running model {selected_model} (fallback: gpt-4o-mini)..."):
        try:
            # 1. Prepare files payload
            files_payload = [
                ("files", (file.name, file.getvalue(), "application/pdf"))
                for file in uploaded_files
            ]

            # 2. Prepare form data payload
            data_payload = {
                "model_id": selected_model,
                "arxiv_query": arxiv_query,
                "arxiv_max_results": int(arxiv_max_results),
            }

            # 3. Send request to backend
            response = requests.post(
                BACKEND_URL,
                files=files_payload,
                data=data_payload,
                timeout=300,  # allow more time for arXiv + LLM
            )

            # 4. Handle response
            if response.status_code == 200:
                st.balloons()
                st.success("✅ Bibliography generated successfully!")

                st.download_button(
                    label="📥 Download APA 7 Word file",
                    data=response.content,
                    file_name=f"references_{selected_model}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                )
            else:
                st.error(f"⚠️ Error: {response.status_code}")
                try:
                    st.json(response.json())
                except Exception:
                    st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error("🚨 Cannot reach backend! Is 'main.py' running in the terminal?")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
