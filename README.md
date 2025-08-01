<img width="1024" height="1024" alt="AI" src="https://github.com/user-attachments/assets/ed411470-d61d-4669-bbb1-ba1454c2385b" />
OUR APP:-- https://ai-teaching-agent.streamlit.app/

<img width="1916" height="1080" alt="page0" src="https://github.com/user-attachments/assets/5b7224c6-af97-4a46-90f4-03896a63b7d3" />
<img width="1916" height="1080" alt="page1" src="https://github.com/user-attachments/assets/23ab5aa0-e54e-4e33-a701-714a11f7fdf0" />

https://github.com/user-attachments/assets/88f8bebf-4748-4ee6-94a2-c1b450792fb7
https://github.com/user-attachments/assets/62ce8894-9093-4408-b273-2e01e9c61dbd


---

# 👨‍🏫 AI Teaching Professor Agent Team

> "Empowering Learning with AI Wisdom"  
> 🌈 Meet Your AI Teaching Team

---

## 📚 Overview

**AI Teaching Professor Agent Team** is a cutting-edge, interactive, AI-powered learning assistant designed to revolutionize self-guided education. The platform enables users to master any topic with help from a coordinated team of intelligent AI agents — each with a specialized role — all within a sleek, modern interface.

This app combines gamification, responsive UI/UX, and powerful AI tools to create a dynamic, personalized, and immersive learning experience.

---

## 🎯 App Purpose

The purpose of the app is to help learners of any level gain knowledge efficiently using AI-driven agents. By entering a topic, users get:

- A custom knowledge base  
- A structured learning roadmap  
- Curated resources from the web  
- Practice quizzes, assignments, and project ideas  
- Real-time AI chat support  
- Progress tracking, gamification, and peer interaction

---

## ✨ Key Features

### 🔹 1. Sidebar

- **Animated Branding**: Displays `Logo.png` and `AI.png` with glowing effects.
- **Developer Info**: Includes your photo (`pic.jpg`) and name.
- **User Profile Panel**: Lets learners set preferences, track progress, and select learning style.
- **Gamification Elements**: Includes points, badges, and levels to boost engagement.

---

### 🔹 2. API Key Management

- Automatically loads API keys (`OpenAI`, `SerpAPI`, `Composio`) securely from `.env` file.
- Validates keys before enabling core app functionality.

---

### 🔹 3. Main Functional Tabs

#### 🧠 Learning Team Tab

Your learning is powered by a team of four specialized AI agents:

- **🧑‍🏫 Professor** – Generates a detailed knowledge base and concept report.
- **🎓 Academic Advisor** – Builds a custom learning roadmap (step-by-step guide).
- **📚 Research Librarian** – Uses SerpAPI to curate top resources (articles, videos, tools).
- **👩‍💻 Teaching Assistant** – Crafts practice quizzes, exercises, and projects.

**Other Learning Features:**

- **Topic Input**: User enters what they want to learn.
- **Start Button**: Triggers all four agents.
- **Response Cards**: Display formatted outputs from each agent.
- **Progress Tracker**: Visual progress bar with completion status.
- **Quiz Module**: Instant quiz generator and evaluator.
- **Smart Reminders**: Offers motivational nudges and suggested next steps.
- **Study Groups**: Peer-to-peer note sharing, group chat, and collaborative reviews.
- **Assignment Feedback**: Submit assignments for instant AI review.
- **Export Options**: Copy/export to Google Docs or Notion.

---

#### 💬 AI Support Assistant Chatbot Tab

- One-on-one conversation with the **Professor AI agent**.
- Maintains conversation history in a sleek chat bubble format.
- Option to clear or restart chat anytime.

---

### 🔹 4. UI / UX

- **Modern Glassmorphism & Neon Dark Theme**: Visually striking and immersive.
- **Responsive Layout**: Built with `Streamlit` columns, cards, and markdown.
- **Custom CSS Enhancements**: Stylish cards, button animations, glowing text, shadows, and smooth UI transitions.

---

### 🔹 5. Meet Your AI Teaching Team

At the bottom of the app, users meet the AI agents in a visually rich, illustrated section:
- Professor
- Academic Advisor
- Research Librarian
- Teaching Assistant

Each has a clear identity and function, making the AI team feel like real educators.

---

## 🛠️ Tech Stack

- **Frontend & UI**: Streamlit
- **AI Engine**: OpenAI GPT-3.5
- **Search Engine**: SerpAPI
- **Integration Framework**: Composio
- **Image Handling**: Base64
- **Security**: `.env` for API key protection
- **Styling**: Advanced custom CSS (glassmorphism + neon dark)

---

## 🔁 User Flow

