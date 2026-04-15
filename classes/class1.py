

class Person: 
    def __init__(self):
        pass
    
    
    def PersonName(self, name: str):
        self.name = name
        return self.name
    
    def PersonAge(self, age: int):
        self.age = age
        return int(self.age)
    
    def PersonWeight(self, weight) -> str:
        
        weight = int(weight)
        self.weight = weight
        
        if weight < 0:
            raise ValueError(f"Weight cannot be negative -> {weight}")
        
        weight_pound = weight * 2.205
        return f"Weight is {weight} kg == {weight_pound:.2f} pounds"
    
    def PersonHight(self, hight) -> str:
        
        self.height = int(hight)
        
        if hight < 30 or hight > 300:
            raise ValueError(f"Hight must be between 30 and 300 cm -> {hight}")
        
        hight_feet = hight / 30.48
        return f"Hight is {hight} cm == {hight_feet:.1f} feet"
    
    def PersonHair(self, style: str):
        self.style = style
        return self.style
    
    def PersonSummary(self):
        summary = {}
        summary["Name"] = self.PersonName(self.name)
        summary["Age"] = self.PersonAge(self.age)
        summary["Weight"] = self.PersonWeight(self.weight)
        summary["Height"] = self.PersonHight(self.height)
        summary["Hair Style"] = self.PersonHair(self.style)
        return summary

if __name__ == "__main__":
    person1 = Person()
    person1_name = Person.PersonName(person1, "Maximillian")
    person_aga = Person.PersonAge(person1, 30)
    person_weight = Person.PersonWeight(person1, 80)
    person_hight = Person.PersonHight(person1, 204)
    person_hair = Person.PersonHair(person1, "Short")
    
    # print(person1.PersonSummary())
    for k, v in person1.PersonSummary().items():
        print(f"{k}: {v}")
    
        