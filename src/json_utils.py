import json


def load_json(filename):
    with open(filename, "r") as read_file:
        json_out = json.load(read_file)
    return json_out

        
    



    
