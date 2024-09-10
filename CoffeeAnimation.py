from time import sleep
from particlesystem import *
from coffeecup import coffee_ascii_big_blocks

def add_spaces_to_ascii_art(ascii_art: str, spaces: int) -> str:
    return '\n'.join(map(lambda x:f'{' '*spaces}{x}', ascii_art.split('\n')))

def main() -> None:
    clear()
    ascii_padding: int = 2
    coffee_ascii = add_spaces_to_ascii_art(coffee_ascii_big_blocks, ascii_padding)
    pad = (coffee_ascii.split("\n")[0].count(" ")//2)+ascii_padding-(9*ascii_padding//20)
    particle_grid = ParticleGrid(18, 52, pad=pad, particles_effect=fire_effect)
    particle_grid.create_particles()

    while True:
        clear()
        print(particle_grid.to_string())
        print(f"{BRIGHT_WHITE}{coffee_ascii}{END}")
        particle_grid.update_particles()
        sleep(0.1)

if __name__ == "__main__":
    main()
