import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class InferenceSystem:
    def __init__(self, definitions):
        self.definitions = definitions

        consequent_variable_names = InferenceSystem.__get_consequent_variable_names(self.definitions)
        print('consequent_variable_names: {}'.format(consequent_variable_names))

        self.variables = InferenceSystem.__define_variables(
            definitions=self.definitions,
            consequent_names=consequent_variable_names
        )
        print('variables: {}'.format(self.variables))

        self.rules = InferenceSystem.__define_rules(self.definitions)
        print('rules: {}'.format(self.rules))

        self.system = ctrl.ControlSystem(rules=self.rules)


    @staticmethod
    def __get_consequent_variable_names(definitions):
        consequent_variable_names = set()

        for rule in definitions['rules']:
            consequent_name, _ = rule['then']
            consequent_variable_names.add(consequent_name)

        return consequent_variable_names


    @staticmethod
    def __define_variables(definitions: object, consequent_names: set = set()):
        variables = {}

        for name, props in definitions['variables'].items():
            universe = np.arange(*props['crisp_universe'])

            variables[name] = ctrl.Consequent(
                universe=universe,
                label=name
            ) if name in consequent_names else ctrl.Antecedent(
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
    def __define_rules(definitions: object):
        rules = []

        return rules
