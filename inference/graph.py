
class InferenceGraph:
    def __init__(self, definitions):
        self.definitions = definitions
        self.dependency_graph = InferenceGraph.__build_dependency_graph(self.definitions)
        print('dependency_graph: {}'.format(self.dependency_graph))


    @staticmethod
    def __build_dependency_graph(definitions):
        adjacency_list = {}

        for variable_name, props in definitions['variables'].items():
            adjacency_list[variable_name] = []

        return adjacency_list
