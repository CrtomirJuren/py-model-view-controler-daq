# conda install -c conda-forge pyyaml
import yaml
import numpy as np

voltages = np.random.randint(2, size=(1,10))

d = {'Experiment':{
        'name': 'This is a test Experiment',
        'list' : ['first', 'second','third'],}
    }

print(d['Experiment'])

with open(r'examples\yaml_test\experiment.yml', 'w') as f:
    f.write(yaml.dump(d, default_flow_style=False))

