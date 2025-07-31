# main_app.py

import streamlit as st
import pandas as pd
import azsqldb
from prompts import SYSTEM_MESSAGE, Graph_system_message, Narrative_system_message, CLASSIFICATION_MESSAGE
from azure_openai import get_completion_from_messages
import json
import matplotlib.pyplot as plt
import pydoc
import base64


# from dotenv import load_dotenv
# load_dotenv()


def query_database(query, conn):
    """Run SQL query and return results in a dataframe"""
    return pd.read_sql_query(query, conn)



conn = azsqldb.create_connection()

# Schema Representation for commercial table
schema_commercial = azsqldb.get_schema_representation_commercial()
schema_residential = azsqldb.get_schema_representation_residential()



st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)


def sidebar_bg(side_bg):
    side_bg_ext = "png"
    st.markdown(
        f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
<style>

.st-emotion-cache-vk3wp9 {
    position: relative;
    background-color: rgb(226, 230, 30);
}
.st-emotion-cache-fblp2m {
    display: none;
}
.st-emotion-cache-11qx4gg {
    display: none;
}

</style>
""",
    unsafe_allow_html=True,
)
with st.sidebar:
    st.image(
        "https://www.briotech.com/wp-content/uploads/2022/05/brio-black-1.svg",
        width=250,
    )

st.title("Finance Analysis")

user_message = st.text_input("Enter your message:")


# chart_type = st.selectbox("Select chart type:", ["Table","Bar Chart", "Pie Chart"])

on_query = st.toggle("Show SQL Query")

classification = get_completion_from_messages(CLASSIFICATION_MESSAGE, user_message)
classification = classification.lower().strip()

# Step 2: Use the correct schema based on classification
is_residential = "residential" in classification

selected_schema = schema_residential if is_residential else schema_commercial
table_name = "crematrix.residential_data" if is_residential else "crematrix.commercial_data"


if user_message:

    formatted_system_message = SYSTEM_MESSAGE.format(
        selected_schema=selected_schema,
        table_name=table_name
    )

    response = get_completion_from_messages(formatted_system_message, user_message)
   
    json_start = response.find("{")
    json_end = response.rfind("}")
    response = response[json_start : json_end + 1]
    # print("before",response)

    # response = response.replace("\n", ' ')

    # print("after",response)

    json_response = json.loads(response)

    query = json_response["query"]

if on_query:

    st.write(query)


try:

    sql_results = query_database(query, conn)
    
    st.write(response)
    st.write(sql_results)

    narrative = get_completion_from_messages(
        user_message=sql_results, system_message=Narrative_system_message
    )

    st.write(narrative)

    code = get_completion_from_messages(
        user_message=sql_results, system_message=Graph_system_message
    )
    # print("Below is the AI generated code:\n")
    # print(code)

    code = code.replace("python", "\n") if "python" in code else code
    code = code.replace("```", "\n") if "```" in code else code
    # print("new_code")
    # print(code)

    exec(code)


except Exception as e:
    st.write(f"An error occurred: {e}")
    pass
