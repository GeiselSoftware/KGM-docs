# K<span/>GM - User Guide

*kgm* is command-line processor utility which allows user to control and manipulate K<span/>GM-controlled graphs in backend graph database.

## Installation

### local `pip install`

```
$ python3 -m venv ~/venv/kgm
$ source ~/venv/kgm/bin/activate
$ pip install py-packages/kgm
```

## K<span/>GM path
KGM provides the way to organize the knowledge graphs in the way similar to files in traditional filesystem. It is always necessary to create KG first to specify *kgm type* and *path* using `kgm new` command:

```console
$ kgm new --kgm-graph-type shacl /alice-bob.shacl
created graph at path /alice-bob.shacl: http://www.geisel-software.com/RDF/KGM#SHACLGraph--40c4faaf-f311-4112-bfec-a945b4f7cdbb

$ kgm new --kgm-graph-type data /alice-bob
created graph at path /alice-bob: http://www.geisel-software.com/RDF/KGM#DataGraph--5f90e074-5582-4ba6-bcf5-67dc55ed4754

$ kgm ls
        kgm_path                                                  g
0        "/alice-bob"  kgm:DataGraph--5f90e074-5582-4ba6-bcf5-67dc55e...
1  "/alice-bob.shacl"  kgm:SHACLGraph--40c4faaf-f311-4112-bfec-a945b4...
```

One of the way to populate KG is to dowload .ttl file using `kgm download` command:
```console
$ kgm download /alice-bob.shacl http://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.shacl.ttl
/alice-bob.shacl http://www.geisel-software.com/RDF/KGM#SHACLGraph--40c4faaf-f311-4112-bfec-a945b4f7cdbb

$ kgm download /alice-bob http://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.data.ttl
/alice-bob http://www.geisel-software.com/RDF/KGM#DataGraph--5f90e074-5582-4ba6-bcf5-67dc55ed4754

$ kgm ls
        kgm_path                                                  g
0        "/alice-bob"  kgm:DataGraph--5f90e074-5582-4ba6-bcf5-67dc55e...
1  "/alice-bob.shacl"  kgm:SHACLGraph--40c4faaf-f311-4112-bfec-a945b4...
```

To access the KG one can use SPARQL console attached to backend database. Using `kgm query` command it is possible to issue SPARQL query:
```console
kgm query -Q '
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

select ?human ?h_name
where {
 ?g kgm:path "/alice-bob"
 graph ?g {
  ?human rdf:type ab:Human .
  ?human ab:name ?h_name .
 }
}
'
```

Output:
```sh
        human     h_name
0    ab:alice    "Alice"
1      ab:bob      "Bob"
2  ab:charlie  "Charlie"
```


## Examples
### Alice-Bob
data files location:

 - [ab.data.ttl] -- data RDF triples
 - [ab.shacl.ttl] -- SHACL structure

Alice-Bob queries:

```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

select ?owner_name ?pet_name ?pet_class
where {
  ?g kgm:path "/alice-bob"
  graph ?g {
      ?pet rdf:type ?pet_class;
           ab:name ?pet_name;
           ab:ownedBy ?owner;
      .
      ?owner ab:name ?owner_name .
  }
}
```

### NorthWind

[NorthWind](https://en.wikiversity.org/wiki/Database_Examples/Northwind) is sample SQL database. We will convert to RDF and then load into KGM-controlled Fuseki server.

data file locations:

- [northwind-sqlite.sql] -- Northwind data as SQL inserts
- [northwind.shacl.ttl] -- SHACL schema of Northwind

The script [build-rdf.py](examples/northwind/build-rdf.py) uses rdflib python package.

```console
$ wget https://geiselsoftware.github.io/KGM-docs/examples/northwind/nortwind-sqlite.sql
$ wget https://geiselsoftware.github.io/KGM-docs/examples/northwind/northwind.shacl.ttl
$ wget https://geiselsoftware.github.io/KGM-docs/examples/northwind/build-rdf.py
$ sqlite3 northwind.sqlitedb < northwind-sqlite.sql
$ python build-rdf.py > northwind.data.ttl
```

```console
$ kgm new -t data /NorthWind
$ kgm new -t shacl /NorthWind.shacl
$ kgm download /NorthWind northwind.data.ttl
$ kgm download /NorthWind.shacl northwind.shacl.ttl
$ kgm validate /NorthWind.shacl /NorthWind
```

Query examples:
```sparql
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
prefix kgm: <http://www.geisel-software.com/RDF/KGM#>
prefix nw: <http://www.geisel-software.com/RDF/NorthWind#>

select ?order (count(?od) as ?c)
where {
  ?g kgm:path "/NorthWind" .
  graph ?g {
    ?order rdf:type nw:Order;
    	   nw:order_detail ?od
  }
}
group by ?order
order by desc(?c)
```
