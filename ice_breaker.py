from ast import Tuple
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from output_parsers import person_intel_parser
from output_parsers import PersonIntel
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.linedin import scrape_linkedin_profile
from dotenv import load_dotenv

load_dotenv()


def ice_break(name: str) -> Tuple(PersonIntel, str):
    linkedin_profile_url = linkedin_lookup_agent(name=name)

    summary_template = """
                given the Linkedin information {information} about a person from I want you to create:
                1. a short summary
                2. two interesting facts about them
                3. A topic that may interest them
                4. creative Ice breakers to open a conversation with them
                \n{format_instructions}
        """

    summary_promt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_variables={
            "format_instructions": person_intel_parser.get_format_instructions()
        },
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    chain = LLMChain(llm=llm, prompt=summary_promt_template)

    linkedin_data = scrape_linkedin_profile(
        "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
    )

    result = chain.run(information=linkedin_data)
    print(result)
    return person_intel_parser.parse(result), linkedin_data.get("profile_fic_url")


if __name__ == "__main__":
    print("hello langchain")
    ice_break(name="Harrison Chase")
