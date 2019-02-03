import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class InferenceSystem:
    def __init__(self, definitions):
        self.definitions = definitions

        self.variables = InferenceSystem.__define_variables(self.definitions)
        print('variables: {}'.format(self.variables))

        self.rules = InferenceSystem.__define_rules(self.definitions)
        print('rules: {}'.format(self.rules))

        self.system = ctrl.ControlSystem(rules=self.rules)


    @staticmethod
    def __define_variables(definitions):
        variables = {}

        for name, props in definitions['variables'].items():
            print(name)
            universe = np.arange(*props['crisp_universe'])
            print(universe)
            # TODO: decide if the variable is an antecedent or a consequent
            variables[name] = ctrl.Antecedent(
                universe=universe,
                label=name
            )

            fuzzy_values = props['fuzzy_values']
            print(fuzzy_values)

            variables[name].automf(
                number=len(fuzzy_values),
                names=fuzzy_values
            )

        return variables

    @staticmethod
    def __define_rules(definitions):
        rules = []

        return rules
