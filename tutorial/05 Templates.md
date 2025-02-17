# Templates 

Next up, we'll get our test to pass and we'll get our page to look like something. 

To do this we'll be learning about templates.

## Views.py

Update your `todos/views.py` file so it looks like this:

```
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def index(request):

    return render(request, "todos/index.html")
```

Now if you refresh your page, you'll get an error message.

![Screenshot](images/template-error.png)

Now this part is weird. Django has an unusual way of organising templates.

Inside your app create a directory called `templates`. Then inside the `templates` directory make a new directory with the name of your app. Then inside that directory create a file called `index.html`

```
todos <<< this is your app name
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── templates   <<< make this directory
│   │   └── todos   <<< then this one. Same name as your app name
│   │       └── index.html <<<<<<< like so
│   ├── tests
│   │   └── test_todos.py
│   ├── urls.py
│   └── views.py
```

Edit `index.html` so it looks like this: 

```
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Things to do</title>
</head>

<body>
    <h1>Things to do</h1>
    Nothing to see here
</body>

</html>
```

If you refresh your web page, you will now see:

![Screenshot](images/index-v1.png)

If you are still getting a template error then kill your `runserver` and restart, then try again.

## Tests: GREEN 

Now if you run your tests using `pytest` you'll see that the test passed. 

