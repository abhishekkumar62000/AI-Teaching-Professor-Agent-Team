
import streamlit as st
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
import os
from agno.tools.arxiv import ArxivTools
from agno.utils.pprint import pprint_run_response
from agno.tools.serpapi import SerpApiTools

# Set page configuration
st.set_page_config(page_title="👨‍🏫 AI Teaching Agent Team", layout="centered")

# Initialize session state for API keys and topic
if 'openai_api_key' not in st.session_state:
    st.session_state['openai_api_key'] = ''
if 'composio_api_key' not in st.session_state:
    st.session_state['composio_api_key'] = ''
if 'serpapi_api_key' not in st.session_state:
    st.session_state['serpapi_api_key'] = ''
if 'topic' not in st.session_state:
    st.session_state['topic'] = ''

# Streamlit sidebar for API keys
with st.sidebar:
    st.title("API Keys Configuration")
    st.session_state['openai_api_key'] = st.text_input("Enter your OpenAI API Key", type="password").strip()
    st.session_state['composio_api_key'] = st.text_input("Enter your Composio API Key", type="password").strip()
    st.session_state['serpapi_api_key'] = st.text_input("Enter your SerpAPI Key", type="password").strip()
    
    # Add info about terminal responses
    st.info("Note: You can also view detailed agent responses\nin your terminal after execution.")


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
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
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
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
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
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
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
    model=OpenAIChat(id="gpt-4o-mini", api_key=st.session_state['openai_api_key']),
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

# Streamlit main UI
st.title("👨‍🏫 AI Teaching Agent Team")
st.markdown("Enter a topic to generate a detailed learning path and resources")

# Add info message about the agents
st.info("The agents will generate detailed learning content, roadmaps, resources, and exercises for your topic.")

# Query bar for topic input
st.session_state['topic'] = st.text_input("Enter the topic you want to learn about:", placeholder="e.g., Machine Learning, LoRA, etc.")

# Start button
if st.button("Start"):
    if not st.session_state['topic']:
        st.error("Please enter a topic.")
    else:
        # Display loading animations while generating responses
        with st.spinner("Generating Knowledge Base..."):
            professor_response: RunResponse = professor_agent.run(
                f"the topic is: {st.session_state['topic']},Don't forget to add the Google Doc link in your response.",
                stream=False
            )
            
        with st.spinner("Generating Learning Roadmap..."):
            academic_advisor_response: RunResponse = academic_advisor_agent.run(
                f"the topic is: {st.session_state['topic']},Don't forget to add the Google Doc link in your response.",
                stream=False
            )
            
        with st.spinner("Curating Learning Resources..."):
            research_librarian_response: RunResponse = research_librarian_agent.run(
                f"the topic is: {st.session_state['topic']},Don't forget to add the Google Doc link in your response.",
                stream=False
            )
            
        with st.spinner("Creating Practice Materials..."):
            teaching_assistant_response: RunResponse = teaching_assistant_agent.run(
                f"the topic is: {st.session_state['topic']},Don't forget to add the Google Doc link in your response.",
                stream=False
            )


        # No Google Doc links to display

        # Display responses in the Streamlit UI using pprint_run_response
        st.markdown("### Professor Response:")
        st.markdown(professor_response.content)
        pprint_run_response(professor_response, markdown=True)
        st.divider()
        
        st.markdown("### Academic Advisor Response:")
        st.markdown(academic_advisor_response.content)
        pprint_run_response(academic_advisor_response, markdown=True)
        st.divider()

        st.markdown("### Research Librarian Response:")
        st.markdown(research_librarian_response.content)
        pprint_run_response(research_librarian_response, markdown=True)
        st.divider()

        st.markdown("### Teaching Assistant Response:")
        st.markdown(teaching_assistant_response.content)
        pprint_run_response(teaching_assistant_response, markdown=True)
        st.divider()
# Information about the agents
st.markdown("---")
st.markdown("### About the Agents:")
st.markdown("""
- **Professor**: Researches the topic and creates a detailed knowledge base.
- **Academic Advisor**: Designs a structured learning roadmap for the topic.
- **Research Librarian**: Curates high-quality learning resources.
- **Teaching Assistant**: Creates practice materials, exercises, and projects.
""")
