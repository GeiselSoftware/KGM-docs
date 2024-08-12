# Fuseki Setup

[Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) is open-source RDF/SPARQL server. The steps below are to have Fuseki server configured and run to be used as shacled KGM backend.

## Install

Fuseki can be downloaded from [Apache Jena Releases](https://jena.apache.org/download/index.cgi)<br/>
Use binary distribution archive `apache-jena-fuseki-5.0.0.tar.gz` Unpack that to location `FUSEKI_HOME`.

## Default server setup

To quickly setup and run Fuseki server with default KGM configuration:

```
cd $FUSEKI_HOME/run
wget https://geiselsoftware.github.io/KGM-docs/backends/fuseki/config-kgm.ttl
cd $FUSEKI_HOME
./fuseki-server --config=run/config-kgm.ttl
```

The default server setup assumes Fuseki server has persistent `kgm-default-dataset` dataset and SHACL endpoint. The configuration file [config-kgm.ttl](/KGM-docs/backends/fuseki/config-kgm.ttl) is placed into Fuseki server run directory and then server is run. The location of TDB2 directory where all K<span/>GM-related data are stored would be `$FUSEKI_HOME/kgm-default-dataset`.

## Misc

### Quick test run of Fuseki server

To run database server use command:

```
cd $FUSEKI_HOME
./fuseki-server --update --loc=/tmp/test-databases /kgm
```

At this point you should be able to access fuseki server via webbrowers at port 3030. You will have single dataset /kgm.
If you want to observe http requests you need to modify file `$FUSEKI_HOME/webapp/log4j2.properties`. You need to set property `logger.fuseki-request.level`:

```
logger.fuseki-request.level                  = DEBUG
```

After that server log will include HTTP requests processed by server.

### TBC - KGM setup testing commands

To test default Fuseki KGM setup:

```
curl -X POST http://localhost:3030/kgm-default-dataset/query -H "Content-Type: application/x-www-form-urlencoded" -H "Cache-Control: no-cache" -H "Connection: keep-alive" -d query=select%20*%20%7B%20%3Fs%20%3Fp%20%3Fo%20%7D
```

Alice-Bob upload and SHACL validation test:
```
cd /tmp
wget https://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.data.ttl
wget https://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.shacl.ttl
curl -XPOST --data-binary @./ab.data.ttl  --header 'Content-type: text/turtle' http://localhost:3030/kgm-default-dataset?default
curl -XPOST --data-binary @./ab.shacl.ttl  --header 'Content-type: text/turtle' http://localhost:3030/kgm-default-dataset/shacl?graph=default
```

### TBC - Setup using configuration file.

You can use `$FUSEKI_HOME/run/config.ttl` existing in distribution or create your own. It allows you to configure fuseki server in the way not accessible using command-line options.

```
cd $FUSEKI_HOME
./fuseki-server
```

The command above uses top run directory `$FUSEKI_HOME/run` and takes default configuration from file `$FUSEKI_HOME/run/config.ttl`. You can try to experiment with config files from [exhaustive list of example configurations](https://github.com/apache/jena/tree/main/jena-fuseki2/examples). You can copy log4j config file from `$FUSEKI/webapp` to that run directory and tune up logging. 

### TBC - Test SHACL endpoint

Place SHACL config file to `$FUSEKI_HOME/run` and start fuseki:

```
cd $FUSEKI_HOME
wget -O run/config-shacl.ttl https://raw.githubusercontent.com/apache/jena/main/jena-fuseki2/examples/config-shacl.ttl
./fuseki-server --config=run/config-shacl.ttl
```

This fuseki server configuration will create transient in-memory dataset named as `/dataset` and configure additional SHACL endpoint. You can use KGM supplied Alice-Bob example files to test SHACL validation:
```
curl -XPOST --data-binary @$KGM_HOME/examples/alice-bob/ab.ttl  --header 'Content-type: text/turtle' http://localhost:3030/dataset?default
curl -XPOST --data-binary @KGM_HOME/examples/alice-bob/ab.shacl.ttl  --header 'Content-type: text/turtle' http://localhost:3030/dataset/shacl?graph=default
```
See also [Integration with Apache Jena Fuseki](https://jena.apache.org/documentation/shacl/index.html#integration-with-apache-jena-fuseki)



-------------

RDFLib has [Dataset](https://rdflib.readthedocs.io/en/stable/apidocs/rdflib.html#rdflib.Dataset) class. It is the way to build rdflib-based vgm backend, see examples/rdflib/test-trig.py
