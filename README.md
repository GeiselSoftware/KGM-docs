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

To publish:

```
git commit -m '... message ...' .
git push
mkdocs gh-deploy --verbose -d docs -b publish
```
