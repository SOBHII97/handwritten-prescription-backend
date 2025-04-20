# 🧾 Handwritten Prescription Backend 🩺

> Flask-based backend API for extracting medical data from handwritten prescriptions using OCR + NLP.

---

## 🚀 Features

- ✍️ Handwriting recognition using TrOCR
- 🔍 Text segmentation using YOLOv9
- 💊 Drug & dosage extraction using med7 (spaCy)
- 🔐 User login / registration with JWT
- 📦 Clean, production-ready Flask structure

---

## 📂 Project Structure


---

## 📬 API Endpoints

| Method | Endpoint                        | Description                             |
|--------|----------------------------------|-----------------------------------------|
| POST   | `/api/auth/register`            | Register new user                       |
| POST   | `/api/auth/login`               | Login & receive JWT token               |
| POST   | `/api/ai/process_text`          | Extract drugs & dosage from text        |
| POST   | `/api/ai/segmentation`          | Return image with detected text boxes   |
| POST   | `/api/ai/extract_text`          | Extract text + image with boxes         |

---

## 🧠 Models Used

- **TrOCR** (Handwritten text recognition)  
- **YOLOv9** (Text line segmentation)  
- **med7 (spaCy)** (Medical NER extraction)

> ⚠️ Models like `en_core_med7_lg`, `.pt` weights are ignored from GitHub (not uploaded)

---

## ⚙️ Setup Instructions

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install packages
pip install -r requirements.txt  # (You’ll need to re-add this locally)
Authorization: Bearer <your_token_here>


# 3. Install med7 model manually
pip install app/models/en_core_med7_lg-any-py3-none-any.whl

# 4. Run the backend
python main.py
