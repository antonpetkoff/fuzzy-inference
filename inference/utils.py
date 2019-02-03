
def flatten(l):
    return [item for sublist in l
                 for item in sublist]


def get_consequent_variable_names(definitions):
    consequent_variable_names = set()

    for rule in definitions['rules']:
        consequent_name, _ = rule['then']
        consequent_variable_names.add(consequent_name)

    return consequent_variable_names
