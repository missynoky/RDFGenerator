from generator.cli import parse_arguments
from generator.core import initialize_environment, generate_rdf_data


def main():
    args = parse_arguments()
    graph, fake, EX = initialize_environment()
    graph = generate_rdf_data(args, graph, fake, EX)

    print("\nData generated in memory.")
    print("Serializing and outputting data.\n")

    if args.output:
        graph.serialize(destination=args.output, format=args.format, encoding="utf-8")
        print(f"\nData saved to: {args.output}")
    else:
        print("Serializing and outputting data to console.\n")
        rdf_output = graph.serialize(format=args.format, encoding="utf-8")
        print(rdf_output.decode("utf-8"))

if __name__ == "__main__":
    main()