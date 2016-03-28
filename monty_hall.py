import random, argparse, math
from multiprocessing import Pool

rand = random.SystemRandom()

class Result:
    def __init__(self, first=0.0, switch=0.0, r=0.0):
        self.first = first
        self.switch = switch
        self.random = r

class Game:
    def __init__(self):
        """Sets up the game. A 0 in the choice is a goat, a 1 is the car."""
        self.choices = [0, 0, 1]
        rand.shuffle(self.choices)

    def make_first_choice(self):
        """Choose an index denoting the first choice in the choices."""
        return rand.choice([0, 1, 2])

    def run(self, i):
        first_choice_index = self.make_first_choice()

        first_choice_value = self.choices[first_choice_index]
        switch_value = 0 if first_choice_value else 1
        if rand.choice([True, False]):
            random_value = switch_value
        else:
            random_value = first_choice_value

        return Result(first_choice_value, switch_value, random_value)


def main():
    num_tries = get_args()
    chunk_size = 10**6

    game = Game()
    pool = Pool()
    final_result = Result()

    for num_turns in get_num_runs_chunk(num_tries, chunk_size):
        results = pool.map(game.run, range(num_turns))
        for result in results:
            final_result.first += result.first
            final_result.switch += result.switch
            final_result.random += result.random

    print("Always keeping first resulted in {} cars, or cars {0:.2f}%% of the time.".format(final_result.first, final_result.first/num_tries * 100))
    print("Always switching resulted in {} cars, or cars {0:.2f}%% of the time.".format(final_result.switch, final_result.switch/num_tries * 100))
    print("Randomly switching resulted in {} cars, or cars {0:.2f}%% of the time.".format(final_result.random, final_result.random/num_tries * 100))


def get_args():
    """Get the one positional command-line arg."""
    parser = argparse.ArgumentParser()
    parser.add_argument("num_tries", help="Number of tries.")
    args = parser.parse_args()

    return eval(args.num_tries)


def get_num_runs_chunk(num_tries, chunk_size):
    """A generator for yielding the size of each number of parallel runs.
    This is done to prevent the memory footprint from the number of results
    getting too big."""
    if chunk_size >= num_tries:
        yield num_tries
    else:
        num_chunks = math.floor(num_tries / chunk_size)
        remainder = num_tries % chunk_size

        for i in range(num_chunks):
            yield chunk_size

        if remainder != 0:
            yield remainder

if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
