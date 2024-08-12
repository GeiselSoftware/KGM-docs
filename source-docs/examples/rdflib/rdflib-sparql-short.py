import urllib.request
import rdflib

ttl_file_url = 'https://geiselsoftware.github.io/KGM-docs/examples/alice-bob/ab.data.ttl'
with urllib.request.urlopen(ttl_file_url) as fd:
    g = rdflib.Graph()
    g.parse(fd, format = "turtle")

    rq = """
    prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    prefix ab: <http://www.geisel-software.com/RDF/alice-bob#>

    select ?pet_name ?owner_name ?pet_class
    where {
      ?pet rdf:type ?pet_class;
           ab:name ?pet_name;
           ab:ownedBy ?owner.
      ?owner ab:name ?owner_name.
    }
    """

    for row in g.query(rq): print([str(x) for x in row])
