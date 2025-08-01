

import streamlit as st
import base64
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
import os
from agno.tools.arxiv import ArxivTools
from agno.utils.pprint import pprint_run_response
from agno.tools.serpapi import SerpApiTools

# --- Glassmorphism & Neon Dark Theme CSS ---
st.markdown('''
<style>
body, .stApp {
    background: linear-gradient(135deg, #181c2b 0%, #23243a 100%) !important;
    color: #f3f3f3 !important;
}
.stApp {
    font-family: 'Poppins', 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}
.main, .block-container {
    background: transparent !important;
}
.glass-card {
    background: rgba(30, 34, 54, 0.65);
    border-radius: 18px;
    box-shadow: 0 8px 32px 0 #1f26875e;
    backdrop-filter: blur(8px);
    border: 1.5px solid rgba(106,130,251,0.25);
    padding: 1.5em 1.2em 1.2em 1.2em;
    margin-bottom: 1.2em;
    transition: box-shadow 0.2s, border 0.2s;
}
.glass-card:hover {
    box-shadow: 0 12px 40px 0 #6a82fb55;
    border: 1.5px solid #6a82fb;
}
.stTextInput>div>div>input, .stTextArea textarea, .stSelectbox>div>div>div>div {
    background: rgba(36, 40, 60, 0.85) !important;
    color: #f3f3f3 !important;
    border: 1.5px solid #00ffe7 !important;
    border-radius: 10px !important;
    font-size: 1.08em;
}
.stButton>button {
    background: linear-gradient(90deg, #00ffe7 0%, #6a82fb 100%) !important;
    color: #181c2b !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold;
    font-size: 1.08em;
    box-shadow: 0 2px 16px 0 #00ffe755;
    transition: 0.2s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #6a82fb 0%, #00ffe7 100%) !important;
    color: #fff !important;
    transform: scale(1.05);
}
.stProgress>div>div>div>div {
    background: linear-gradient(90deg, #00ffe7 0%, #6a82fb 100%) !important;
}
.stSlider>div>div>div>div {
    background: #00ffe7 !important;
}
.stSelectbox>div>div>div>div {
    background: rgba(36, 40, 60, 0.85) !important;
    color: #f3f3f3 !important;
}
.stInfo, .stSuccess, .stWarning, .stError {
    border-radius: 12px !important;
    font-weight: 500;
    font-size: 1.08em;
    background: rgba(0,255,231,0.08) !important;
    color: #00ffe7 !important;
    border: 1.5px solid #00ffe7 !important;
}
.stSuccess { color: #00ffb0 !important; border-color: #00ffb0 !important; }
.stWarning { color: #ffe700 !important; border-color: #ffe700 !important; }
.stError { color: #ff007a !important; border-color: #ff007a !important; }
.stTabs [data-baseweb="tab"] {
    background: rgba(36, 40, 60, 0.85) !important;
    color: #fff !important;
    border-radius: 10px 10px 0 0 !important;
    font-weight: bold;
    margin-right: 2px;
    font-size: 1.08em;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #00ffe7 0%, #6a82fb 100%) !important;
    color: #181c2b !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
    color: #00ffe7 !important;
    text-shadow: 0 2px 8px #6a82fb44;
}
.stMarkdown ul, .stMarkdown ol {
    color: #f3f3f3 !important;
}
.stSidebar {
    background: linear-gradient(135deg, #181c2b 0%, #6a82fb 100%) !important;
    color: #fff !important;
}
.stSidebar .stTextInput>div>div>input, .stSidebar .stTextArea textarea, .stSidebar .stSelectbox>div>div>div>div {
    background: rgba(36, 40, 60, 0.85) !important;
    color: #f3f3f3 !important;
    border: 1.5px solid #00ffe7 !important;
    border-radius: 10px !important;
}
.stSidebar .stButton>button {
    background: linear-gradient(90deg, #00ffe7 0%, #6a82fb 100%) !important;
    color: #181c2b !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold;
    font-size: 1.08em;
    box-shadow: 0 2px 16px 0 #00ffe755;
    transition: 0.2s;
}
.stSidebar .stButton>button:hover {
    background: linear-gradient(90deg, #6a82fb 0%, #00ffe7 100%) !important;
    color: #fff !important;
    transform: scale(1.05);
}
.stDivider {
    border-top: 2px solid #00ffe7 !important;
    margin: 1.5em 0;
}
.stFileUploader>div>div {
    background: rgba(36, 40, 60, 0.85) !important;
    color: #f3f3f3 !important;
    border: 1.5px solid #00ffe7 !important;
    border-radius: 10px !important;
}
.stColumns>div {
    background: rgba(36, 40, 60, 0.35) !important;
    border-radius: 12px;
    margin-bottom: 0.5em;
}
.stMarkdown code {
    background: #181c2b !important;
    color: #00ffe7 !important;
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 1.08em;
}
</style>
''', unsafe_allow_html=True)

