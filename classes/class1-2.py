from class1 import Person
import numpy as np
from pprint import pprint

class Child(Person):
    def __init__(self):
        super().__init__()
    
    
    def ChildCharacter(self, kwargs) -> dict:
        characters = {}
        characters = dict(list(kwargs.items()))
        number_of_characters = len(characters)
        # characters_set_array = np.array([list(v.values()) for v in characters.values()], dtype=float)
        # for k,v in enumerate(characters.items()):
            
        return f"Number of characters: {number_of_characters}, Characters: {characters}"
    
    def ChildCharacterOutputArray(self, kwargs) -> list:
        characters = kwargs
        result = []
        for k,v in characters.items():
            # print(f"{k}: {v}")
            character_array = []
            for j in v:
                array_of_arrays = [[x, y] for x,y in j.items()]
                # for x,y in j.items():
                character_array.append(array_of_arrays)
            
            charcter_rows = []
            for i in range(0, len(character_array), 3):
                charcter_rows.append(character_array[i:i+3])
                
            result.append(charcter_rows)
        return result

    
if __name__ == "__main__":
    child1 = Child()
    characters = {
        "Character1": [{"Good": "Nice"}, {"Good": "Kind"}, {"Good": "Friendly"}, {"Good": "Generous"}, {"Good": "Loyal"}],
        "Character2": [{"Good": "Curious"}, {"Good": "Adventurous"}, {"Good": "Creative"}],
        "Character3": [{"Good": "Helpful"},]
    }
    
    print(child1.ChildCharacter(characters))
    
    pprint(child1.ChildCharacterOutputArray(characters))
    child1.PersonAge(12)
    child1.PersonName("Timmy the nigro")
    child1.PersonSummary()