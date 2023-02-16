Create a repository on GitHub, initialised with an empty Readme.

Build a django app which should produce an API for fetching fizzbuzz entities, a fizzbuzz entity is defined as a set of keyvalue pairs:
```
{
  "number": 1,
  "fizzbuzz": null,
  "placeholder_post": {
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
  }
}
```

The value of `fizzbuzz` key is determined by the famous fizzbuzz algorithm:
```
If number is a multiple of three, set it to “Fizz”, for multiples of five set it to “Buzz”. 
For numbers which are multiples of both three and five set it to “FizzBuzz”.
For numbers which satisfy neither of these, set it to null / None.
```

The value of `placeholder_post` should fetch the data from the relevant APIs documented on https://jsonplaceholder.typicode.com/guide/, you should only include `title` and `body` from the responses (if they are unset / missing, then set them to "" in your response). 

The API should have two endpoints:

* An endpoint that responds with a list of the first 10 fizzbuzz entities (i.e. number 1-10)
* An endpoint that includes a number parameter in the url path, e.g. `fizzbuzz/15` and responds with the relevant `fizzbuzz` entity

For submission, please create a private repository, and add timharper27, saeedghx68, and peykar as collaborators.

Key success criteria:
* Instructions on how to build and run the application locally in a README file.
* A Pipfile, requirements.txt, or equivalent to document dependencies
* A working application per the spec above
* Accompanying python based unit tests which can be run to validate that the API works as expected 
* Buildable and runnable as a Docker based application