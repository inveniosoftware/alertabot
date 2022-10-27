# wh-dispatcher



Install the dependencies locally:

```bash
poetry install
poetry run uvicorn src.main:app --reload --env-file secrets.txt
```
Or run it with docker:

```bash
docker build -t wh-dispatcher .
docker run -it wh-dispatcher
```

Send a payload:

```bash
curl -X 'POST' \
  'http://ramiel.cern.ch/webhook/1' \
  -d '{"42": "your_json_data_should_go_here"}'
```
