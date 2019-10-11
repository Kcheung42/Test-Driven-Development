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

### TODO

  * ~~Don't save black items for request~~
  * ~~Code smells: POST test is too long~~
  * ~~Display multiple items in the table~~
  * Adjust models so that items are associated with different lists
  * Add Unique URLs for each list
  * Add new URL for creating a new list via POST
  * Add URLs for adding new items to a list via POST
