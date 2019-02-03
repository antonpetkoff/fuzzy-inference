from inference.system import InferenceSystem
from inference.utils import get_consequent_variable_names

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

        for variable_name, props in definitions['variables'].items():
            adjacency_list[variable_name] = []

        return adjacency_list
