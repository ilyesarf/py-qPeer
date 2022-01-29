FROM python
RUN apt update
WORKDIR /quanta
COPY . .
RUN pip install -r requirements.txt
RUN rm *.pkl *.pem
CMD python bootstrap.py 
