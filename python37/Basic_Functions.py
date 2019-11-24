import json


def writeJsonFile(data: object = None, name: object = "UnKnown", folder: object = "data") -> object:
    if data is not None:
        print("Writing JSON file ‘{}/{}.json‘......".format(folder, name))
        json_data = json.dumps(data)
        print(json_data)
        with open('{}/{}.json'.format(folder, name), 'w') as f:
            f.write(json_data)
        print("JSON file ‘{}/{}.json‘ has been written successfully.".format(folder, name))
    else:
        print("Please provide data.")


def readJsonFile(name="UnKnown", folder="data"):
    with open('{}/{}.json'.format(folder, name)) as json_file:
        dataset = json.load(json_file)
        return dataset
        
def printDictionary(dictionary):
    for key in dictionary.keys():
        print(format(key) + ": " + format(dict[key]))