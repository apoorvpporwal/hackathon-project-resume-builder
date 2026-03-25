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

def enhance_experience(experience: str) -> str:
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["experience"],
        template="""Rewrite the following experience into strong ATS-friendly bullet points.
        Rules:
        * Use action verbs
        * Add measurable impact (numbers, %, results)
        * Be concise and professional
        
        Input: {experience}
        
        Return ONLY the rewritten experience as markdown bullets."""
    )
    chain = prompt | llm
    try:
        return chain.invoke({"experience": experience}).content
    except Exception as e:
        return f"Error: {e}"

def optimize_skills(skills: str) -> str:
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["skills"],
        template="""Organize and optimize the following skills for ATS.
        Rules:
        * Group into categories (Technical, Tools, Soft Skills)
        * Add relevant missing skills if obvious
        * Remove redundancy
        
        Input: {skills}
        
        Return ONLY the categorized list as markdown."""
    )
    chain = prompt | llm
    try:
        return chain.invoke({"skills": skills}).content
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

def generate_resume(name: str, contact: str, objective: str, enhanced_experience: str, optimized_skills: str, education: str, keywords: str) -> str:
    llm = get_llm()
    prompt = PromptTemplate(
        input_variables=["name", "contact", "objective", "enhanced_experience", "optimized_skills", "education", "keywords"],
        template="""
You are an expert resume writer and ATS optimization system.

Create a HIGH-QUALITY, ATS-OPTIMIZED, PROFESSIONAL resume in MARKDOWN format.

STRICT RULES:
- No explanations, no extra text, no headings like "Here is your resume"
- Only output the resume content
- Use clean markdown (## for sections)
- Use strong action verbs (Built, Developed, Optimized, Led, Designed)
- Each bullet must show IMPACT (use numbers if possible)
- Never write "No experience provided" — instead, intelligently convert skills/projects into experience-style bullets
- Make it look like a REAL candidate ready for hiring

---

## NAME
{name}

## CONTACT
{contact}

## SUMMARY
Rewrite this into a powerful 2–3 line professional summary:
{objective}

## SKILLS
Organize into categories (Technical, Tools, Soft Skills):
{optimized_skills}

## EXPERIENCE
Transform this into strong resume bullet points:
{enhanced_experience}

## EDUCATION
{education}

---

KEYWORDS (must be naturally included in skills/experience):
{keywords}

---

OUTPUT FORMAT EXAMPLE:

## NAME
John Doe

## CONTACT
Email | Phone | LinkedIn

## SUMMARY
2–3 impactful lines

## SKILLS
**Technical:** Python, Java  
**Tools:** Git, Docker  
**Soft Skills:** Leadership, Communication  

## EXPERIENCE
- Developed X which improved Y by Z%
- Built X using Y

## EDUCATION
Degree details

---

Now generate the final resume.
"""
    )
    chain = prompt | llm
    try:
        return chain.invoke({
            "name": name,
            "contact": contact,
            "objective": objective,
            "enhanced_experience": enhanced_experience,
            "optimized_skills": optimized_skills,
            "education": education,
            "keywords": keywords
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
