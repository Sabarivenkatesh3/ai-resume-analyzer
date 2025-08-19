# agents.py
from crewai import Agent
from langchain_community.chat_models import ChatLiteLLM  # ✅ correct import
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ loads .env file


# Define LLM
llm = ChatLiteLLM(model="gemini/gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))


# Agents
parser_agent = Agent(
    role="Resume Parser",
    goal="Parse resumes into structured JSON.",
    backstory="You are an expert at reading resumes and extracting structured data.",
    llm=llm,
    allow_delegation=False
)

jd_keywords_agent = Agent(
    role="JD Keyword Extractor",
    goal="Extract important keywords, skills, and requirements from job descriptions.",
    backstory="You are skilled at keyword extraction and job analysis.",
    llm=llm,
    allow_delegation=False
)

ats_agent = Agent(
    role="ATS Evaluator",
    goal="Evaluate resumes against job descriptions with ATS logic.",
    backstory="You simulate an Applicant Tracking System (ATS) scoring process.",
    llm=llm,
    allow_delegation=False
)

improve_agent = Agent(
    role="Resume Improvement Coach",
    goal="Suggest resume improvements tailored to a specific job description.",
    backstory="You help candidates improve their resumes to increase their ATS score and recruiter appeal.",
    llm=llm,
    allow_delegation=False
)
