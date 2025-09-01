### This repo is supplement for other repos
It will allow you to test solutions in web environment using simple website.

1) build docker-compose with Dockerfile:
docker compose build

2) To start wesite:
docker compose up

Project structure:
```
/test_website/
├── flask_app/               
│   ├── templates/  # html files     
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
├── nginx/ 
|	└── nginx.conf
├── .dockerignore
├── docker-compose.yml
```

3) usage:
* to access food101 inference enter:
localhost:5000/food101

* 

4) when you finish using website run:
docker compose down