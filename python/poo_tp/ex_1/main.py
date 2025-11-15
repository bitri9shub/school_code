class Robot:
    def __init__(self, nom:str, x:int = 0, y:int = 0, direction:str = "N"):
        self.nom = nom
        self.x = x
        self.y = y
        if direction not in ["N", "E", "S", "O"]:
            raise ValueError("La direction doit être 'N', 'E', 'S' ou 'O'.")
        self.direction = direction
    
    def avancer(self):
        match(self.direction):
            case "N":
                self.y += 1
            case "E":
                self.x += 1
            case "S":
                self.y -= 1
            case "O":
                self.x -= 1
    
    def tourner_gauche(self):
        if self.direction == 'N':
            self.direction = 'O'
        elif self.direction == 'S':
            self.direction = 'E'
        elif self.direction == 'E':
            self.direction = 'N'
        else:
            self.direction = 'S'

    def tourner_droite(self):
        if self.direction == 'N':
            self.direction = 'E'
        elif self.direction == 'S':
            self.direction = 'O'
        elif self.direction == 'O':
            self.direction = 'N'
        else:
            self.direction = 'S'

    def position(self):
        return f'Robot {self.nom} en position (x={self.x},y={self.y}), direction {self.direction}'


class NGRobot(Robot):
    def __init__(self, nom:str, x:int=0, y:int=0, direction:str="N", vitesse:int=1):
        super().__init__(nom, x, y, direction)
        self.vitesse = vitesse
    
    def avancer(self):
        for i in range(self.vitesse):
            super().avancer()
    
    def accelerer(self):
        self.vitesse += 1
    
    def ralentir(self):
        self.vitesse -= 1


R1 = Robot('robot 1')
print(R1.position())
R1.avancer()
R1.tourner_droite()
print(R1.position())
R2 = NGRobot('robot 2')
print(R2.position())
R2.accelerer()
R2.avancer()
print(R2.position())