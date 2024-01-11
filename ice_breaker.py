from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linedin import scrape_linkedin_profile
from dotenv import load_dotenv 

load_dotenv()


if __name__ == "__main__":
    print("hello langchain")
    
    linkedin_profile_url = linkedin_lookup_agent(name="Eden Marco Udemy")
    
    summary_template = """
                given the Linkedin information {information} about a person from I want you to create:
                1. a short summary
                2. two interesting facts about them
        """
    
    summary_promt_template = PromptTemplate(input_variables=["information"], template=summary_template)

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_promt_template)
    
    
    linkedin_data = scrape_linkedin_profile(
        "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
    )
    
    print(chain.run(information=linkedin_data))

