FROM python
RUN apt update
WORKDIR /quanta
COPY . .
RUN pip install -r requirements.txt

