# 🧾 Invoice Data Extractor

A Streamlit web app that extracts structured invoice data from images or raw text using Google Gemini LLM via LangChain. Supports parsing buyer details, itemized billing, tax calculations, and visualizing tax per item.

---

## 📌 Features

- 🔍 Extracts invoice data from uploaded images or pasted text
- 🧠 Uses Google Gemini LLM via LangChain with few-shot prompting
- 📊 Displays itemized results including quantity, tax, and total
- 📈 Visualizes tax per item with a clean bar chart
- ⚙️ Pydantic model-based output parsing for reliable data extraction
- 🖼️ Supports JPEG, PNG invoice formats

---

## 🛠️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/invoice-data-extractor.git
cd invoice-data-extractor
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file and add your API key:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## ▶️ Usage

Run the app locally:

```bash
streamlit run app.py
```

Once launched, you can:
- Upload an invoice image
- Or paste invoice text manually
- View extracted data and tax breakdowns

---

## 📂 Project Structure

```
.
├── app.py                  # Main Streamlit application
├── invoice_utils.py        # Core OCR and parsing functions
├── requirements.txt
└── README.md
```

---

## 📦 Dependencies

- streamlit
- langchain
- pydantic
- matplotlib
- python-dotenv
- Pillow

---

## 📜 License

This project is licensed under the MIT License.  
See [`LICENSE`](LICENSE) for more information.

---

## 🙌 Acknowledgments

- [Google Gemini](https://deepmind.google/technologies/gemini/)
- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)

---

## 📬 Contact

For questions, suggestions, or collaborations:  
**Your Name** – [your.email@example.com](mailto:marawan.abdellah0@gmail.com)  
GitHub: [@yourusername](https://github.com/MarwanAbedllah)
