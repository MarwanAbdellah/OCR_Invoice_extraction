import streamlit as st
import os
from invoice_utils import process_invoice, format_invoice_data, plot_tax_per_item

st.set_page_config(page_title="Invoice Extractor", layout="centered")

# 🧾 App Title
st.markdown("<h1 style='text-align:center;'>📑 Invoice Data Extractor</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# 🎛️ Input Mode Selector
st.markdown("### 🛠️ Select Input Method")
input_mode = st.radio("Select input type:", ["Upload Image", "Enter Text Manually"], label_visibility="collapsed")

def handle_invoice_processing(image_path=None, invoice_text=None):
    try:
        with st.spinner("⏳ Extracting data from invoice..."):
            output = process_invoice(image_path=image_path, invoice_text=invoice_text)
            formatted = format_invoice_data(output)

        with st.expander("📄 Extracted Invoice Data", expanded=True):
            if isinstance(formatted, dict):
                st.json(formatted)
            else:
                st.text(formatted)

        try:
            fig = plot_tax_per_item(formatted)
            with st.expander("📊 Tax per Item Chart", expanded=True):
                st.pyplot(fig)
        except Exception as e:
            st.warning(f"⚠️ Could not generate tax chart: {e}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

# 📤 Upload Image Input
if input_mode == "Upload Image":
    uploaded_file = st.file_uploader("Choose an invoice image...", type=["jpg", "jpeg", "png"])

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("📤 Submit", use_container_width=True)

    if uploaded_file and submit:
        temp_folder = "temp"
        os.makedirs(temp_folder, exist_ok=True)
        temp_file_path = os.path.join(temp_folder, uploaded_file.name)

        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(uploaded_file, caption="🖼️ Uploaded Image", use_container_width=True)
        handle_invoice_processing(image_path=temp_file_path)

        os.remove(temp_file_path)

# 📝 Manual Text Input
elif input_mode == "Enter Text Manually":
    manual_text = st.text_area("Paste invoice text here:", height=200)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("📤 Submit", use_container_width=True)

    if manual_text.strip() and submit:
        handle_invoice_processing(invoice_text=manual_text)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:13px; color:gray;'>Made with ❤️ using LangChain & Streamlit</p>", unsafe_allow_html=True)
