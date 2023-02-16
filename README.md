A simple app for fizzbuzz game.
It provide four main API endpoints:
1. '/' or '/index': it will show briefly the other API endpoints
2. 'fizzbuzz_detail/': It takes a parameter; 'number'. It determines the fizzbuzz status for the number and return accordingly a JSON object. It save the data into the database and caches it into the cache.
3. 'fizzbuzz_list/': It takes two optional parameters; 'from_number' and 'to_number'. It will determine the fizzbuzz status for all numbers and return an object includes a list of numbers and their status. It save also numbers into both database and cache.
4. 'fizzbuzzes/': It returns all the data which are recorded into the database.


This is a containerized app. Poetry is used and all the requirements are in the pyproject.toml.
In order to bring up the app run this command:

### $ docker-compose up --build 

This will build an image named dayrizer_task and bring up three services:
1. dayrizer_app: The main app; http://127.0.0.1:8000/.
2. postgresql_db: an instance of postgres image. The database should be kept here.
3. pgadmin: provide a tool to connect to the database; "http://127.0.0.1:5051/browser/".

Test:
    Some simple tests have been added. You can run the tests by the following command:
 python manage.py test dayrizer_task/tests/
### $ python manage.py test dayrizer_task/tests/


I used isort, black, and flake8 for code convention.

For the test, a simple sqlite3 is used which is hold in the local machine.

I am eager to learn from senior developer. It would be great if you fix any minor issue you may see here. It would be greatly appreciated.




