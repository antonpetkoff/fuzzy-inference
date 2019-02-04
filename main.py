import sys
import json
import numpy as np
from inference import InferenceSystem, InferenceGraph


def run_inference_system(definitions):
    inference_system = InferenceSystem(definitions)
    inference_system.visualize_rules()
    result = inference_system.evaluate(definitions['inputs'])
    print('result: {}'.format(result))
    inference_system.visualize_result()


def run_inference_graph(definitions):
    inference_graph = InferenceGraph(definitions)
    print('required inputs: {}'.format(inference_graph.get_required_inputs()))

    result = inference_graph.evaluate(inputs=definitions['inputs'])
    print('result: {}'.format(result))

    inference_graph.visualize_result()
    input('Press ENTER to hide result visualization')


def main(definitions):
    run_inference_graph(definitions)


if __name__ == "__main__":
    np.random.seed(0)

    if len(sys.argv) < 2:
        raise AttributeError("Missing JSON file argument")

    definitions_file = sys.argv[1]

    with open(definitions_file) as definitions_json:
        definitions = json.load(definitions_json)

    main(definitions)