# Set page configuration
st.set_page_config(page_title="👨‍🏫 AI Teaching Agent Team", layout="centered")



# --- Fetch API keys from Streamlit secrets (for Streamlit Cloud) or environment as fallback ---
if 'openai_api_key' not in st.session_state or not st.session_state['openai_api_key']:
    st.session_state['openai_api_key'] = st.secrets.get('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY', ''))
if 'composio_api_key' not in st.session_state or not st.session_state['composio_api_key']:
    st.session_state['composio_api_key'] = st.secrets.get('COMPOSIO_API_KEY', os.getenv('COMPOSIO_API_KEY', ''))
if 'serpapi_api_key' not in st.session_state or not st.session_state['serpapi_api_key']:
    st.session_state['serpapi_api_key'] = st.secrets.get('SERP_API_KEY', os.getenv('SERP_API_KEY', ''))
if 'topic' not in st.session_state:
    st.session_state['topic'] = ''



# --- Sidebar Logo with Unique Style and Animation ---
logo_path = os.path.join(os.path.dirname(__file__), "Logo.png")
ai_logo_path = os.path.join(os.path.dirname(__file__), "AI.png")
encoded_logo = None
encoded_ai_logo = None
if os.path.exists(logo_path):
    with open(logo_path, "rb") as image_file:
        encoded_logo = base64.b64encode(image_file.read()).decode()
if os.path.exists(ai_logo_path):
    with open(ai_logo_path, "rb") as image_file:
        encoded_ai_logo = base64.b64encode(image_file.read()).decode()

