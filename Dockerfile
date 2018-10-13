FROM python:3
ADD . /code
WORKDIR /code
RUN apt-get update && apt-get -y install ffmpeg
RUN pip install -r requirements.txt
CMD ["python", "do_montage.py"]
