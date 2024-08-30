# Fuseki Setup

[Apache Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) is open-source RDF/SPARQL server. The steps below are to have Fuseki server configured and run to be used as shacled KGM backend.

You can use browser to access Fuseki webapp. It is running by default at port 3030.

## Install

Fuseki can be downloaded from [Apache Jena Releases](https://jena.apache.org/download/index.cgi)<br/> page. Use binary distribution archive `apache-jena-fuseki-5.0.0` or newer. Unpack that to location `FUSEKI_HOME`.

### Setting up FUSEKI_HOME environment variable

Linux
```
env FUSEKI_HOME={full path to FUSEKI_HOME directory}
```
Windows
```
setx FUSEKI_HOME {full path to FUSEKI_HOME directory} /m
```

### Default server setup

To quickly setup and run Fuseki server with default KGM configuration:

Linux
```
cd $FUSEKI_HOME
mkdir run
cd run
wget https://geiselsoftware.github.io/KGM-docs/backends/fuseki/config-kgm.ttl
cd $FUSEKI_HOME
./fuseki-server --config=run/config-kgm.ttl
```
Windows
```
cd %FUSEKI_HOME%
mkdir run
cd run
curl -O https://geiselsoftware.github.io/KGM-docs/backends/fuseki/config-kgm.ttl
cd %FUSEKI_HOME%
fuseki-server --config=run/config-kgm.ttl
```

The default server setup assumes Fuseki server has persistent `kgm-default-dataset` dataset and SHACL endpoint. The configuration file [config-kgm.ttl](/KGM-docs/backends/fuseki/config-kgm.ttl) is placed into Fuseki server run directory and then server is run. The location of TDB2 directory where all K<span/>GM-related data are stored would be `$FUSEKI_HOME/kgm-default-dataset`.

### Quick test setup

To run database server use command:

Linux
```
mkdir /tmp/test-databases
cd $FUSEKI_HOME
./fuseki-server --update --loc=/tmp/test-databases /test-gdb
```
Windows
```
cd %FUSEKI_HOME%
fuseki-server --update --loc=/tmp/test-databases /test-gdb
```

At this point you should be able to access fuseki server via webbrowers at port 3030. You will have single dataset /test-gdb.
If you want to observe http requests you need to modify file `$FUSEKI_HOME/webapp/log4j2.properties`. You need to set property `logger.fuseki-request.level`:

```
logger.fuseki-request.level                  = DEBUG
```

After that server log will include HTTP requests processed by server.


To send request to Fuseki server you can use curl command:

```shell
curl -X POST http://localhost:3030/test-gdb/query -H "Content-Type: application/x-www-form-urlencoded" -H "Cache-Control: no-cache" -H "Connection: keep-alive" -d query=select%20*%20%7B%20%3Fs%20%3Fp%20%3Fo%20%7D
```

### Setup using custom configuration file

You can use `$FUSEKI_HOME/run/config.ttl` existing in distribution or create your own. It allows you to configure fuseki server in the way not accessible using command-line options.

Linux
```
cd $FUSEKI_HOME
./fuseki-server
```
Windows
```
cd %FUSEKI_HOME%
fuseki-server
```

The command above uses top run directory `$FUSEKI_HOME/run` and takes default configuration from file `$FUSEKI_HOME/run/config.ttl`. You can try to experiment with config files from [exhaustive list of example configurations](https://github.com/apache/jena/tree/main/jena-fuseki2/examples). You can copy log4j config file from `$FUSEKI/webapp` to that run directory and tune up logging. 


## Misc


### Testing SHACL server endpoint

Place SHACL config file to `$FUSEKI_HOME/run` and start fuseki:

```
cd $FUSEKI_HOME
wget -O run/config-shacl.ttl https://raw.githubusercontent.com/apache/jena/main/jena-fuseki2/examples/config-shacl.ttl
./fuseki-server --config=run/config-shacl.ttl
```

This fuseki server configuration will create transient in-memory dataset named as `/dataset` and configure additional SHACL endpoint. You can use KGM supplied Alice-Bob example files to test SHACL validation:
```
cd tmp
wget https://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.data.ttl
wget https://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.shacl.ttl
curl -XPOST --data-binary @ab.data.ttl  --header 'Content-type: text/turtle' http://localhost:3030/dataset?default
curl -XPOST --data-binary @ab.shacl.ttl  --header 'Content-type: text/turtle' http://localhost:3030/dataset/shacl?graph=default
```
See also [Integration with Apache Jena Fuseki](https://jena.apache.org/documentation/shacl/index.html#integration-with-apache-jena-fuseki)

