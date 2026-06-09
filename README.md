# RDF Data Generator
A CLI tool used to generate RDF data with classic reification.

## Installation
```bash
pip install -r requirements.txt
```

## Usage examples

```bash
# Print 10 statements to console (Turtle format)
python gen.py -st 10 -f turtle
```

```bash
# Save 50 statements to an N-Triples file
python gen.py -st 50 -f ntriples -o output.nt
```

```bash
# Generate data with IRIs and specific seed (TriG format)
python gen.py -st 20 -f trig -rt iri -s 42 -o dataset.trig
```

## CLI arguments

| Flag | Argument | Required | Description |
| :--- | :--- | :---: | :--- |
| `-st` | `--statements` | Yes | Number of base statements to generate. |
| `-f` | `--format` | Yes | Output format (ntriples, turtle, nquads, trig). |
| `-o` | `--output` | No | Path to the output file (omitted = console). |
| `-rt` | `--reifier-type` | No | Reifier node type (bnode or iri). |
| `-s` | `--seed` | No | Random seed for reproducibility. |
