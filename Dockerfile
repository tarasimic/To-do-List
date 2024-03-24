FROM python:3.13.0a5-bullseye
RUN pip install virtualenv
RUN virtualenv myenv
RUN /bin/bash -c "source myenv/bin/activate"
COPY requirements.txt /app/
COPY app /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]  