with st.sidebar:
    # Logo and animated style
    if encoded_logo:
        st.markdown(
            f"""
            <style>
            @keyframes colorfulGlow {{
                0% {{ box-shadow: 0 0 24px #ffd200, 0 0 0px #00c6ff; filter: hue-rotate(0deg); }}
                25% {{ box-shadow: 0 0 32px #00c6ff, 0 0 12px #f7971e; filter: hue-rotate(90deg); }}
                50% {{ box-shadow: 0 0 40px #f7971e, 0 0 24px #ffd200; filter: hue-rotate(180deg); }}
                75% {{ box-shadow: 0 0 32px #00c6ff, 0 0 12px #ffd200; filter: hue-rotate(270deg); }}
                100% {{ box-shadow: 0 0 24px #ffd200, 0 0 0px #00c6ff; filter: hue-rotate(360deg); }}
            }}
            .colorful-animated-logo {{
                animation: colorfulGlow 2.5s linear infinite;
                transition: box-shadow 0.3s, filter 0.3s;
                border-radius: 30%;
                box-shadow: 0 2px 12px #00c6ff;
                border: 2px solid #ffd200;
                background: #232526;
                object-fit: cover;
            }}
            .sidebar-logo {{
                text-align: center;
                margin-bottom: 12px;
            }}
            </style>
            <div class='sidebar-logo'>
                <img class='colorful-animated-logo' src='data:image/png;base64,{encoded_logo}' alt='Logo' style='width:150px;height:150px;'>
                <div style='color:#00c6ff;font-size:1.1em;font-family:sans-serif;font-weight:bold;text-shadow:0 1px 6px #ffd200;margin-top:8px;'>Professor.Team.Agent</div>
            </div>
            <!-- Second logo below the first -->
            <div class='sidebar-AI' style='margin-top:0;'>
                {f"<img src='data:image/png;base64,{encoded_ai_logo}' alt='AI' style='width:210px;height:220px;border-radius:30%;box-shadow:0 2px 12px #00c6ff;border:2px solid #ffd200;margin-bottom:8px;background:#232526;object-fit:cover;'>" if encoded_ai_logo else "<div style='color:#ff4b4b;'>AI.png not found</div>"}
                <div style='color:#00c6ff;font-size:1.1em;font-family:sans-serif;font-weight:bold;text-shadow:0 1px 6px #ffd200;margin-top:8px;'></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Developer info and image below the logos
        st.markdown("<div style='text-align:center;font-size:1.1em;margin-top:10px;'>👨👨‍💻<b>Developer:</b> <br>Abhishek💖Yadav</br></div>", unsafe_allow_html=True)
        developer_path = os.path.join(os.path.dirname(__file__), "pic.jpg")
        developer_path = os.path.join(os.path.dirname(__file__), "pic.jpg")
        if os.path.exists(developer_path):
            st.image(developer_path, caption="Abhishek Yadav", use_container_width=True)
        else:
            st.warning("pic.jpg file not found. Please check the file path.")
    else:
        st.markdown(
            "<div style='text-align:center;font-size:2em;margin:16px 0;'>🚀</div><div style='text-align:center;color:#00c6ff;font-weight:bold;'>NewsCraft.AI</div>",
            unsafe_allow_html=True
        )
    # ...existing code for sidebar user profile and gamification...
    st.markdown("""
    <div style='background: linear-gradient(120deg, #6a82fb 0%, #fc5c7d 100%); border-radius: 16px; padding: 1.2em 1em 1em 1em; box-shadow: 0 2px 12px 0 #fc5c7d44;'>
        <h2 style='color:#fff; text-align:center; margin-bottom:0.7em;'>👤 User Profile & Progress</h2>
    </div>
    """, unsafe_allow_html=True)
    st.selectbox("Preferred Learning Style", ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"], key="learning_style")
    st.slider("Your Progress (%)", 0, 100, st.session_state.get('progress', 0), key="progress_slider")
    st.text_input("Current Section", st.session_state.get('current_section', ''), key="current_section")
    # --- Gamification ---
    if 'points' not in st.session_state:
        st.session_state['points'] = 0
    if 'level' not in st.session_state:
        st.session_state['level'] = 1
    if 'badges' not in st.session_state:
        st.session_state['badges'] = []
    st.markdown("---")
    st.markdown(f"<div style='color:#fc5c7d; font-size:1.1em; text-align:center;'><b>🏅 Points:</b> {st.session_state['points']} | <b>Level:</b> {st.session_state['level']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:#6a82fb; font-size:1.05em; text-align:center;'><b>Badges:</b> {' '.join(st.session_state['badges']) if st.session_state['badges'] else 'No badges yet.'}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='color:#fff; text-align:center;'>Your progress and preferences will be used to personalize your learning path.</div>", unsafe_allow_html=True)


# Validate API keys (only OpenAI and SerpAPI needed now)
if not st.session_state['openai_api_key'] or not st.session_state['serpapi_api_key']:
    st.error("Please enter OpenAI and SerpAPI keys in the sidebar.")
    st.stop()

# Set the OpenAI API key from session state
os.environ["OPENAI_API_KEY"] = st.session_state['openai_api_key']

# Create the Professor agent (formerly KnowledgeBuilder)
professor_agent = Agent(
    name="Professor",
    role="Research and Knowledge Specialist", 
    model=OpenAIChat(id="gpt-3.5-turbo", api_key=st.session_state['openai_api_key'], temperature=0.1),
    tools=[],
    instructions=[
        "Create a comprehensive knowledge base that covers fundamental concepts, advanced topics, and current developments of the given topic.",
        "Explain the topic from first principles first. Include key terminology, core principles, and practical applications and make it as a detailed report that anyone who's starting out can read and get maximum value out of it.",
        "Make sure it is formatted in a way that is easy to read and understand.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Create the Academic Advisor agent (formerly RoadmapArchitect)
academic_advisor_agent = Agent(
    name="Academic Advisor",
    role="Learning Path Designer",
    model=OpenAIChat(id="gpt-3.5-turbo", api_key=st.session_state['openai_api_key'], temperature=0.1),
    tools=[],
    instructions=[
        "Using the knowledge base for the given topic, create a detailed learning roadmap.",
        "Break down the topic into logical subtopics and arrange them in order of progression, a detailed report of roadmap that includes all the subtopics in order to be an expert in this topic.",
        "Include estimated time commitments for each section.",
        "Present the roadmap in a clear, structured format.",
    ],
    show_tool_calls=True,
    markdown=True
)

# Create the Research Librarian agent (formerly ResourceCurator)
research_librarian_agent = Agent(
    name="Research Librarian",
    role="Learning Resource Specialist",
    model=OpenAIChat(id="gpt-3.5-turbo", api_key=st.session_state['openai_api_key'], temperature=0.1),
    tools=[SerpApiTools(api_key=st.session_state['serpapi_api_key'])],
    instructions=[
        "Make a list of high-quality learning resources for the given topic.",
        "Use the SerpApi search tool to find current and relevant learning materials.",
        "Include technical blogs, GitHub repositories, official documentation, video tutorials, and courses.",
        "Present the resources in a curated list with descriptions and quality assessments.",
    ],
    show_tool_calls=True,
    markdown=True,
)

# Create the Teaching Assistant agent (formerly PracticeDesigner)
teaching_assistant_agent = Agent(
    name="Teaching Assistant",
    role="Exercise Creator",
    model=OpenAIChat(id="gpt-3.5-turbo", api_key=st.session_state['openai_api_key'], temperature=0.1),
    tools=[SerpApiTools(api_key=st.session_state['serpapi_api_key'])],
    instructions=[
        "Create comprehensive practice materials for the given topic.",
        "Use the SerpApi search tool to find example problems and real-world applications.",
        "Include progressive exercises, quizzes, hands-on projects, and real-world application scenarios.",
        "Ensure the materials align with the roadmap progression.",
        "Provide detailed solutions and explanations for all practice materials.",
    ],
    show_tool_calls=True,
    markdown=True,
)

st.title("👨‍🏫 AI Teaching Agent Team")

# --- Tabs for main app and AI Support Assistant Chatbot ---
tab1, tab2 = st.tabs(["Learning Team", "AI Support Assistant Chatbot"])

with tab1:
    st.markdown("""
    <div class='glass-card' style='border-left: 5px solid #00ffe7;'>
        <h2 style='color:#00ffe7; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>✨ Enter a topic to generate a detailed learning path and resources</h2>
    </div>
    """, unsafe_allow_html=True)
    st.info("The agents will generate detailed learning content, roadmaps, resources, and exercises for your topic.")
    # Query bar for topic input
    st.session_state['topic'] = st.text_input("Enter the topic you want to learn about:", placeholder="e.g., Machine Learning, LoRA, etc.")

    # --- Ensure 'started' is initialized in session state ---
    if 'started' not in st.session_state:
        st.session_state['started'] = False

    # --- Start Button for Answer Response ---
    if st.button("Start / Get Answer Response", key="start_topic"):
        if not st.session_state['topic']:
            st.error("Please enter a topic.")
        else:
            st.session_state['started'] = True
            # Display loading animations while generating responses
            with st.spinner("Generating Knowledge Base..."):
                professor_response: RunResponse = professor_agent.run(
                    f"the topic is: {st.session_state['topic']}, user learning style: {st.session_state['learning_style']}, user progress: {st.session_state['progress_slider']}%.",
                    stream=False
                )
            with st.spinner("Generating Learning Roadmap..."):
                academic_advisor_response: RunResponse = academic_advisor_agent.run(
                    f"the topic is: {st.session_state['topic']}, user learning style: {st.session_state['learning_style']}, user progress: {st.session_state['progress_slider']}%.",
                    stream=False
                )
            with st.spinner("Curating Learning Resources..."):
                research_librarian_response: RunResponse = research_librarian_agent.run(
                    f"the topic is: {st.session_state['topic']}, user learning style: {st.session_state['learning_style']}, user progress: {st.session_state['progress_slider']}%.",
                    stream=False
                )
            with st.spinner("Creating Practice Materials..."):
                teaching_assistant_response: RunResponse = teaching_assistant_agent.run(
                    f"the topic is: {st.session_state['topic']}, user learning style: {st.session_state['learning_style']}, user progress: {st.session_state['progress_slider']}%.",
                    stream=False
                )
            # Debug output: print the actual responses to the UI
            st.info(f"Professor response: {getattr(professor_response, 'content', professor_response)}")
            st.info(f"Academic Advisor response: {getattr(academic_advisor_response, 'content', academic_advisor_response)}")
            st.info(f"Research Librarian response: {getattr(research_librarian_response, 'content', research_librarian_response)}")
            st.info(f"Teaching Assistant response: {getattr(teaching_assistant_response, 'content', teaching_assistant_response)}")
            # Store responses in session state for later use
            st.session_state['professor_response'] = professor_response
            st.session_state['academic_advisor_response'] = academic_advisor_response
            st.session_state['research_librarian_response'] = research_librarian_response
            st.session_state['teaching_assistant_response'] = teaching_assistant_response
            # Use st.rerun() for newer Streamlit versions; fallback to experimental_rerun for older
            try:
                st.rerun()
            except AttributeError:
                # For older Streamlit versions
                st.experimental_rerun()

    # --- Progress Tracker & Smart Reminders ---
    def show_progress_tracker():
        st.markdown("---")
        st.markdown("""
        <div class='glass-card' style='border-left: 5px solid #6a82fb;'>
            <h3 style='color:#6a82fb; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>📈 Progress Tracker</h3>
        </div>
        """, unsafe_allow_html=True)
        progress = st.session_state.get('progress_slider', 0)
        st.progress(progress)
        completed_sections = st.session_state.get('completed_sections', [])
        st.markdown(f"<div style='color:#fff; font-size:1.08em;'><b>Completed Sections:</b> {', '.join(completed_sections) if completed_sections else 'None yet.'}</div>", unsafe_allow_html=True)
        if progress < 30:
            st.warning("Keep going! Every step counts. 💪")
        elif progress < 70:
            st.info("Great progress! Stay consistent for best results.")
        else:
            st.success("Amazing! You're close to mastering this topic.")

# --- Adaptive Learning Path and Quiz Section ---
def show_quiz_and_update_progress():
    st.markdown("""
    <div class='glass-card' style='border-left: 5px solid #00ffe7;'>
        <h4 style='color:#00ffe7; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>📝 Quick Quiz: Test Your Understanding</h4>
    </div>
    """, unsafe_allow_html=True)
    quiz_question = st.session_state.get('quiz_question', 'What is the most important concept you learned so far?')
    user_answer = st.text_input("Your Answer", key="quiz_answer")
    if st.button("Submit Quiz Answer"):
        # For demo, just increment progress and add a completed section
        st.session_state['progress_slider'] = min(100, st.session_state.get('progress_slider', 0) + 10)
        completed_sections = st.session_state.get('completed_sections', [])
        current_section = st.session_state.get('current_section', 'Section ' + str(len(completed_sections) + 1))
        if current_section not in completed_sections:
            completed_sections.append(current_section)
        st.session_state['completed_sections'] = completed_sections
        st.success("Progress updated! Your learning path will adapt accordingly.")
        st.session_state['quiz_answer'] = user_answer
        # --- Gamification: Add points and badges ---
        st.session_state['points'] += 10
        if st.session_state['points'] >= 100 and 'Quiz Master' not in st.session_state['badges']:
            st.session_state['badges'].append('🏆 Quiz Master')
        # Level up for every 50 points
        st.session_state['level'] = 1 + st.session_state['points'] // 50

# --- Smart Reminders (Motivational Nudge) ---
def show_smart_reminder():
    import random
    reminders = [
        "Remember to take short breaks for better retention!",
        "Share your progress with your study group for extra motivation.",
        "Try explaining a concept to someone else—it helps you learn!",
        "Stay curious and keep exploring new resources.",
        "Consistency is key. Even 10 minutes a day makes a difference!"
    ]
    st.markdown("""
    <div class='glass-card' style='border-left: 5px solid #ffe700;'>
        <h4 style='color:#ffe700; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>💡 Smart Reminders</h4>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Need Motivation?"):
        st.info(random.choice(reminders))

# --- Collaborative Study Groups & Peer Review ---
def show_study_groups():
    st.markdown("---")
    st.markdown("""
    <div class='glass-card' style='border-left: 5px solid #6a82fb;'>
        <h3 style='color:#6a82fb; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>👥 Study Groups & Peer Review</h3>
    </div>
    """, unsafe_allow_html=True)
    group_name = st.text_input("Join or Create a Study Group", key="group_name")
    st.write(f"You are in group: **{group_name or 'None'}**")
    st.markdown("#### Share Notes with Your Group")
    shared_note = st.text_area("Your Note", key="shared_note")
    if st.button("Share Note"):
        st.success("Note shared with your group!")
        # Gamification: Points for sharing notes
        st.session_state['points'] += 5
        if st.session_state['points'] >= 50 and 'Collaborator' not in st.session_state['badges']:
            st.session_state['badges'].append('🤝 Collaborator')
        st.session_state['level'] = 1 + st.session_state['points'] // 50
    st.markdown("#### Peer Review")
    peer_review = st.text_area("Review a peer's solution or note", key="peer_review")
    if st.button("Submit Review"):
        st.success("Your review has been submitted!")
        # Gamification: Points for peer review
        st.session_state['points'] += 5
        if st.session_state['points'] >= 75 and 'Reviewer' not in st.session_state['badges']:
            st.session_state['badges'].append('📝 Reviewer')
        st.session_state['level'] = 1 + st.session_state['points'] // 50
# --- AI-Powered Personalized Feedback on Assignments ---
def show_assignment_feedback():
    st.markdown("---")
    st.markdown("""
    <div class='glass-card' style='border-left: 5px solid #00ffb0;'>
        <h3 style='color:#00ffb0; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>🤖 Assignment Feedback (AI-Powered)</h3>
    </div>
    """, unsafe_allow_html=True)
    st.write("Upload a file or type your solution/essay below to get instant, AI-generated feedback and suggestions.")
    uploaded_file = st.file_uploader("Upload your assignment (txt, md, or pdf)", type=["txt", "md", "pdf"], key="assignment_upload")
    assignment_text = st.text_area("Or paste/type your solution here:", key="assignment_text")
    content = ""
    if uploaded_file is not None:
        try:
            content = uploaded_file.read().decode("utf-8")
        except Exception:
            content = "(Unable to decode file. Please paste your text below.)"
    elif assignment_text:
        content = assignment_text
    if st.button("Get AI Feedback"):
        if not content.strip():
            st.warning("Please upload a file or enter your solution.")
        else:
            with st.spinner("Generating feedback from Professor agent..."):
                feedback_response = professor_agent.run(f"Please provide detailed, constructive feedback and improvement suggestions for this assignment/essay:\n\n{content}", stream=False)
            st.markdown("#### 📋 AI Feedback:")
            st.markdown(feedback_response.content)
            # Gamification: Points for submitting assignment
            st.session_state['points'] += 15
            if st.session_state['points'] >= 125 and 'Consistent Learner' not in st.session_state['badges']:
                st.session_state['badges'].append('📚 Consistent Learner')
            st.session_state['level'] = 1 + st.session_state['points'] // 50

# --- One-Click Export to Google Docs/Notion ---
def show_export_buttons():
    st.markdown("---")
    st.markdown("""
    <div class='glass-card' style='border-left: 5px solid #00ffe7;'>
        <h3 style='color:#00ffe7; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>📤 Export Your Learning Materials</h3>
    </div>
    """, unsafe_allow_html=True)
    st.write("Export your personalized knowledge base, roadmap, and resources:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export to Google Docs"):
            st.info("Exporting to Google Docs... (Demo: Copy content and paste into your Google Doc)")
    with col2:
        if st.button("Export to Notion"):
            st.info("Exporting to Notion... (Demo: Copy content and paste into your Notion page)")

# --- Interactive Live Q&A Section ---
def show_live_qa():
    st.markdown("---")
    st.markdown("""
    <div class='glass-card' style='border-left: 5px solid #00ffe7;'>
        <h3 style='color:#00ffe7; text-align:center; margin-bottom:0.7em; letter-spacing:1px;'>💬 Live Q&A with Agents</h3>
    </div>
    """, unsafe_allow_html=True)
    agent_choice = st.selectbox("Which agent do you want to ask?", ["Professor", "Academic Advisor", "Research Librarian", "Teaching Assistant"], key="qa_agent")
    user_question = st.text_input("Ask your question:", key="qa_input")
    if st.button("Ask Agent"):
        with st.spinner("Getting answer from agent..."):
            if agent_choice == "Professor":
                response = professor_agent.run(user_question, stream=False)
            elif agent_choice == "Academic Advisor":
                response = academic_advisor_agent.run(user_question, stream=False)
            elif agent_choice == "Research Librarian":
                response = research_librarian_agent.run(user_question, stream=False)
            else:
                response = teaching_assistant_agent.run(user_question, stream=False)
        st.markdown(f"**{agent_choice} says:**")
        st.markdown(response.content)

    # --- Only show main features if started ---
    if st.session_state.get('started', False):
        # Debug: Check if responses exist in session state
        missing = []
        for key in [
            'professor_response',
            'academic_advisor_response',
            'research_librarian_response',
            'teaching_assistant_response']:
            if key not in st.session_state or st.session_state[key] is None:
                missing.append(key)
        if missing:
            st.warning(f"No response found for: {', '.join(missing)}.\nTry clicking the button again or check for errors in the agent code.")
        else:
            # Display responses in the Streamlit UI using pprint_run_response
            st.markdown("### Professor Response:")
            st.markdown(st.session_state['professor_response'].content)
            pprint_run_response(st.session_state['professor_response'], markdown=True)
            st.divider()
            st.markdown("### Academic Advisor Response:")
            st.markdown(st.session_state['academic_advisor_response'].content)
            pprint_run_response(st.session_state['academic_advisor_response'], markdown=True)
            st.divider()
            st.markdown("### Research Librarian Response:")
            st.markdown(st.session_state['research_librarian_response'].content)
            pprint_run_response(st.session_state['research_librarian_response'], markdown=True)
            st.divider()
            st.markdown("### Teaching Assistant Response:")
            st.markdown(st.session_state['teaching_assistant_response'].content)
            pprint_run_response(st.session_state['teaching_assistant_response'], markdown=True)
            st.divider()
        # Show progress tracker
        show_progress_tracker()
        # Show quiz and update progress
        show_quiz_and_update_progress()
        # Show smart reminders
        show_smart_reminder()
        # Show study groups and peer review
        show_study_groups()
        # Show AI-powered assignment feedback
        show_assignment_feedback()
        # Show export buttons
        show_export_buttons()
        # Show live Q&A
        show_live_qa()

# --- AI Support Assistant Chatbot Tab ---
with tab2:
    st.header("🤖 AI Support Assistant Chatbot")
    st.write("Chat one-to-one with your AI assistant. Your conversation is remembered!")
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
    # --- Enhanced Chat UI ---
    st.markdown("""
        <style>
        .chat-container {max-height: 400px; overflow-y: auto; padding: 0.5em 0; border-radius: 8px; background: #f7f7fa; border: 1px solid #e0e0e0; margin-bottom: 1em;}
        .chat-bubble-user {background: #d1e7ff; color: #222; padding: 0.7em 1em; border-radius: 18px 18px 4px 18px; margin: 0.3em 0 0.3em 2em; display: inline-block; max-width: 80%;}
        .chat-bubble-ai {background: #f0f0f0; color: #222; padding: 0.7em 1em; border-radius: 18px 18px 18px 4px; margin: 0.3em 2em 0.3em 0; display: inline-block; max-width: 80%;}
        .chat-row {display: flex; align-items: flex-end;}
        .chat-avatar {width: 32px; height: 32px; border-radius: 50%; margin: 0 0.5em;}
        .chat-row.user {justify-content: flex-end;}
        .chat-row.ai {justify-content: flex-start;}
        </style>
    """, unsafe_allow_html=True)
    # Scrollable chat area
    chat_html = ["<div class='chat-container'>"]
    for entry in st.session_state['chat_history']:
        if entry['role'] == 'user':
            chat_html.append(f"<div class='chat-row user'><div class='chat-bubble-user'>{entry['content']}</div><img class='chat-avatar' src='https://cdn-icons-png.flaticon.com/512/1946/1946429.png' alt='User'></div>")
        else:
            chat_html.append(f"<div class='chat-row ai'><img class='chat-avatar' src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' alt='AI'><div class='chat-bubble-ai'>{entry['content']}</div></div>")
    chat_html.append("</div>")
    st.markdown("\n".join(chat_html), unsafe_allow_html=True)
    # Input area with send button on same line
    col1, col2 = st.columns([8,1])
    with col1:
        user_message = st.text_area("Type your message...", key="chat_input", height=68, label_visibility="collapsed")
    with col2:
        send_clicked = st.button("➡️", key="send_chat", help="Send message")
    # Clear chat button
    if st.button("🧹 Clear Chat", key="clear_chat"):
        st.session_state['chat_history'] = []
        st.rerun()
    # Handle sending
    if send_clicked:
        if user_message.strip():
            st.session_state['chat_history'].append({'role': 'user', 'content': user_message})
            # Build conversation for context
            conversation = "\n".join([f"User: {e['content']}" if e['role']=='user' else f"AI: {e['content']}" for e in st.session_state['chat_history']])
            with st.spinner("AI is typing..."):
                ai_response = professor_agent.run(f"Continue this conversation as a helpful AI assistant.\n\n{conversation}\nAI:", stream=False)
            st.session_state['chat_history'].append({'role': 'ai', 'content': ai_response.content})
            st.rerun()
# 🌟 Meet Your AI Teaching Team
st.markdown("""
<hr style='margin-top:2em;margin-bottom:1em;border:1px solid #e0e0e0;'>
<style>
.ai-team-section {
  background: linear-gradient(120deg, #a18cd1 0%, #fbc2eb 100%);
  border-radius: 18px;
  padding: 2em 1em 1.5em 1em;
  margin-bottom: 2em;
  box-shadow: 0 4px 24px 0 rgba(120, 80, 180, 0.10);
  animation: fadeIn 1.2s;
}
.ai-team-title {
  text-align: center;
  color: #fff;
  font-size: 2.1em;
  font-weight: bold;
  letter-spacing: 1px;
  margin-bottom: 1.2em;
  text-shadow: 0 2px 8px #a18cd1;
}
.ai-team-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.5em;
}
.ai-agent-card {
  background: linear-gradient(120deg, #fbc2eb 0%, #a6c1ee 100%);
  border-radius: 16px;
  box-shadow: 0 2px 12px 0 rgba(120, 80, 180, 0.10);
  padding: 1.2em 1.1em 1em 1.1em;
  min-width: 240px;
  max-width: 320px;
  flex: 1 1 220px;
  transition: transform 0.18s, box-shadow 0.18s;
  cursor: pointer;
  border: 2px solid #fff0;
}
.ai-agent-card:hover {
  transform: translateY(-8px) scale(1.04);
  box-shadow: 0 8px 32px 0 rgba(120, 80, 180, 0.18);
  border: 2px solid #a18cd1;
}
.ai-agent-icon {
  font-size: 2.2em;
  margin-bottom: 0.3em;
  display: block;
  text-align: center;
  filter: drop-shadow(0 2px 6px #fff8);
}
.ai-agent-title {
  font-size: 1.18em;
  font-weight: bold;
  color: #3b3b6d;
  text-align: center;
  margin-bottom: 0.3em;
}
.ai-agent-desc {
  color: #4b3b5d;
  font-size: 1.05em;
  text-align: center;
  margin-bottom: 0.1em;
}
.ai-team-footer {
  text-align: center;
  margin-top: 1.5em;
  color: #fff;
  font-weight: bold;
  font-size: 1.15em;
  letter-spacing: 0.5px;
  text-shadow: 0 2px 8px #a18cd1;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
<div class='ai-team-section'>
  <div class='ai-team-title'>🌈 Meet Your AI Teaching Team</div>
  <div class='ai-team-cards'>
    <div class='ai-agent-card' title='Your expert for deep research, clear explanations, and a rich knowledge base on any topic.'>
      <span class='ai-agent-icon'>👨‍🏫</span>
      <div class='ai-agent-title'>Professor</div>
      <div class='ai-agent-desc'>Deep research, clear explanations, and a rich knowledge base on any topic.</div>
    </div>
    <div class='ai-agent-card' title='Crafts a personalized, step-by-step learning roadmap to guide your journey from beginner to expert.'>
      <span class='ai-agent-icon'>🎓</span>
      <div class='ai-agent-title'>Academic Advisor</div>
      <div class='ai-agent-desc'>Personalized, step-by-step learning roadmap for your journey.</div>
    </div>
    <div class='ai-agent-card' title='Finds and curates the best resources, tutorials, and references from across the web.'>
      <span class='ai-agent-icon'>📚</span>
      <div class='ai-agent-title'>Research Librarian</div>
      <div class='ai-agent-desc'>Curates the best resources, tutorials, and references from the web.</div>
    </div>
    <div class='ai-agent-card' title='Designs interactive exercises, quizzes, and real-world projects to boost your skills.'>
      <span class='ai-agent-icon'>🧑‍💻</span>
      <div class='ai-agent-title'>Teaching Assistant</div>
      <div class='ai-agent-desc'>Interactive exercises, quizzes, and real-world projects to boost your skills.</div>
    </div>
  </div>
  <div class='ai-team-footer'>🚀 Unlock your learning potential with your personal AI-powered teaching team!</div>
</div>
""", unsafe_allow_html=True)





