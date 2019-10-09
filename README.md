##### This repository is my backup code from my book, "Test-Driven Web Development with Python", available at www.obeythetestinggoat.com

### To Build
```
docker-compose build
```

### Run containers in background
```
docker-compose up -d
```

### Run Functional Test (Selenium)
```
docker exec -it django python3 manage.py test --tag=selenium 
```

### Run Unit Tests
```
docker exec -it django python3 manage.py test --exclude-tag=selenium 
```
