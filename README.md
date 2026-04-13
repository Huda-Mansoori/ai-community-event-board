
# AI-Powered Community Event Board

Our team proposes to develop an AI-Powered Community Event Board, a web
application that allows users to create, share, and discover local
community events such as workshops, sports activities, and study sessions.

The platform will allow users to post events with details like title,
date, location, and category. Other users will be able to browse and
discover events happening in their community.

The application will include an AI-powered feature using a Large Language
Model (LLM) to automatically generate event descriptions and recommend
events based on user interests.

The system will be implemented as a web application and will follow
DevOps practices including GitHub version control, Docker containerization,
CI/CD pipelines, and cloud deployment.

**Live App:**  https://ai-community-event-board-n0e6.onrender.com

##  Architecture Overview
User Browser
↓
Flask Web App (Render.com)
↓
Controllers → Services → Models
↓              ↓
MongoDB Atlas    Gemini AI API

### How it works:
- User interacts with the **HTML/CSS/JS frontend**
- Frontend sends requests to the **Flask backend**
- Controllers handle the requests and call the **Services layer**
- Services interact with **MongoDB Atlas** for data storage
- AI features call the **Gemini API** to generate descriptions and recommendations
- The entire app is **containerized with Docker** and deployed on **Render.com**
- Every push to main triggers **GitHub Actions** to test and auto-deploy


---

## Team Members
Huda Mansoori - 60304645 
Lolwa Al-Hemaidi - 60105155 
Abdulla Twair - 60307682 

---

## Features

-  Browse and discover local community events
- Create and post new events with title, date, location, and category
- Filter events by category
- AI-powered event description generation
- AI-powered personalized event recommendations

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Database | MongoDB Atlas |
| Frontend | HTML + CSS + JavaScript |
| AI/LLM | Google Gemini API |
| CI/CD | GitHub Actions |
| Deployment | Render.com |
| Containerization | Docker |
