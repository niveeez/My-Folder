import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from secretkey import Groq_API_Key
from dotenv import load_dotenv
load_dotenv()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.6,
    groq_api_key = os.getenv("Groq_API_Key")
    # other params...
)

def generate_restaurant_name_and_items(cuisine):
    #Chain 1: Restaurant name
    prompt_template_name = PromptTemplate(
        input_variables = ['cuisine'],
        #template = "I want to open a restaurant for {cuisine} food. Suggest only one fancy name for this. Do not preamble"
        template=(
        "I want to open a restaurant for {cuisine} food. "
        "Suggest only one fancy name for this. "
        "Return only the name. Do not add any explanation or translation. Do not preamble."
        )
    )

    name_chain = LLMChain(llm=llm, prompt = prompt_template_name, output_key="restaurant_name")

    #Chain 2: Menu items
    prompt_template_items = PromptTemplate(
    input_variables= ['restaurant_name'],
    #template = """suggest some menu items for {restaurant_name}. Return it as a comma separated list."""
    template = (
        "Suggest some menu items for {restaurant_name}."
        "Return only the name. Do not add any explanation or translation. Do not preamble."
    )

    )

    food_items_chain = LLMChain(llm=llm, prompt = prompt_template_items, output_key="menu_items")

    chain = SequentialChain(
    chains = [name_chain, food_items_chain],
    input_variables = ['cuisine'],
    output_variables = ['restaurant_name', 'menu_items']
    )

    response = chain({'cuisine': cuisine})

    return response

if __name__ == "__main__":
    print(generate_restaurant_name_and_items("Chinese"))
