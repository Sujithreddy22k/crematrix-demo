from dotenv import load_dotenv
import os
from openai import AzureOpenAI
import azsqldb
# from prompts.prompts import SYSTEM_MESSAGE
from prompts import SYSTEM_MESSAGE
import os
import time 



load_dotenv()

api_type = "azure"
api_base = os.environ["api_base"]
api_version = os.environ["api_version"]
api_key = os.environ["api_key"]
model_name=os.environ["model_name"]





client = AzureOpenAI(api_key=api_key,azure_endpoint=api_base,api_version=api_version)

def get_completion_from_messages(system_message,user_message,model=model_name):

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': f"{user_message}"}
    ]



    response = client.chat.completions.create(

    model=model,
    messages=messages
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    start_db = time.time()

    schema_finances = azsqldb.get_schema_representation_finances()
    schemas_category = azsqldb.get_schema_representation_categories()
    schemas_city = azsqldb.get_schema_representation_city()
    end_db = time.time()

    print("time to get schema from db:",end_db-start_db)




    system_message = SYSTEM_MESSAGE.format(schema_finances=schema_finances,schema_dimcat=schemas_category,schema_dimcity=schemas_city)

    # system_message="You are a helpful assistant"
    # user_message = "Who won the football world cup in 2018?"
    user_message = "give me profits month wise with month name"
    
    start_openai = time.time()
    print(get_completion_from_messages(system_message, user_message,model="GPT4-Model"))
    
    end_openai = time.time()

    print("time taken to call the api and get the results back:",end_openai-start_openai)



    
    
    # print(get_completion_from_messages(system_message, user_message))