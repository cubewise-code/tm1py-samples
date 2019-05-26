"""
Read rules from all cubes and sort cubes by some metrics (Number rows, Number feeders,... )
"""
import configparser

from TM1py.Services import TM1Service

config = configparser.ConfigParser()
config.read(r'..\config.ini')

# Connect to TM1
with TM1Service(**config['tm1srv01']) as tm1:
    cubes = tm1.cubes.get_all()

    # cubes with SKIPCHECK
    cubes_with_skipcheck = [cube.name for cube in cubes if cube.skipcheck]
    print("Cubes with SKIPCHECK:")
    print(cubes_with_skipcheck)

    # cubes with UNDEFVALS
    cubes_with_undefvals = [cube.name for cube in cubes if cube.undefvals]
    print("Cubes with UNDEFVALS:")
    print(cubes_with_undefvals)

    # cubes ordered by the number of rule statements
    cubes.sort(key=lambda cube: len(cube.rules.rule_statements) if cube.has_rules else 0, reverse=True)
    print("Cubes sorted by number of Rule Statements:")
    print([cube.name for cube in cubes])

    # cubes ordered by the number of feeder statements
    cubes.sort(key=lambda cube: len(cube.rules.feeder_statements) if cube.has_rules else 0, reverse=True)
    print("Cubes sorted by number of Feeder Statements:")
    print([cube.name for cube in cubes])
