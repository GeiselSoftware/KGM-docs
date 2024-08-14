# KGM docs

Setup kgm-docs venv:
```
python3 -m venv ~/venv/kgm-docs
source ~/venv/kgm-docs
pip install -r docs/requirements.txt
```

Local run of doc site:
```
source ~/venv/kgm-docs/bin/activate
mkdocs serve -a 0.0.0.0:8001
```

github pages shoud pick up newly generated and commit docs files from /docs location of main branch. To build and push docs to public site:
```
python3 -m venv ~/venv/kgm-docs
source ~/venv/kgm-docs
mkdocs build -d docs
git add .
git commit -m 'new docs are coming' .
git push
```
