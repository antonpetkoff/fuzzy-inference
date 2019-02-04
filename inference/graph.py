from inference import InferenceSystem
from inference.utils import get_consequent_variable_names, flatten, get_root_variables

class InferenceGraph:
    def __init__(self, definitions):
        self.definitions = definitions

        self.dependency_graph = InferenceGraph.__build_dependency_graph(self.definitions)
        print('dependency_graph: {}'.format(self.dependency_graph))

        self.consequent_variable_names = get_consequent_variable_names(self.definitions)
        print('consequent_variable_names: {}'.format(self.consequent_variable_names))

        self.root_variable_names = get_root_variables(
            consequent_variable_names=self.consequent_variable_names,
            dependency_graph=self.dependency_graph
        )
        print('root_variable_names: {}'.format(self.root_variable_names))

        self.systems = InferenceGraph.__build_systems(
            definitions=self.definitions,
            dependency_graph=self.dependency_graph,
            consequent_variable_names=self.consequent_variable_names
        )
        print('systems: {}'.format(self.systems))
        print()


    def evaluate(self, inputs):
        required_inputs = self.get_required_inputs()
        if set(inputs.keys()) != required_inputs:
            raise ValueError('required inputs: {}; given: {}'.format(
                required_inputs,
                set(inputs.keys())
            ))

        self.environment = {}
        self.environment.update(inputs)

        def evaluate_variable(variable):
            if not variable in self.environment:
                system = self.systems[variable]
                inputs = {
                    input_name: evaluate_variable(input_name)
                    for input_name in system.get_required_inputs()
                }
                # get only the output for the target variable
                output = system.evaluate(inputs)[variable]
                self.environment[variable] = output

            return self.environment[variable]

        return {
            variable: evaluate_variable(variable)
            for variable in self.root_variable_names
        }


    def get_required_inputs(self):
        children_inputs = set(flatten([
            system.get_required_inputs()
            for _, system in self.systems.items()
        ]))
        return children_inputs.difference(self.consequent_variable_names)


    def visualize_result(self):
        for system in self.systems.values():
            system.visualize_result()


    @staticmethod
    def __build_systems(definitions, dependency_graph, consequent_variable_names):
        systems = {}

        for consequent in consequent_variable_names:
            filtered_definitions = {
                'variables': {
                    variable_name: props
                    for variable_name, props in definitions['variables'].items()
                    if variable_name in dependency_graph[consequent] or \
                        variable_name == consequent
                },
                'rules': [
                    rule
                    for rule in definitions['rules']
                    if rule['then'][0] == consequent
                ]
            }

            print('filtered_definitions: {}'.format(filtered_definitions))

            systems[consequent] = InferenceSystem(filtered_definitions)

        return systems


    @staticmethod
    def __build_dependency_graph(definitions):
        adjacency_list = {}

        for variable_name in definitions['variables']:
            adjacency_list[variable_name] = set()

        for rule in definitions['rules']:
            consequent_name, _ = rule['then']
            antecedents = set(map(lambda clause: clause[0], flatten(rule['if'])))

            print('{} => {}'.format(antecedents, consequent_name))

            for variable_name in antecedents:
                adjacency_list[consequent_name].add(variable_name)

        return adjacency_list
