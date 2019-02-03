import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

from functools import reduce
from inference.utils import get_consequent_variable_names

class InferenceSystem:
    def __init__(self, definitions):
        self.definitions = definitions

        consequent_variable_names = get_consequent_variable_names(self.definitions)
        print('consequent_variable_names: {}'.format(consequent_variable_names))

        self.variables = InferenceSystem.__define_variables(
            definitions=self.definitions,
            consequent_names=consequent_variable_names
        )
        print('variables: {}'.format(self.variables))

        self.rules = InferenceSystem.__define_rules(self.definitions, self.variables)
        print('rules: {}'.format(self.rules))

        self.system = ctrl.ControlSystem(rules=self.rules)


    def get_required_inputs(self) -> list:
        return set(map(lambda antecedent: antecedent.label, self.system.antecedents))


    def evaluate(self, inputs: object):
        required_inputs = self.get_required_inputs()
        if set(inputs.keys()) != required_inputs:
            print('required inputs: {}'.format(required_inputs))
            print('given: {}'.format(inputs))

        self.simulation = ctrl.ControlSystemSimulation(self.system)
        self.simulation.inputs(inputs)
        self.simulation.compute()
        # TODO: defuzzify
        return self.simulation.output


    def visualize_rules(self):
        self.system.view_n()
        input('Press ENTER to hide rule visualization')


    def visualize_result(self):
        for name in self.variables:
            self.variables[name].view(sim=self.simulation)
        input('Press ENTER to hide result visualization')


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
    def __define_rules(definitions: object, variables: object):
        rules = []

        for rule in definitions['rules']:

            def reduce_or(disjunction):
                def get_variable(expr):
                    variable_name, variable_value = expr
                    return variables[variable_name][variable_value]

                return reduce(
                    lambda a, b: a | b,
                    map(get_variable, disjunction)
                )

            def reduce_and(conjunction):
                return reduce(
                    lambda a, b: a & b,
                    map(reduce_or, conjunction)
                )

            # build a clause in conjunctive normal form
            antecedent=reduce_and(conjunction=rule['if'])

            consequent_name, consequent_value = rule['then']
            consequent=variables[consequent_name][consequent_value]

            rule = ctrl.Rule(
                antecedent=antecedent,
                consequent=consequent
            )
            rules.append(rule)

        return rules
