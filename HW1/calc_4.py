class Calc:
    def __init__(self, weight, height_cm):
        self.weight = weight
        self.height_cm = height_cm
        self.height = height_cm /100

    def bmi(self):
        return round (self.weight / (self.height**2), 2)
    
    def idealwe(self):
        if self.height_cm > 165:
            return (self.height_cm - 100)
        else:
            return (self.height_cm - 110)
        
    def diff(self):
        return (self.weight - self.idealwe())
    
    def  finale(self):
        w = self.bmi()
        if w < 18.5:
             return "Недовес, стоит больше есть"
        elif w < 25:
            return "Норма! Идеальный вес"
        elif w < 30:
            return "Избыточный вес, стоит больше заниматься спортом"
        else:
            return "Ожирение, обязательно сходи к врачу"

    def show(self):
        print(f"Вес: {self.weight} кг")
        print(f"Рост: {self.height_cm} см")
        print(f"ИМТ: {self.bmi()}")
        print(f"Идеальный вес: {self.idealwe()} кг")

        d = self.diff()
        if d > 0:
            print(f"Ты весишь на {d} кг больше нормы")
        elif d < 0:
            print(f"Ты весишь на {abs(d)} кг меньше нормы")
        else:
            print("Ты весишь ровно столько, сколько нужно!")

        print(self.finale())
def get_number(prompt):
        while True:
                try:
                    return float(input(prompt))
                except ValueError:
                    print("Ошибка: введи число")

def main():
    print("Введи свои данные, и я посчитаю ИМТ и идеальный вес.\n")

    weight = get_number("Введи вес (кг): ")
    height = get_number("Введи рост (см): ")

    calc = Calc(weight, height)
    calc.show()



