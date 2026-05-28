<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=30&pause=1000&color=4A90D9&center=true&vCenter=true&width=700&lines=PrepLP+%F0%9F%8E%93+%E2%80%94+Smart+Exam+Prep+Platform;NLP-Powered+Study+Assistant+%F0%9F%A4%96;Chatbot+%7C+Trends+%7C+Study+Materials+%F0%9F%93%9A;Built+with+Django+%2B+Python+%2B+NLP+%F0%9F%90%8D" alt="Typing SVG" />

<br/>

# 🎓 PrepLP — AI-Powered Placement & Exam Preparation Platform

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Web_App-4A90D9?style=for-the-badge&logo=google-chrome&logoColor=white" />
  <img src="https://img.shields.io/badge/Backend-Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/AI-NLP_Powered-FF6B6B?style=for-the-badge&logo=openai&logoColor=white" />
  <img src="https://img.shields.io/badge/Cloud-Backblaze_B2-E87722?style=for-the-badge&logo=backblaze&logoColor=white" />
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-62%25-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/HTML-37%25-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
</p>

<br/>

> **PrepLP** is a **Natural Language Processing–powered exam preparation platform** that gives students a single integrated space to store study materials, analyze question trends & patterns, interact with an AI chatbot, and submit feedback — all in one place.

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Coming_Soon-lightgrey?style=for-the-badge)](https://github.com/dewanshikarnawat/PrepLP-)
[![View Code](https://img.shields.io/badge/📂_View_Code-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/dewanshikarnawat/PrepLP-)

</div>

---

## 📌 Table of Contents

- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [My Contributions](#-my-contributions--improvements)
- [Getting Started](#-getting-started)
- [Future Roadmap](#-future-roadmap)
- [Connect](#-connect-with-me)

---

## 🚩 Problem Statement

Students preparing for placements and exams often face:

- 📦 **Scattered resources** — notes spread across drives, messages, and websites
- 🔍 **No pattern analysis** — unable to identify important/recurring topics
- 🤖 **No AI assistance** — no personalised guidance during self-study
- 💬 **No feedback loop** — no mechanism to track what's working or not

**PrepLP** solves all of this with a unified, intelligent platform.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 📂 **Study Material Hub** | Centralized repository to store, access & navigate all learning resources |
| 📊 **Trends & Patterns** | NLP-based analysis of question patterns and high-frequency exam topics |
| 🤖 **AI Chatbot** | Conversational assistant for doubt resolution and study guidance |
| 💬 **Feedback System** | Students can submit feedback to improve their learning experience |
| ☁️ **Cloud Storage** | Study files stored securely on Backblaze B2 (S3-compatible cloud) |
| 🔐 **User Accounts** | Authentication system for personalized, role-based access |

---

## 🛠️ Tech Stack

<div align="center">

### Frontend
<img src="https://skillicons.dev/icons?i=html,css,js" />

### Backend & AI
<img src="https://skillicons.dev/icons?i=python,django" />

| Component | Technology |
|---|---|
| NLP Engine | Python (NLTK / spaCy-based processing) |
| Chatbot | NLP-powered conversational model |
| Trends Analysis | Text pattern mining & frequency analysis |

### Storage & Database
<img src="https://skillicons.dev/icons?i=sqlite" />

| Layer | Technology |
|---|---|
| Primary DB | SQLite |
| Cloud File Storage | Backblaze B2 (S3-compatible API via `boto3`) |
| File Metadata | JSON-based auth & data management |

</div>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        STUDENT                          │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │    Django Web Server    │
         │  (Views + URL Routing)  │
         └──┬──────┬────────┬─────┘
            │      │        │
    ┌────────▼──┐ ┌─▼──────┐ ┌▼────────────┐
    │  NLP Core │ │  Auth   │ │  File/Notes │
    │ (Chatbot, │ │ Module  │ │   Manager   │
    │  Trends)  │ │accounts │ │  (B2 Cloud) │
    └────────┬──┘ └─┬──────┘ └┬────────────┘
             │      │         │
         ┌───▼──────▼─────────▼───┐
         │       SQLite DB         │
         │  + Backblaze B2 Storage │
         └─────────────────────────┘
```

---

## 📁 Project Structure

```
PrepLP-/
│
├── 📂 accounts/           # User authentication & session management
├── 📂 Notes/              # Notes module — upload, view, manage study notes
├── 📂 ProgramPage/        # Program/course listing pages
├── 📂 StudentMaterial/    # Core study material storage & retrieval
├── 📂 mahipal/            # Core Django app (main logic, chatbot, NLP)
├── 📂 templates/          # HTML templates (Jinja2 / Django templates)
│
├── 📄 manage.py           # Django project entry point
├── 📄 requirements.txt    # Python dependencies
├── 📄 db.sqlite3          # SQLite database
├── 📄 data.json           # Raw dataset
├── 📄 data_clean.json     # Cleaned/processed dataset
├── 📄 auth_meta.json      # Auth metadata config
├── 📄 users.json          # User data
├── 📄 test_b2.py          # Backblaze B2 cloud storage integration test
├── 📄 package.json        # Node dependencies (frontend tooling)
└── 📄 .env                # Environment variables (not committed)
```

---

## 🙋 My Contributions & Improvements

> This is a **forked and extended** project. Below are the meaningful engineering improvements I implemented:

### ☁️ Cloud Storage Module — Refactored & Enhanced

**File:** `test_b2.py` — Backblaze B2 (S3-compatible) upload module

#### Before vs After

| Aspect | Before (Original) | After (My Implementation) |
|---|---|---|
| **File Handling** | Uploaded a single hardcoded file (`boto3-test.txt`) | Dynamic input — any file can be uploaded at runtime |
| **File Naming** | Fixed filename — overwrote existing files | UUID-based unique naming prevents all overwrites |
| **Code Design** | Flat, non-reusable script | Encapsulated `upload_text_file()` function — reusable anywhere |
| **Error Handling** | None — silent failures | `try-except` block with descriptive error messages |
| **Scalability** | Single-use script | Modular — integrates cleanly with Django views |

#### Key Code Improvement

```python
# BEFORE — hardcoded, fragile
s3.upload_file("boto3-test.txt", BUCKET_NAME, "boto3-test.txt")

# AFTER — dynamic, reusable, production-ready
import uuid

def upload_text_file(content: str, bucket_name: str) -> str:
    """Upload dynamic content to B2 with a unique filename. Returns the file key."""
    try:
        unique_key = f"uploads/{uuid.uuid4()}.txt"
        s3.put_object(Bucket=bucket_name, Key=unique_key, Body=content)
        return unique_key
    except Exception as e:
        print(f"Upload failed: {e}")
        raise
```

**Impact:** Enables safe, collision-free file uploads — critical for a multi-user platform where many students upload study files simultaneously.

---

## 🚀 Getting Started

### Prerequisites

```bash
Python 3.8+
pip
Node.js (for frontend tooling)
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/dewanshikarnawat/PrepLP-.git
cd PrepLP-

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Node dependencies
npm install

# 5. Configure environment variables
cp .env.example .env
# Edit .env with your Backblaze B2 credentials and Django SECRET_KEY

# 6. Run database migrations
python manage.py migrate

# 7. Start the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

### Environment Variables (`.env`)

```env
SECRET_KEY=your_django_secret_key
B2_KEY_ID=your_backblaze_key_id
B2_APPLICATION_KEY=your_backblaze_app_key
B2_BUCKET_NAME=your_bucket_name
DEBUG=True
```

---

## 🔭 Future Roadmap

- [ ] 🔐 Full user authentication with role-based access (Student / Admin)
- [ ] 🤖 Advanced RAG (Retrieval-Augmented Generation) for smarter chatbot responses
- [ ] 📈 Personalized dashboard with study progress tracker
- [ ] 📎 Drag-and-drop file upload & sharing between students
- [ ] 🔔 Notification system for new materials & upcoming exam reminders
- [ ] 📱 Mobile-responsive UI redesign

---

## 🛠️ Tools & Technologies

<p align="left">
  <img src="https://skillicons.dev/icons?i=python,django,html,css,js,sqlite,git,github,vscode" />
</p>

---

## 👩‍💻 Connect with Me

<p align="left">
  <a href="https://github.com/dewanshikarnawat">
    <img src="https://img.shields.io/badge/GitHub-dewanshikarnawat-181717?style=for-the-badge&logo=github&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://www.linkedin.com/in/dewanshi-karnawat-388578353/">
    <img src="https://img.shields.io/badge/LinkedIn-dewanshikarnawat-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://www.geeksforgeeks.org/user/dewanshikarnawat/">
    <img src="https://img.shields.io/badge/GeeksForGeeks-Profile-2F8D46?style=for-the-badge&logo=geeksforgeeks&logoColor=white" />
  </a>
</p>

---

<div align="center">

**If you find this project useful or interesting, please ⭐ Star the repo — it means a lot!**

<br/>

<img src="https://komarev.com/ghpvc/?username=dewanshikarnawat&label=Profile+Views&color=4A90D9&style=flat" alt="Profile Views" />

<br/><br/>

*Built with 💙 using Django, Python & NLP*

</div>
