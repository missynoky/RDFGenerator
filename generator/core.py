import random
from rdflib import Dataset, Namespace, Literal, BNode
from rdflib.namespace import RDF, RDFS, DCTERMS, FOAF, XSD
from faker import Faker
from .enums import ReifierType


def initialize_environment(seed=None):
    if seed is not None:
        random.seed(seed)
        Faker.seed(seed)

    fake = Faker()
    if seed is not None:
        fake.seed_instance(seed)

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

    base_triples_pool = []

    chars = '0123456789abcdef'

    for _ in range(args.statements):
        if base_triples_pool and random.random() < 0.30:
            person_a_uri, predicate, person_b_uri, slug_a, slug_b = random.choice(base_triples_pool)
        else:
            name_a = fake.name()
            name_b = fake.name()

            slug_a = name_a.lower().replace(" ", "_") + f"_{''.join(random.choices(chars, k=4))}"
            slug_b = name_b.lower().replace(" ", "_") + f"_{''.join(random.choices(chars, k=4))}"

            person_a_uri = EX[slug_a]
            person_b_uri = EX[slug_b]

            graph.add((person_a_uri, RDF.type, FOAF.Person))
            graph.add((person_a_uri, FOAF.name, Literal(name_a)))

            graph.add((person_b_uri, RDF.type, FOAF.Person))
            graph.add((person_b_uri, FOAF.name, Literal(name_b)))

            predicate = random.choice(possible_predicates)

            base_triples_pool.append((person_a_uri, predicate, person_b_uri, slug_a, slug_b))

            if random.choice([True, False]):
                graph.add((person_a_uri, predicate, person_b_uri))

        if args.reifier_type == ReifierType.BNODE.value:
            reifier = BNode()
        else:
            unique_id = ''.join(random.choices(chars, k=8))
            statement_slug = f"stmt_{slug_a}_{slug_b}_{unique_id}"
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

        if random.random() < 0.20:
            social_platforms = [
                "LinkedIn",
                "Facebook",
                "Instagram",
                "X",
                "Snapchat"
            ]
            source_node = EX[random.choice(social_platforms)]

            meta_predicates = [EX.indicates, EX.shows, EX.suggests, EX.confirms]
            chosen_meta = random.choice(meta_predicates)

            if random.choice([True, False]):
                graph.add((source_node, chosen_meta, reifier))

            if args.reifier_type == ReifierType.BNODE.value:
                nested_reifier = BNode()
            else:
                nested_id = ''.join(random.choices(chars, k=8))
                nested_slug = f"nested_stmt_{nested_id}"
                nested_reifier = EX[nested_slug]

            graph.add((nested_reifier, RDF.type, RDF.Statement))
            graph.add((nested_reifier, RDF.subject, source_node))
            graph.add((nested_reifier, RDF.predicate, chosen_meta))
            graph.add((nested_reifier, RDF.object, reifier))

            nested_certainty = round(random.uniform(0.5, 1.0), 2)
            graph.add((nested_reifier, EX.certainty, Literal(nested_certainty, datatype=XSD.float)))

    return graph