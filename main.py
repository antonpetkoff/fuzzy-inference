# from tipping_problem_example import tipping_problem_example

import json
import numpy as np
from inference import InferenceSystem


def main():
    with open('definitions_single.json') as definitions_json:
        definitions = json.load(definitions_json)

    inference_system = InferenceSystem(definitions)
    # inference_system.visualize_rules()
    result = inference_system.evaluate({
        'driving': 9.8,
        'journey_time': 2,
    })
    print('result: {}'.format(result))
    # inference_system.visualize_result()


if __name__ == "__main__":
    np.random.seed(0)
    main()
