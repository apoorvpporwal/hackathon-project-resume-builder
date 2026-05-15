import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

load_dotenv(override=True)

def get_llm():
    groq_api_key = os.getenv("GROQ_API_KEY")
    # Using supported model
    return ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7, api_key=groq_api_key)

def call_llm(prompt: str) -> str:
    """Generic wrapper if raw prompt execution is ever needed without LangChain PromptTemplates."""
    llm = get_llm()
    try:
        res = llm.invoke(prompt)
        return res.content
    except Exception as e:
        return f"Error: {e}"

def extract_keywords(job_description: str) -> str:
    if not job_description or not job_description.strip():
        return ""
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["job_description"],
        template="""Extract important keywords, tools, and skills from this job description.
        Return: Comma-separated list of keywords. ONLY the list, nothing else.
        
        Input: {job_description}"""
    )
    chain = prompt | llm
    try:
        return chain.invoke({"job_description": job_description}).content
    except Exception as e:
        return ""


def generate_resume(
    name: str,
    professional_title: str,
    contact: str,
    summary: str,
    experience: str,
    skills: str,
    education: str,
    projects: str,
    certifications: str,
    achievements: str,
    activities: str,
    languages: str,
    interests: str,
    keywords: str,
) -> str:
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=[
            "name", "professional_title", "contact", "summary",
            "experience", "skills", "education", "projects",
            "certifications", "achievements", "activities",
            "languages", "interests", "keywords",
        ],
        template="""You are an elite professional resume writer. Generate a CLEAN, PROFESSIONAL, ATS-OPTIMIZED resume.

STRICT RULES:
1. Output ONLY the resume — no explanations, no "Here is your resume", no commentary
2. Use MARKDOWN formatting (# for name, ## for section headers, **bold** for emphasis)
3. Keep it CONCISE and RECRUITER-READY — no verbose paragraphs
4. Use strong action verbs with measurable impact (numbers, %, results)
5. If experience is vague, intelligently rewrite it into professional bullet points with realistic impact metrics
6. Naturally weave in these ATS keywords: {keywords}
7. NEVER say "No experience provided" — always generate meaningful content from the data given
8. Only include sections that have data provided. Skip empty sections entirely.

---

CANDIDATE DATA:
- Name: {name}
- Professional Title: {professional_title}
- Contact: {contact}
- Professional Summary: {summary}
- Experience: {experience}
- Skills: {skills}
- Education: {education}
- Projects: {projects}
- Certifications: {certifications}
- Achievements: {achievements}
- Extra-Curricular Activities: {activities}
- Languages Known: {languages}
- Interests/Hobbies: {interests}

---

FORMAT THE RESUME EXACTLY LIKE THIS:

# CANDIDATE NAME
email@example.com | +91 XXXXXXXXXX | City, State, Country | LinkedIn URL | GitHub URL

## PROFESSIONAL SUMMARY
2-3 concise lines summarizing the candidate's value proposition, strengths, and career goals. Written in third person or neutral tone. Must sound professional and specific to the target role.

## EXPERIENCE
**Company Name** | Location
*Job Title* | Start Date – End Date
- Strong bullet point starting with an action verb, explaining what you did and the measurable business impact.
- Another bullet showing skills applied and results delivered.

## EDUCATION
**Institution Name** | City, State
*Degree Name, Field of Study* | Start Year – End Year
- CGPA/Percentage: X.XX/10 or XX% (Only if provided)

## PROJECTS
**Project Name** | *Technologies Used*
- Strong bullet point explaining the project, your role, and the outcome.
- Link: GitHub URL | Live Demo URL

## SKILLS
**Languages:** Skill1, Skill2, Skill3
**Technologies/Frameworks:** Skill1, Skill2
**Tools:** Tool1, Tool2
**Soft Skills:** Skill1, Skill2

## CERTIFICATIONS
**Certification Name** | *Issuing Organization*
- Issue Date: Mar 2024 | Credential ID: ABC123

## ACHIEVEMENTS
- Achievement with brief context showing impact.

## EXTRA-CURRICULAR ACTIVITIES
- Activity with brief context showing leadership, teamwork, or initiative.

## LANGUAGES
Language1 (Proficiency), Language2 (Proficiency)

## INTERESTS
Interest1, Interest2, Interest3

---

IMPORTANT FORMATTING NOTES:
- Use EXACTLY the headers shown above. Do not invent new headers.
- Skills should be comma-separated on ONE line per category, NOT bulleted lists.
- Experience and Project bullets should be concise (1-2 lines max each).
- Keep the entire resume to 1-2 pages worth of content.
- Do NOT use ### or deeper heading levels — only # for name and ## for sections.
- SKIP any section entirely if no data was provided for it (don't add placeholder text).

Now generate the professional resume.
"""
    )
    chain = prompt | llm
    try:
        return chain.invoke({
            "name": name,
            "professional_title": professional_title,
            "contact": contact,
            "summary": summary,
            "experience": experience,
            "skills": skills,
            "education": education,
            "projects": projects,
            "certifications": certifications,
            "achievements": achievements,
            "activities": activities,
            "languages": languages,
            "interests": interests,
            "keywords": keywords,
        }).content
    except Exception as e:
        return f"Error generating resume: {str(e)}"


class ATSFeedbackDetails(BaseModel):
    ats_score: int = Field(description="ATS score (0–100)")
    strengths: list[str] = Field(description="List of strengths")
    weaknesses: list[str] = Field(description="List of weaknesses")
    missing_keywords: list[str] = Field(description="Missing keywords")
    suggestions: list[str] = Field(description="Suggestions for improvement")

def analyze_resume(resume_text: str, job_description: str) -> dict:
    if not job_description or not job_description.strip():
        return {
            "ats_score": 0,
            "strengths": [],
            "weaknesses": ["No job description provided for comparison."],
            "missing_keywords": [],
            "suggestions": []
        }
    
    llm = get_llm()
    parser = JsonOutputParser(pydantic_object=ATSFeedbackDetails)
    prompt = PromptTemplate(
        input_variables=["resume_text", "job_description"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
        template="""Analyze the following resume against the job description and provide:
1. ATS score (0–100)
2. Strengths
3. Weaknesses
4. Missing keywords
5. Suggestions for improvement

Job Description: {job_description}
Resume: {resume_text}

Output ONLY valid JSON matching this format:
{format_instructions}"""
    )
    chain = prompt | llm | parser
    try:
        return chain.invoke({
            "resume_text": resume_text,
            "job_description": job_description
        })
    except Exception as e:
        return {
            "ats_score": 0,
            "strengths": [],
            "weaknesses": [f"Error during analysis: {str(e)}"],
            "missing_keywords": [],
            "suggestions": []
        }
