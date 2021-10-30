# Project: [Alpha store](https://alpha.nazarhanov.com)

![CI/CD workflow](https://github.com/nazarhanov/alpha/actions/workflows/automation.yml/badge.svg)

### Run app with `python`

```sh
pip install -r src/requirements.txt
python src/manage.py runserver 8000
```

### Run app with `docker`

```sh
docker build -t app .
docker run --network=host --env-file .env app
```
