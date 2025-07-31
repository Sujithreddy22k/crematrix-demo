FROM python:3.11-slim


RUN apt-get update
RUN apt-get update && apt-get install -y gnupg2
RUN apt-get install -y curl apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

WORKDIR /app

ADD azsqldb.py /app
ADD azure_openai.py /app
ADD prompts.py /app
ADD main_app_streamlit.py /app
ADD requirements.txt /app



RUN pip install -r requirements.txt 
RUN pip install pyodbc

EXPOSE 80

# ENTRYPOINT [ "streamlit", "run" ]

CMD [ "streamlit", "run", "main_app_streamlit.py"]