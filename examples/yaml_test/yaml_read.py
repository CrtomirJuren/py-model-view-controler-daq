# conda install -c conda-forge pyyaml
import yaml

with open(r'src\experiment.yml', 'r') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

print(data['DAQ']['name'])