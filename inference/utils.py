
def flatten(l):
    return [item for sublist in l
                 for item in sublist]


def get_consequent_variable_names(definitions: object) -> list:
    consequent_variable_names = set()

    for rule in definitions['rules']:
        consequent_name, _ = rule['then']
        consequent_variable_names.add(consequent_name)

    return consequent_variable_names


def get_root_variables(consequent_variable_names: list, dependency_graph: object) -> bool:
    def predicate(variable):
        for vertex, children in dependency_graph.items():
            if vertex != variable and variable in children:
                return False
        return True

    return list(filter(predicate, consequent_variable_names))
