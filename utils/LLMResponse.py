from tqdm import tqdm

class GenerateLLMResponse:
    def __init__(self,  llm):

       self.llm = llm

    def _extract_relevant_details(self, resume: str, job_desc: str)->str:

        prompt = f'''
            You are an experienced & harsh employer thats extracts specific important aspects from the resume that is relevant to the job Details
            You will be given text that contains multiple sentences. Only output the sentences that can be relevant to the job Details.

            Use the following rules to judge if a particular sentence is important/ relevant to the job Details or not.

            1. Extract the sentence contains specific skills mentioned in the job Details.
            2. Extract sentences that reference specific tools, technologies, frameworks, or platforms that are mentioned in the job Details.
            3. Extract sentences that highlight measurable results and are highly relevant.
            4. Extract sentences that demonstrate experience with tasks or responsibilities similar to those listed in the job Details.
            5. Extract sentences that demonstrate problem-solving ability or direct impact on previous projects or companies.
            6. Extract sentences that demonstrate previous roles or positions that are similar to the job you are hiring for should be marked as relevant.
            
            -Input Format-

            Job Description: ""
            Resume: ""

            -Output Format-

            "Relevant Sentence"
            "Relevant Sentence"

            -Instructions-

            1. Maintain the original meaning of the text, using proper grammar and vocabulary suitable for a general audience.
            2. Avoid changing the tone or intent of the original sentence.
            3. Preserve all escape sequences such as \\n (newlines) and \\t (tabs) in their exact positions in the text.
            4. Don't generate any sentence on your own. Only filter the relevant sentences from the resume
            5. Don't give results like "This skill is demonstrated in this..."
            6. Also do mention skills from the resume section

            Dont give me any code and dont mention 'json' at the top of the response. There should not be any extra output (even a single word) besides the output required.

            ######################
            -Examples-
            ######################

            Job Details: 
            
            We are looking for a Senior AI Engineer with expertise in fine-tuning large language models (LLMs) and working with retrieval-augmented generation (RAG) architectures. 
            In this role, you will help enhance our existing AI systems by fine-tuning LLMs for specific use cases, integrating RAG architectures to improve model performance, and developing high-impact AI solutions.
            Key Responsibilities:
            Fine-tune large language models (LLMs) to improve performance on domain-specific tasks.
            Design and implement RAG architectures to enhance retrieval-based AI systems.
            Collaborate with cross-functional teams to identify AI-driven solutions for business challenges.
            Optimize LLMs for both accuracy and efficiency, ensuring high-quality model output.
            Conduct thorough testing and validation of fine-tuned models to ensure robustness and scalability.
            Provide leadership and mentorship in AI model development and deployment processes.
            Required Skills:
            Proven experience in fine-tuning large language models (GPT, BERT, T5, etc.) for domain-specific tasks.
            Deep understanding of retrieval-augmented generation (RAG) architectures and integration with LLMs.
            Strong programming skills in Python, TensorFlow, PyTorch, and relevant AI libraries.
            Experience in designing and deploying AI solutions at scale.
            Knowledge of natural language processing (NLP) techniques and best practices.
            Strong communication and collaboration skills.

            Resume: 

        
            ################
            Output:

            "Led a project to fine-tune a large GPT-3 model for customer support, improving response accuracy by 20% compared to the previous version."
            "Designed and implemented a retrieval-augmented generation (RAG) architecture to integrate external knowledge sources, enhancing the relevance and diversity of generated text."
            "Optimized BERT for document classification tasks, increasing accuracy by 15% while reducing inference time by 25%."
            "Collaborated with cross-functional teams to build and deploy an LLM-powered chatbot, improving customer satisfaction by 30% through personalized interactions."
            "Implemented end-to-end pipelines for training and fine-tuning LLMs, including data preprocessing, model selection, and hyperparameter tuning."
            "Integrated RAG techniques into a content generation system, reducing reliance on pre-trained models and improving the context relevance of generated responses."
            "Developed scalable LLM fine-tuning strategies using TensorFlow and PyTorch, ensuring model performance on a range of NLP tasks."
            "Evaluated model performance through rigorous testing and validation, ensuring robustness and alignment with business needs in a production environment."

            #############################

            -Real Data-
            ######################
            Job Details: {job_desc}
            Resume: {resume}
            ######################
            Output:

        '''

        result = self._invoke(prompt)

        return result

    def _invoke(self, prompt: str)->str:

        response = self.llm.invoke(prompt)

        return response.content
        
    def _buildPrompt(self, context: str, cover_letter: str, jobData: str, task: str)->str:

        template = f'''

        Instruction: 

        Think from the perspective of an employer. Your response must sound extremely natural and should not contain buzzwords.
        Be direct & sound enthusiastic about the role. Don't give very general response. 
        Give answers that display my expertise for that particular topic

        Only return the answer to the question and nothing else. In no circumstance will yoo return anything like "I made the following changes:..."


        Details relevant to the job details:

        {context}


        My cover letter which contains my tech background:

        {cover_letter}

        Job data which includes about the job & requirements: 

        {jobData}

        {task}

        Only give me the final answer & don't give tell what changes did you make.

        '''

        return template

    def _runInferenceLoop(self, instruction: str, prompt: str):

        
        prompt = f'''
        
                Prompt: {prompt}

                Instruction: {instruction}
        '''
            
        result = self._invoke(prompt)

        return result

