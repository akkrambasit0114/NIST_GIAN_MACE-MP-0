import pandas as pd
import numpy as np
import os

def reformat(df):
    # Extracting and converting data from the dataframe
    converted_data = {
        'total_energy': [float(entry['energy']['$numberDouble']) for entry in df['outputs']],
        'forces': [[[float(force.get('$numberDouble', 0)) for force in l]for l in entry['forces']] for entry in df["outputs"]],
        'stresses': [[float(stress['$numberDouble']) if isinstance(stress, dict) and '$numberDouble' in stress else 0 for stress in entry['stress']] for entry in df['outputs']],
        'atoms':[
                    {
                    'lattice_mat':[[float(l['$numberDouble']) for l in list] for list in entry['lattice']['matrix']],
                    'coords':[[float(j['$numberDouble']) for j in i['xyz']] for i in entry['sites']], 
                    'abc':[float(entry['lattice']['a']['$numberDouble']), float(entry['lattice']['b']['$numberDouble']), float(entry['lattice']['c']['$numberDouble'])],
                    'elements':[i['species'][0]['element'] for i in entry['sites']],
                    'angles':[float(entry['lattice']['alpha']['$numberDouble']), float(entry['lattice']['beta']['$numberDouble']), float(entry['lattice']['gamma']['$numberDouble'])],
                    'cartesian': False,
                    'props': ['']
                    } 
                    for entry in df["structure"]
                ]
    }
    converted_df = pd.DataFrame(converted_data)
    converted_df['total_energy'] = converted_df['total_energy'].astype(float)
    converted_df.to_csv('/Users/insomni_.ak/Documents/Machine Learning/MoTaNbTi/input/MoTaNbTi_1.csv', index=False)
    return converted_df

if __name__ == "__main__":
    with open('/Users/insomni_.ak/Documents/Machine Learning/MoTaNbTi/dump/data/output.json', 'r') as file:
        data = file.read().splitlines()
    dfs = [pd.read_json(json_str, lines=True) for json_str in data]
    df = pd.concat(dfs, ignore_index=True)

    df_modified = reformat(df)
