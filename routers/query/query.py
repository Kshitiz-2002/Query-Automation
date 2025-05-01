from fastapi import APIRouter
from pydantic import BaseModel
from langchain_groq import ChatGroq
from utils.LLMResponse import GenerateLLMResponse
from utils.ScrapeClass import ScrapeJobDetails
from dotenv import load_dotenv
import os

router = APIRouter(prefix='/query')
load_dotenv()

class RequestType(BaseModel):
    resume: str
    cover_letter: str
    task: str
    urls: list

global llm, instructions

@router.on_event('startup')
def _initialize():
    api = os.getenv('groq_api_key')

    global llm
    
    llm = ChatGroq(groq_api_key=api,
                   model="llama-3.3-70b-versatile", temperature=0.3)

    global instructions

    instructions = '''
                        0. **Adopt a conversational yet professional tone**: Write naturally as if you're explaining your interest and value to a hiring manager, avoiding overly formal or robotic language.

                        1. **Start with a specific reference to the company**: Mention a project, product, or initiative that directly aligns with your skills or experience. Research the company's AI-related work and integrate it naturally into the response. Avoid generic statements like "I'm excited about your innovation."

                        2. **Showcase your unique abilities and proven expertise**: Highlight your strongest abilities, previous experience, and measurable achievements that make you uniquely qualified for this role. Draw examples directly from your past work, such as specific tools (e.g., LLMs, RAG architectures) or accomplishments (e.g., "improved response accuracy by 25%").

                        3. **Demonstrate clear value to the company**: Link your achievements and skills to the company’s goals or challenges. Instead of saying "I can make an impact," explain exactly how your expertise will solve their problems, improve processes, or drive innovation.

                        4. **Provide measurable results with context**: Use one strong example with metrics to back up your claims (e.g., "I implemented a this at that that improved performance by this percent "). Avoid inventing metrics or offering vague claims.

                        5. **Make every sentence count**: Remove repetition or filler. Each sentence should serve a clear purpose—whether it's showing value, demonstrating expertise, or connecting to the company's mission.

                        6. **End with a confident, specific conclusion**: Reinforce how your unique skills will help the company succeed. Replace weak statements like "I’m excited to help" with clear, tailored contributions (e.g., "I’m eager to optimize your AI pipeline and drive measurable performance gains for your team").

                        7. **Keep it concise and focused**: Limit the response to **100-150 words** while retaining clarity, specificity, and impact. Be enthusiastic but to the point.

                        8. Replace metrics & results that are not mentioned in my resume & cover letter. Don't invent results. Only use values that are in resume & cover letter
    '''

@router.post("/")
def _query(data: RequestType):

    list_ = data.urls

    object_ = ScrapeJobDetails(list_)
    response_dict = object_._run()
    
    lr = GenerateLLMResponse(llm)

    resultList = {}

    for url in list_:

        context = lr._extract_relevant_details(
            resume=data.resume, job_desc=response_dict[url]
        )

        custom_prompt = lr._buildPrompt(
            context = context, cover_letter=data.cover_letter, jobData=response_dict[url], task=data.task)

        final_response = lr._runInferenceLoop(
            instruction=instructions, prompt=custom_prompt)

        resultList[url] = final_response

    return resultList