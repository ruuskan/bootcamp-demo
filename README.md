# LottoAG

A demo project using Flask, Python, SQLAlchemy (+ some other libraries) for getting some interesting values out of Veikkaus data.

## Installation

You need to have Python 3.x with pipenv. 

Create an environment (.env) file in your project directory. (See .env_example)

```bash
  pipenv install
```

## Running

To run the app:

```bash
  pipenv shell
  python app.py
```

If you want to have the database locally (SQLite) you can run (once):

```bash
  pipenv shell
  python create_db.py
```

## Local usage

After running the app.py go to **localhost:5000**

If the database is empty, log in with your credentials set in .env, head to **Data** tab and **Sync** the desired time period into your database.

## Deployment

~~Application has support for Heroku deployment (gunicorn).~~
  
## Author

- [@ruuskan](https://www.github.com/ruuskan)

  
## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[MIT](https://choosealicense.com/licenses/mit/)

  