# fuzzy-inference

Inference with Fuzzy Logic using Fuzzy Rules and Fuzzy Linguistic Variables

## Installation

It is recommended to run the project in a virtual environment, e.g. `virtualenv`.

Run `pip install -r requirements.txt` to install the required Python libraries.

Run `python main.py` to run the program.

## Running

Once you have defined a JSON file `my_definitions.json`
(this name is given only as an example) with fuzzy variables,
fuzzy rules and inputs, like the examples in `definitions/`,
you can run the inference graph by executing:
  `python main.py my_definitions.json`

To run the example, execute:
  `python main.py definitions/compound.json`
