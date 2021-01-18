# Pre-requisites
- docker
- django
- django rest framework

# Initial setup

You can execute the provided Dockerfile by running:\
docker build -t ratestask .


This will create a container with the name ratestask, which you can start in the following way:\
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask


This will migrate models in to docker database by running in another terminal:\
cd ../xeneta folder\
python3 manage.py migrations


# Running the application

Start the local server:\
python manage.py runserver


Task 1: HTTP-based API\
GET Request Task\
        Part 1 ex: http://127.0.0.1:8000/rates?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main \
        Part 2 ex: http://127.0.0.1:8000/rates_null?date_from=2016-01-01&date_to=2016-01-10&origin=CNSGH&destination=north_europe_main

POST Request Task\
        Part 1 ex: http://127.0.0.1:8000/\
        Part 2 I couldn't use the external api because it requires registration

Task 2: Batch Processing Task
For updating large amounts of data we need to take into consideration standardization of the recieved data in order to be sure \
that the date provided to us has the same format as our database tables.\
Another aspect that we should be aware of is the space of the database server to be sure that we don't run out of space and of course \
also the memory to be sure that the batch can be processed.