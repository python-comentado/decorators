# -*- encoding: utf-8 -*-

class User:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name
        # self.full_name = first_name + "." + last_name

    @property
    def full_name(self):
        return self.first_name + "." + self.last_name

    @full_name.setter
    def full_name(self, new_value: str):
        self.first_name, self.last_name = new_value.split(".")
    
    @full_name.deleter
    def full_name(self):
        self.first_name = None
        self.last_name = None


user = User("python", "comentado")

print(user.full_name)
# python.comentado

user.first_name = "javascript"

print(user.full_name)
# javascript.comentado

user.full_name = "java.comentado"

print(user.first_name)  # java
print(user.last_name)   # comentado
print(user.full_name)   # java.comentado

del user.full_name
print(user.first_name)  # None
print(user.last_name)   # None
