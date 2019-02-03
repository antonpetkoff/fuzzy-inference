# from tipping_problem_example import tipping_problem_example

import json
from inference import InferenceSystem


def main():
    with open('definitions_single.json') as definitions_json:
        definitions = json.load(definitions_json)

    inference_system = InferenceSystem(definitions)
    result = inference_system.evaluate({
        'driving': 9.8,
        'journey_time': 2,
    })
    print('result: {}'.format(result))


if __name__ == "__main__":
    main()
