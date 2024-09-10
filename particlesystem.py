from typing import Any
from time import perf_counter
from random import choice, random

clear_screen: str = "\033[2J"
mv_cursor: str    = "\033[H"
CLEAR: str        = mv_cursor+clear_screen


BLOCK = "█"
RED = "\033[0;31m"
YELLOW = "\033[1;33m"
BLACK = "\033[30m"

BRIGHT_WHITE = "\033[97m"
BRIGHT_RED   = "\033[91m"
BRIGHT_YEL   = "\033[93m"

END = "\033[0m"

RED_BLOCK = f"{RED}{BLOCK}{END}"
YEL_BLOCK = f"{YELLOW}{BLOCK}{END}"

BRED_BLOCK = f"{BRIGHT_RED}{BLOCK}{END}"
BYEL_BLOCK = f"{BRIGHT_YEL}{BLOCK}{END}"

fire_effect = (BYEL_BLOCK, BYEL_BLOCK, BRED_BLOCK)
curly_brackets_effect = ("{", "}", ".")
esses_and_z_effect = ( "Ƨ", "S", "z")

CHAR1 = CHAR2 = YEL_BLOCK
CHAR3 = RED_BLOCK

def clear() -> None:
    print(clear_screen+mv_cursor)


class Particle:
    def __init__(self, pos: tuple[int, int], master: list[Any], active: bool, always_active: bool = False, max_time: float|int|None = None, effect: tuple[str, str, str] = ("{", "}", ".")) -> None:
        self.pos = pos
        self.char = effect[0]
        self.active = active
        self.master = master
        self.max_time = max_time
        self.always_active = always_active
        
        self.effect = effect
        assert len(self.effect) == 3, "Only 3 Characters are supported"
        self.CHAR1 = effect[0]
        self.CHAR2 = effect[1]
        self.CHAR3 = effect[2]

        self.birth: float = -1.0
        self.timealive: float = 0.0


        x, y = self.pos

        #calculating max particles above
        xperc: float = (x+1)/len(self.master[0])*100
        if xperc < 50: 
            self.max_above: float = len(self.master)*xperc/100+1
        else:
            self.max_above: float = len(self.master)*(100-xperc)/100+1

        self.around_center: bool = False

        if self.max_time is None:
            self.max_time = abs(self.max_above)
            if xperc in range(35, 66):
                self.around_center = True
                self.max_time = self.always_active = True

        self.master[y][x] = self
        self.update()

    def switch_char(self) -> None:
        if self.char == self.CHAR1 and random() > 0.5:
            self.char = self.CHAR2
        else:
            self.char = self.CHAR1

    def deactivate(self) -> None:
        self.active = False
        self.birth = -1.0

    def activate(self) -> None:
        self.active = True
        self.birth = perf_counter()

    def update(self) -> None:
        if self.active:
            self.timealive: float = perf_counter() - self.birth
            timepercmax: float|int = self.timealive/self.max_time*100

            all_particles_above: list[Particle] = [ row[self.pos[0]] for row in self.master[:self.pos[1]]]
            active_particles_above: filter[Particle] = filter( lambda x:x.active,  all_particles_above)
            active_above: int = len(list(active_particles_above))

            jump = 1
            rare_jump = 0 if random() <= 0.95 else 2
            
            if self.timealive > choice([4, 2, 10]) and self.pos[1]-jump <= len(self.master)-1 and active_above <= self.max_above+rare_jump:
                particle_above: Particle = self.master[self.pos[1]-jump][self.pos[0]]
                if not(particle_above.active):
                    particle_above.activate()

            if round(self.timealive, 1)%3 == 0:
                self.switch_char()  
            
            if round(timepercmax>75) and not(self.always_active) and self.pos[1]!=len(self.master)-2:
                self.char = self.CHAR3
            
            if active_above < (3 if random() > 50 else 2 if random() < 50 else 1):
                self.char = self.CHAR3
            else:
                self.char = self.CHAR2
                


            if round(self.timealive) > round(self.max_time) and not(self.always_active) or\
                    len(self.master) - self.pos[1] >= self.max_above:
                self.deactivate()
        else:
            self.char = " "

    def __str__(self) -> str:
        return self.char


class ParticleGrid:
    def __init__(self, rows: int, columns: int, pad: int=0, particles_effect: tuple[str, str, str] = ("{", "}", ".")) -> None:
        self.rows = rows
        self.columns = columns
        self.padding = " "*pad
        self.particles_effect = particles_effect
        self.grid: list[list[Particle|int]] = [
        ]
        for _ in range(rows):
            self.grid.append([0]*self.columns)

    def create_particles(self) -> None:
        for i in range(self.rows):
            for j in range(self.columns):
                first_row = False if i!=self.rows-1 else True
                new_particle: Particle = Particle(pos=(j, i), master=self.grid, active=first_row, always_active=first_row, effect=self.particles_effect)
                new_particle.char = self.particles_effect[0 if j%2 else 1]

    def update_particles(self) -> None:
        for row in self.grid[::-1]:
            for column in row:
                column.update()

    def to_string(self) -> str:
        return "\n".join( self.padding+"".join(map(str, row)) for row in self.grid )

    def __str__(self) -> str:
        return self.to_string()
