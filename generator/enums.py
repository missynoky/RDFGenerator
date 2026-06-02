from enum import Enum

class RdfFormat(Enum):
    NTRIPLES = 'ntriples'
    TURTLE = 'turtle'
    NQUADS = 'nquads'
    TRIG = 'trig'

class ReifierType(Enum):
    BNODE = 'bnode'
    IRI = 'iri'