FROM python:3.13


RUN apt-get update
RUN apt-get update && apt-get install -y gnupg2
RUN apt-get install -y curl apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev

WORKDIR /app

ADD app/azsqldb.py /app
ADD app/azure_openai.py /app
ADD app/prompts.py /app
ADD app/main_app_streamlit.py /app
ADD requirements.txt /app



RUN pip install -r requirements.txt 
RUN pip install pyodbc

EXPOSE 8080

# ENTRYPOINT [ "streamlit", "run" ]

CMD ["python", "-m", "streamlit", "run", "main_app_streamlit.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
