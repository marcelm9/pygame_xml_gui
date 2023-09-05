class Entity:
    def __init__(self, name, position):
        self.name = name
        self.position = position

entities = [
    Entity("Pascal", (1,1)),
    Entity("Marcel", (2,2))
]

starting_position = (0, 0)

a = 1