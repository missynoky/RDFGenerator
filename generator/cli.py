import argparse
from .enums import RdfFormat, ReifierType

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="RDF data generator with classic reification.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path to save the generated file."
    )

    parser.add_argument(
        "-st", "--statements",
        type=int,
        required=True,
        help="Number of base statements to generate."
    )

    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=[format.value for format in RdfFormat],
        required=True,
        help="Output format of the generated RDF data."
    )

    parser.add_argument(
        "-rt", "--reifier-type",
        type=str,
        choices=[rtype.value for rtype in ReifierType],
        default=ReifierType.BNODE.value,
        help="Type of the reifier node."
    )

    return parser.parse_args()