1. User enters a **topic**.
2. Clicks **Start**.
3. AI agents generate:
   - 📖 Knowledge base
   - 🗺️ Learning roadmap
   - 🌐 Curated resources
   - 🧪 Practice content
4. User interacts by:
   - Tracking progress
   - Taking quizzes
   - Getting reminders
   - Joining peer groups
   - Exporting content
   - Asking live questions to the AI

---

## 🧩 Summary

**AI Teaching Professor Agent Team** is a next-gen learning assistant — highly personalized, visually captivating, and functionally robust. It not only guides users through complex topics but also keeps them engaged through progress tracking, AI feedback, and a rich user experience.

Whether you're a student, professional, or curious learner, this platform turns your learning into an interactive journey powered by smart agents and elegant design.


---

## 🧩 **AI Teaching Agent Team – Full Decision Tree Flow**

```mermaid
flowchart TD
    A1[🟢 App Start — Launch Streamlit UI]
    
    A1 --> A2[🧑 User Enters Topic]
    A2 --> A3{🔐 Are API Keys Valid?}
    
    A3 -- No --> A4[❌ Show Error: Missing or Invalid API Keys]
    A3 -- Yes --> A5[✅ Load Keys & Save to State]

    A5 --> B1[🚀 Trigger AI Teaching Agents]

    B1 --> C1[🧑‍🏫 Professor Agent\n→ Generate Knowledge Base]
    B1 --> C2[🎓 Academic Advisor Agent\n→ Create Learning Roadmap]
    B1 --> C3[📚 Research Librarian Agent\n→ Curate Web Resources]
    B1 --> C4[👩‍💻 Teaching Assistant Agent\n→ Create Quizzes & Practice]

    C1 --> D1[🖥️ Display Knowledge Base]
    C2 --> D1
    C3 --> D1
    C4 --> D1

    D1 --> E1{📊 Does User Want to Track Progress?}
    E1 -- Yes --> E2[📈 Show Progress Bar, Points, Levels]
    E1 -- No --> F1[⏭ Skip Gamification]

    E2 --> G1{🧪 Does User Want a Quiz?}
    G1 -- Yes --> G2[📝 Generate Quiz from Knowledge Base]
    G2 --> G3[✅ Update Progress Based on Score]
    G1 -- No --> F1

    F1 --> H1{🤝 Join Study Group or Peer Review?}
    H1 -- Yes --> H2[📓 Connect to Study Group & Share Notes]
    H1 -- No --> I1

    H2 --> I1{📝 Submit Assignment for Feedback?}
    I1 -- Yes --> I2[📤 Submit → Get Instant AI Feedback]
    I1 -- No --> J1

    I2 --> J1{📄 Export to Docs/Notion?}
    J1 -- Yes --> J2[📥 Copy / Export All Outputs]
    J1 -- No --> K1

    J2 --> K1{💬 Open AI Chat Assistant?}
    K1 -- Yes --> K2[💡 Chat with Professor Agent (Memory Enabled)]
    K1 -- No --> L1

    K2 --> L1{🔁 Restart Learning or Exit?}
    L1 -- Restart --> A2
    L1 -- Exit --> Z1[✅ Session Complete]

    A4 --> Z1
```

---

## 🔄 Summary of Each Phase

| **Phase**         | **Action**                                                     |
| ----------------- | -------------------------------------------------------------- |
| 🧑 Input          | User enters topic to learn                                     |
| 🔐 Validation     | API keys (OpenAI, SerpAPI, Composio) are checked               |
| 🤖 Agent Trigger  | All 4 agents generate their respective content                 |
| 🖥️ UI Display    | Output is shown in Streamlit (with animations and layout)      |
| 🎮 Gamification   | Optional — levels, badges, and progress bar shown              |
| 🧪 Quiz           | Optional — user takes auto-generated quiz and updates score    |
| 🤝 Collaboration  | Optional — join study group or peer review                     |
| 📝 Assignment     | Optional — submit work to receive AI feedback                  |
| 📤 Export         | Export entire learning module to Google Docs / Notion          |
| 💬 AI Chat        | Optional — chat with the AI Professor using memory and context |
| 🔁 Restart / Exit | User decides whether to learn a new topic or exit              |

---

---
def validate_keys_node(state):
    import os
    assert os.getenv("OPENAI_API_KEY"), "Missing OpenAI Key"
    assert os.getenv("SERPAPI_KEY"), "Missing SerpAPI Key"
    assert os.getenv("COMPOSIO_API_KEY"), "Missing Composio Key"
    return {"keys_validated": True}

--- 
---

## 🚀 Developed by

**👨‍💻 Code with Abhi**  
*Building the future of intelligent learning experiences.*


---

