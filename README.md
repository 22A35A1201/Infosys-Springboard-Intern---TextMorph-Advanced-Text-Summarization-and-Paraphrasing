
# Project Title
## Infosys_Springboard_TextMorph_Advanced_Text_Summarization_and_Paraphrasing

# 🧠 TextMorph  
### AI-Powered Content Simplification, Summarization & Paraphrasing Suite  
Transforming complex content into clear, concise, and accessible communication.

---

## 🔗 Quick Links

| Category | Link |
|----------|------|
| 📽️ Demo Video | https://drive.google.com/file/d/11BptchXlwkf57GmHGy3VI_m-XZZkZXcp/view |
| 🧩 Source Code | This Repository |
| 🐳 Docker Support | Coming Soon |
| 🧠 AI Models | Pegasus · BART · FLAN-T5 |

---

## 📌 Table of Contents
- About the Project
- Problem Statement & Motivation
- Key Features
- Architecture
- Tech Stack
- Models Used
- Installation & Setup
- Usage Guide
- Admin Controls
- Datasets & Evaluation
- Screenshots
- Team
- License

---

## 📖 About the Project
TextMorph is an advanced AI tool designed to enhance reading accessibility and content quality using NLP, readability science, and transformer-based language models.

It offers:
- Summarization  
- Paraphrasing  
- Readability scoring  
- Admin dashboard  

📌 Built as part of Infosys Springboard Internship Final Project  
📌 Target users: Students, educators, researchers, bloggers, media professionals  

---

## 🎯 Problem Statement & Motivation
Millions of people struggle to understand complex written content. Manual simplification takes time and expertise.

🔹 Our solution uses AI to:
- Improve readability  
- Shorten lengthy content  
- Rewrite content at different complexity levels  
- Help users learn faster  

---

## 🚀 Key Features

### 👤 User Features

| Feature | Description |
|--------|------------|
| 🔐 Secure JWT Authentication | Login, registration, OTP recovery |
| 📊 Readability Analyzer | Flesch, SMOG, Gunning Fog, graphs |
| ✂️ Summarization | Short / Medium / Long |
| 🔁 Paraphrasing | Simple / Neutral / Advanced |
| 👥 Comparison View | Original vs Generated |
| ⭐ Feedback System | Ratings |
| 🕘 History Log | Save & download |
| 🧑 Profile Management | Secure password update |

---

### 🛠 Admin Features 
- User management (add/remove/promote)  
- Usage analytics & reports  
- Feedback monitoring  
- Global search system  
- Full audit logs  
- Lock/Unlock
---

## 🧩 Architecture
Monolithic deployment with secure database and ML model integration  

📌 Architecture Diagram 
<img width="1024" height="1536" alt="ChatGPT Image Mar 23, 2026, 08_14_41 AM" src="https://github.com/user-attachments/assets/73bfb727-8c50-4c1d-98b2-2f9f2fd42e52" />

---

## 🛠 Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | Streamlit |
| Backend | Python |
| NLP Models | Hugging Face Transformers |
| Database | Postgresql |
| Security | JWT, bcrypt |
| Deployment | Docker |

---

## 🤖 Models Used

| Model / Tool | Purpose                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| Pegasus      | Abstractive text summarization (especially long documents, news articles)      |
| BART         | Text summarization, rewriting, and text generation (denoising autoencoder)     |
| FLAN-T5      | Paraphrasing, question answering, translation, and instruction-based NLP tasks |
| NLTK         | Text preprocessing (tokenization, stemming, POS tagging, etc.)                 |
| textstat     | Readability scoring (Flesch Reading Ease, Grade Level, etc.)                   |

---

📝 Usage Guide

 1.Register / Login
<img width="1908" height="890" alt="Screenshot 2026-03-18 154726" src="https://github.com/user-attachments/assets/58ad0227-5abf-4546-8171-70df13e8b02e" />
 2.Input text or upload file
