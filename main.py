import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def main():
    quality = ctrl.Antecedent(universe=np.arange(0, 11, 1), label='quality')
    service = ctrl.Antecedent(universe=np.arange(0, 11, 1), label='service')
    tip = ctrl.Consequent(universe=np.arange(0, 26, 1), label='tip')

    quality.automf(number=3, variable_type='quality', names=[
        'poor', 'average', 'good'
    ])

    service.automf(number=3, variable_type='quality', names=[
        'poor', 'average', 'good'
    ])

    tip['low'] = fuzz.trimf(x=tip.universe, abc=[0, 0, 13])
    tip['medium'] = fuzz.trimf(x=tip.universe, abc=[0, 13, 25])
    tip['high'] = fuzz.trimf(x=tip.universe, abc=[13, 25, 25])

    rule1 = ctrl.Rule(
        antecedent=quality['poor'] | service['poor'],
        consequent=tip['low'],
        label='low tip rule'
    )

    rule2 = ctrl.Rule(
        antecedent=service['average'],
        consequent=tip['medium'],
        label='medium tip rule'
    )

    rule3 = ctrl.Rule(
        antecedent=service['good'] | quality['good'],
        consequent=tip['high'],
        label='high tip rule'
    )

    # rule3.view_n()

    tipping_ctrl = ctrl.ControlSystem(rules=[rule1, rule2, rule3])

    # tipping_ctrl.view_n()

    tipping = ctrl.ControlSystemSimulation(control_system=tipping_ctrl)
    tipping.inputs({
        'quality': 6.5,
        'service': 9.8
    })

    tipping.compute()

    # Mamdani 3 step inferente: aggregation, activation, accumulation
    tipping.compute_rule(rule1)
    tipping.print_state()

    # print computed output for tip
    print(tipping.output['tip'])

    # visualize tip MF activation
    tip.view(sim=tipping)


if __name__ == "__main__":
    main()
