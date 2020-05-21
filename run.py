import json
import random
import pandas as pd
from utils.load_stats import breakpoints, setup, steps, get_movement, get_bp_type, get_next_mouse

input_val = json.load(open("resources/input.json", 'r'))

for i, row in steps.iterrows():
    if row.total_steps > input_val['steps']:
        break

estep = steps[steps.apply(lambda x: x.floor % 8 == 7 and x.total_steps >= input_val['steps'], axis=1)]
estep = estep['total_steps'].tolist()
steps = steps[max(0, i-1):]
steps = list(zip(steps['floor'] + 1, steps['total_steps']))

row_dict = {    
    'steps': input_val['steps'],
    'floor': steps[0][0],
    'eclipses': (steps[0][0]-1) // 8,
    'stamina': input_val['stamina'],
    'floor_step_no': steps[0][1],
    'next_estep': estep[0],
    'floor_type': '',
    'next_mouse': '',
    'caught': '',
    'm_rng': random.random(),
    'm_cr': '',
    'c_rng': random.random(),
    'movement': ''
}

def update_row_dict(dict1):
    dict1['floor_type'] = get_bp_type(dict1['floor'])
    dict1['next_mouse'] = get_next_mouse(dict1['floor'], dict1['floor_type'], dict1['m_rng'])
    dict1['m_cr'] = setup['cr_setup'][dict1['next_mouse']]
    dict1['caught'] = (dict1['m_cr'] > dict1['c_rng'])
    dict1['movement'] = get_movement(mouse=dict1['next_mouse'], catch=dict1['caught'])

update_row_dict(row_dict)

df = pd.DataFrame(row_dict, index=[0])

def gen_next_row(i, steps, estep):
    last = df.iloc[-1]

    row_dict = {
        'steps': max(last.floor_step_no, min(last.next_estep, last.steps + last.movement)),
        'stamina': last.stamina - 1,
        'm_rng': random.random(),
        'c_rng': random.random(),
    }

    if steps[1][1] <= row_dict['steps']:
        steps.pop(0)
    if estep[0] <= row_dict['steps']:
        estep.pop(0)

    row_dict.update({
        'floor': steps[0][0],
        'eclipses': steps[0][0] // 8,
        'floor_step_no': steps[0][1],
        'next_estep': estep[0]})

    if last.next_mouse == 'eclipse' and last.caught:
        row_dict['stamina'] += setup['run_setup']['siphon']['value'] 

    update_row_dict(row_dict)
    df.loc[i] = row_dict

    return steps, estep

for i in range(1, 1000):
    steps, estep = gen_next_row(i, steps, estep)
    if df.iloc[-1].stamina == 0:
        break

pd.options.display.max_rows = 999
print(df)