<img width="1909" height="894" alt="Screenshot 2026-03-18 160515" src="https://github.com/user-attachments/assets/8f97831c-51cc-4e8e-a616-104d5ef2738f" />
3.Select feature (summarization/paraphrasing)
<img width="1909" height="886" alt="Screenshot 2026-03-18 160645" src="https://github.com/user-attachments/assets/3fdce1f2-beaf-4e69-85fb-0f3700252e88" />
4.Adjust settings
<img width="1908" height="838" alt="Screenshot 2026-03-18 161226" src="https://github.com/user-attachments/assets/0b625cdb-ccf1-45c3-9d0e-de0d443e37ad" />
5.Generate result
<img width="1896" height="848" alt="Screenshot 2026-03-18 161301" src="https://github.com/user-attachments/assets/81ba33d1-e48e-4abc-a09c-7d0b35f8fcef" />
6.Save & rate output
<img width="1895" height="890" alt="Screenshot 2026-03-18 161328" src="https://github.com/user-attachments/assets/3edb9b6d-1770-45b6-976e-eee1f3e9fb3c" />
7.History
<img width="1905" height="896" alt="Screenshot 2026-03-18 162301" src="https://github.com/user-attachments/assets/d812c2b3-7f2b-4401-8b90-32c2b03a0763" />

📊 Datasets & Evaluation
Used for testing and model improvement:
Dataset
Usage
WikiAuto
Text simplification
Newsela
Grade-level rewriting
ASSET
Paraphrasing benchmark

Evaluation Metrics:
ROUGE-L


BLEU


Readability Delta

1.Login Page
<img width="1917" height="899" alt="Screenshot 2026-03-18 154603" src="https://github.com/user-attachments/assets/ceb99db4-3e6e-463a-86f9-00aa16e59a1c" />
2.Dashboard
<img width="1909" height="894" alt="Screenshot 2026-03-18 160515" src="https://github.com/user-attachments/assets/937cb441-cde5-486e-82f0-90e359bbf76c" />
3.Readability Graph
<img width="1896" height="848" alt="Screenshot 2026-03-18 161301" src="https://github.com/user-attachments/assets/65ed18b3-a7dc-4931-a4db-d184f94e32e1" />
4.Results Page
<img width="1895" height="890" alt="Screenshot 2026-03-18 161328" src="https://github.com/user-attachments/assets/f35b5ba9-0337-4c87-b8da-143b532512b0" />
5.History
<img width="1880" height="891" alt="Screenshot 2026-03-18 164710" src="https://github.com/user-attachments/assets/5bf437c9-aa31-442c-a727-119b6474d5e9" />
6.Admin Dashboard
<img width="1914" height="963" alt="Screenshot 2026-03-20 125927" src="https://github.com/user-attachments/assets/35b3c0a7-3b35-4a90-bf28-234dc4d4c34d" />
<img width="1910" height="624" alt="Screenshot 2026-03-20 125944" src="https://github.com/user-attachments/assets/cfa257a4-dfe1-4021-b5ea-3f35f68e28da" />
<img width="1890" height="673" alt="Screenshot 2026-03-20 125956" src="https://github.com/user-attachments/assets/84638d61-45a5-4105-92ae-f1d652d774b2" />
<img width="1918" height="969" alt="Screenshot 2026-03-20 130014" src="https://github.com/user-attachments/assets/cb57b904-11b3-44a6-bf42-6ace512c983b" />

👥 Team 

| Name              | Role                 | Responsibilities                          |
|-------------------|----------------------|-------------------------------------------|
| 1. Ch. Bhavana    | Project Lead         | Project design, coordination, and deployment, UI/UX |
| 2. K. Akshara       | ML Engineer          | Model tuning, optimization, and evaluation | 
| 3. A. Lavanya       | Backend Developer    | API development and database management    | 
| 4. N. Raja  | Full Stack Developer | Built the entire application, AI integration |
