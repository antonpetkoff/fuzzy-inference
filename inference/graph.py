from inference import InferenceSystem
from inference.utils import get_consequent_variable_names, flatten

class InferenceGraph:
    def __init__(self, definitions):
        self.definitions = definitions

        consequent_variable_names = get_consequent_variable_names(self.definitions)
        print('consequent_variable_names: {}'.format(consequent_variable_names))

        self.dependency_graph = InferenceGraph.__build_dependency_graph(self.definitions)
        print('dependency_graph: {}'.format(self.dependency_graph))


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
