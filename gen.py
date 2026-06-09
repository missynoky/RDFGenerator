import sys
from generator.cli import parse_arguments
from generator.core import initialize_environment, generate_rdf_data


def main():
    args = parse_arguments()
    graph, fake, EX = initialize_environment(seed=args.seed)
    graph = generate_rdf_data(args, graph, fake, EX)

    print("Data generated in memory.", file=sys.stderr)
    print("Serializing and outputting data.", file=sys.stderr)

    if args.output:
        graph.serialize(destination=args.output, format=args.format, encoding="utf-8")
        print(f"Data saved to: {args.output}", file=sys.stderr)
    else:
        print("Serializing and outputting data to console.\n", file=sys.stderr)
        rdf_output = graph.serialize(format=args.format, encoding="utf-8")
        print(rdf_output.decode("utf-8"))

if __name__ == "__main__":
    main()