class Student:
    def __init__(self, name:str, age:int, grade:str, favorite_subject:str):
        self.name = name
        self.age = age
        self.grade = grade
        self.favorite_subject = favorite_subject
        print(f'Имя: {self.name}, ' f'Возраст: {self.age}, ' f'Класс: {self.grade}, ' f'Любимый предмет: {self.favorite_subject}.')

    def greeting(self):
            print("Здравствуйте, Марина Евгеньевна!")

    def classmate(self):
        print("*повернулся к другу* Привет, как дела?")

if __name__ == '__main__':
    Alice = Student("Алиса", 16, "10Н", "Русский язык")
    Alice.greeting()
    Alice.classmate()

    Makar = Student("Макар", 17, "10Н", "Физкультура")
    Makar.greeting()
    Makar.classmate()