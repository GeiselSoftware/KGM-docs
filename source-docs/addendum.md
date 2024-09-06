# Addendum
## Appendix A: prefixes

### Well-known prefixes
```
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix dash: <http://datashapes.org/dash#> .
```

### KGM prefixes
```
@prefix kgm: <http://www.geisel-software.com/RDF/KGM#> .
@prefix ab: <http://www.geisel-software.com/RDF/alice-bob#> .
@prefix nw: <http://www.geisel-software.com/RDF/NorthWind#> .
@prefix TU: <http://www.geisel-software.com/RDF/KGM/TestUser#> .
```

### Prefix *kgm:*

TBC

## Appendix B: SHACL notes

Example of SHACL definitions: [https://github.com/pyjanitor-devs/pyjviz/blob/main/rdflog.shacl.ttl](https://github.com/pyjanitor-devs/pyjviz/blob/main/rdflog.shacl.ttl)

TopQuandrant SHACL implementation: [https://github.com/TopQuadrant/shacl](https://github.com/TopQuadrant/shacl)

Validate script located at `src/main/command/`, file `shaclvalidate.sh`
Use binary distrib from https://repo1.maven.org/maven2/org/topbraid/shacl/

## Appendix C: rdflib notes

RDFLib has [Dataset](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.Dataset) class. It is the way to build rdflib-based kgm backend, see examples/rdflib/test-trig.py

