import random
from rdflib import Dataset, Namespace, Literal, BNode
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, XSD
from faker import Faker
from .enums import ReifierType


def initialize_environment():
    print("Initializing RDF Graph.")

    fake = Faker()
    graph = Dataset()
    EX = Namespace("http://example.org/data/")

    graph.bind("ex", EX)
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("dcterms", DCTERMS)
    graph.bind("foaf", FOAF)
    graph.bind("xsd", XSD)

    return graph, fake, EX


def generate_rdf_data(args, graph, fake, EX):
    print(f"Generating {args.statements} statements.")

    possible_predicates = [
        FOAF.knows,
        EX.worksWith,
        EX.isMarriedTo,
        EX.dislikes
    ]

    for _ in range(args.statements):
        name_a = fake.name()
        name_b = fake.name()

        slug_a = name_a.lower().replace(" ", "_") + f"_{random.randint(10, 99)}"
        slug_b = name_b.lower().replace(" ", "_") + f"_{random.randint(10, 99)}"

        person_a_uri = EX[slug_a]
        person_b_uri = EX[slug_b]

        graph.add((person_a_uri, RDF.type, FOAF.Person))
        graph.add((person_a_uri, FOAF.name, Literal(name_a)))

        graph.add((person_b_uri, RDF.type, FOAF.Person))
        graph.add((person_b_uri, FOAF.name, Literal(name_b)))

        predicate = random.choice(possible_predicates)
        graph.add((person_a_uri, predicate, person_b_uri))


        if args.reifier_type == ReifierType.BNODE.value:
            reifier = BNode()
        else:
            statement_slug = f"stmt_{slug_a}_{slug_b}"
            reifier = EX[statement_slug]

        graph.add((reifier, RDF.type, RDF.Statement))
        graph.add((reifier, RDF.subject, person_a_uri))
        graph.add((reifier, RDF.predicate, predicate))
        graph.add((reifier, RDF.object, person_b_uri))

        metadata_choice = random.choice([1, 2, 3])
        if metadata_choice in [1, 3]:
            uncertainty_value = round(random.uniform(0.1, 1.0), 2)
            graph.add((reifier, EX.certainty, Literal(uncertainty_value, datatype=XSD.float)))

        if metadata_choice in [2, 3]:
            graph.add((reifier, DCTERMS.created, Literal(fake.date_this_year(), datatype=XSD.date)))

    return graph