import random

def setup_ships():
    sample_pos = [
        {"ship":"Carrier","locs":[[1,3],[1,4],[1,5],[1,6],[1,7]]},
        {"ship":"Battleship","locs":[[4,3],[5,3],[6,3],[7,3]]},
        {"ship":"Submarine","locs":[[4,8],[5,8],[6,8]]},
        {"ship":"Cruiser","locs":[[1,0],[2,0],[3,0]]},
        {"ship":"Destroyer","locs":[[1,1],[1,2]]}
    ]
    return sample_pos

def rand_space(missile_list):
    loc = [random.randrange(10), random.randrange(10)]
    while loc in missile_list:
        loc = [random.randrange(10), random.randrange(10)]
    return(loc)