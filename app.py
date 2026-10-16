from io import BytesIO

import streamlit as st

from classifier import classify_document


st.set_page_config(
    page_title="Lexi | Legal document classifier",
    page_icon="📄",
    layout="centered",
)

with st.sidebar:
    st.markdown("### :material/gavel: Lexi")
    st.caption("Legal document classifier")
    st.divider()
    st.markdown("**How it works**")
    st.caption("A transparent, rule-based scan looks for phrases commonly found in legal documents.")
    st.markdown("**Privacy**")
    st.caption("No AI service or API key is used. When hosted, text is processed by the Streamlit app server.")
    st.divider()
    st.caption("For general information only. Not legal advice.")

st.markdown(":material/verified_user:  **LEXI  /  DOCUMENT INTELLIGENCE**")
st.title("Know what you're looking at.")
st.write(
    "Classify a legal document in seconds. Lexi scans for common signals and shows you exactly "
    "which phrases informed its result."
)

intro_left, intro_right = st.columns(2)
with intro_left:
    with st.container(border=True, height="stretch"):
        st.markdown(":material/search: **Clear classification**")
        st.caption("Identify common document types, from contracts to court filings.")
with intro_right:
    with st.container(border=True, height="stretch"):
        st.markdown(":material/visibility: **See the clues**")
        st.caption("Review matched phrases and alternative categories. No mystery score.")

st.subheader("Analyze a document")
source = st.segmented_control(
    "Choose how to add your document",
    ["Paste text", "Upload a text file"],
    default="Paste text",
    key="source_mode",
    width="stretch",
    wrap=True,
)

document_text = ""
if source == "Upload a text file":
    uploaded = st.file_uploader("Choose a plain text file", type=["txt", "md"])
    if uploaded is not None:
        try:
            document_text = uploaded.getvalue().decode("utf-8-sig")
            st.caption(f"Ready to analyze: {uploaded.name}")
        except UnicodeDecodeError:
            st.error("This file could not be read as UTF-8. Save it as a UTF-8 .txt file and try again.")
else:
    document_text = st.text_area(
        "Document text",
        placeholder="Paste a clause, letter, agreement, or other legal text here...",
        height=230,
        key="document_text_input",
    )

if st.button("Classify document", type="primary", icon=":material/arrow_forward:", width="stretch"):
    if not document_text.strip():
        st.warning("Add some text before classifying.", icon=":material/info:")
    else:
        st.session_state["classification_result"] = classify_document(document_text)
        st.session_state["classified_text"] = document_text

result = st.session_state.get("classification_result")
if result:
    st.divider()
    st.subheader("Classification result")
    category_col, strength_col = st.columns([2, 1])
    with category_col:
        with st.container(border=True, height="stretch"):
            st.caption("MOST LIKELY DOCUMENT TYPE")
            st.markdown(f"## :material/description: {result['category']}")
    with strength_col:
        with st.container(border=True, height="stretch"):
            st.caption("MATCH STRENGTH")
            st.markdown(f"## {result['strength']}")

    if result["matches"]:
        st.markdown("#### Phrases we found")
        st.pills("Matched signals", result["matches"], selection_mode="multi", disabled=True)
    else:
        st.info("No strong document-type phrases were found. Try adding more of the document text.")

    if result["alternatives"]:
        st.markdown("#### Other possible matches")
        for option in result["alternatives"]:
            with st.container(border=True):
                st.markdown(f"**{option['category']}**")
                st.caption("Matched: " + ", ".join(option["matches"]))

    with st.expander("How to read this result"):
        st.write(
            "This result comes from a small set of weighted phrase rules. Match strength describes "
            "how many and how distinctive the matching phrases were; it is not a probability or a "
            "legal conclusion. A document can fit more than one category."
        )

    report = (
        f"Document type: {result['category']}\n"
        f"Match strength: {result['strength']}\n"
        f"Matched phrases: {', '.join(result['matches']) or 'None'}\n\n"
        "Original text:\n"
        f"{st.session_state.get('classified_text', '')}\n"
    )
    st.download_button(
        "Download classification report",
        data=BytesIO(report.encode("utf-8")),
        file_name="legal-document-classification.txt",
        mime="text/plain",
        icon=":material/download:",
        width="stretch",
    )

st.divider()
st.caption(
    "Lexi is an informational tool, not a legal service. Its rule-based classification may be incomplete "
    "or incorrect. Do not use it as a substitute for professional review."
)
