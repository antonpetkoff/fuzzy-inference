from inference import InferenceSystem
from inference.utils import get_consequent_variable_names, flatten

class InferenceGraph:
    def __init__(self, definitions):
        self.definitions = definitions

        self.dependency_graph = InferenceGraph.__build_dependency_graph(self.definitions)
        print('dependency_graph: {}'.format(self.dependency_graph))

        self.consequent_variable_names = {
            variable_name
            for variable_name, children in self.dependency_graph.items()
            if len(children) > 0
        }

        print('consequent_variable_names: {}'.format(self.consequent_variable_names))

        self.systems = InferenceGraph.__build_systems(
            definitions=self.definitions,
            dependency_graph=self.dependency_graph,
            consequent_variable_names=self.consequent_variable_names
        )
        print('systems: {}'.format(self.systems))


    def evaluate(self, inputs):
        environment = {}
        environment.update(inputs)

        # TODO:
        systems_in_post_order = []
        return {}


    def get_required_inputs(self):
        children_inputs = set(flatten([
            system.get_required_inputs()
            for _, system in self.systems.items()
        ]))
        return children_inputs.difference(self.consequent_variable_names)


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
