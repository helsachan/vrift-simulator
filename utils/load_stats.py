import json
import pandas as pd

setup = json.load(open("resources/setup.json", 'r'))
setup['run_setup']['speed']['value'] = setup['run_setup']['speed']['level']
setup['run_setup']['sync']['value'] = setup['run_setup']['sync']['level'] * 10 + 30
setup['run_setup']['siphon']['value'] = setup['run_setup']['siphon']['level'] * 5 * (
    int(setup['run_setup']['super_siphon'] + 1))

breakpoints = json.load(open("resources/breakpoints.json", 'r'))
if setup['run_setup']['uu']:
    breakpoints = breakpoints['uu']
else:
    breakpoints = breakpoints['normal']

for k in setup['cr_setup'].keys():
    setup['cr_setup'][k] = float(setup['cr_setup'][k].replace('%','')) / 100

steps = pd.read_csv('resources/steps.csv')

def get_movement(mouse='normal', catch=True):
    if catch:
        m = setup['run_setup']['speed']['value']   
        if setup['run_setup']['fire']: 
            m += 1
        if mouse == 'TA':
            m *= 2
            if setup['run_setup']['string_stepping']:
                m *= 2
        return m
    else:
        if mouse == 'bulwark':
            return -10
        else:
            return -5

def get_bp_type(floor=1):
    if 1 <= floor <= 7:
        return '1-7'
    elif 8 <= floor <= 15:
        return '9-15'
    elif 16 <= floor <= 23:
        return '17-23'
    return '25+'

def get_next_mouse(floor, bp_type, rng):
    bp = breakpoints[bp_type]
    if floor % 8 == 0:
        return 'eclipse'
    if rng < bp['TA']:
        return 'TA'
    if 'bulwark' in bp.keys() and bp['TA'] < rng < bp['bulwark']:
        return 'bulwark'
    return 'normal'