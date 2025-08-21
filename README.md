# QuantumSketch
Quantum Circuit Rendering with LaTeX, via [qcircuit](https://github.com/CQuIC/qcircuit/tree/master).

This repository provides tools to construct quantum circuits programmatically, render them as LaTeX diagrams, and automatically export them as PDF or SVG files, including cropping and formatting.

## Features

- Build quantum circuits with single-qubit, controlled, and multi-qubit block gates.
- Automatically manage qubit wires and gate alignment for clean diagrams.
- Compile LaTeX circuit diagrams into PDF and optionally SVG.
- Auto-crop PDFs to remove whitespace.
- Specify output directories for generated files.

## Installation

First, clone the repository
```bash
git clone https://github.com/danielflight/QuantumSketch.git
cd QuantumSketch
```

Setup a virtual environment (optional)

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Now install python dependencies and ensure the required TeX packages are installed.

```bash
pip install -r requirements.txt
```

- Linux: ```sudo apt install texlive-latex-base texlive-latex-extra pdfcrop pdf2svg```
- MacOS: ```brew install mactex-no-gui pdf2svg```

Finally, install to environemnt

```bash 
pip install -e .
```

## Example of use

To obtain a plot, we need a history of all quantum gates applied in the format ```{"gate": "SYMBOL", "targets": [q1, ..., qN]}``` and, optionally, a ```"control"``` key. 

Assume we have the following circuit history (starting with the last gate):

```python
history = [
{'gate': 'S', 'targets': [1, 2]}, {'gate': 'S', 'targets': [4, 5]}, 
{'gate': 'S', 'targets': [7, 8]}, {'gate': 'S', 'targets': [10, 11]}, 
{'gate': 'BS', 'targets': [0, 1]}, {'gate': 'BS', 'targets': [3, 4]}, 
{'gate': 'BS', 'targets': [6, 7]}, {'gate': 'BS', 'targets': [9, 10]}, 
{'gate': 'BS', 'targets': [1, 3]}, {'gate': 'BS', 'targets': [6, 10]}, 
{'gate': 'BS', 'targets': [3, 10]}, {'gate': 'BS', 'targets': [1, 6]}
]
```

To obtain a pdf representation of this circuit, simply use the ```sketch_circuit()``` function:

```python

from quantumsketch import sketch_circuit

sketch_circuit(history, num_qubits = 12)

```

By default, this will create a directory named 'quantumsketch_out', containing only the .tex and .pdf (and the associated .aux, .log files). If one wishes for a cropped .pdf and .svg conversion, simply set ```just_pdf = False``` in the above function.

The PDF of this example circuit can be viewed [here](docs/example_circuit.png)




