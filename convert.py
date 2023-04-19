from pathlib import Path
import json


data_file = Path("data/larin")
    
with open(data_file, 'r') as fp:
    data = json.load(fp)

result = {}
for val in data:
    result[val]=0
        
with open(data_file, 'w') as fp:
    json.dump(result, fp)
