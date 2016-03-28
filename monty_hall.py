import random, argparse, math, locale
from multiprocessing import Pool

locale.setlocale(locale.LC_ALL, "")
rand = random.SystemRandom()

class Result:
    def __init__(self, first=0, switch=0, random=0):
        self.first = first
        self.switch = switch
        self.random = random

class Game:
    def __init__(self):
        """Set up the game. A 0 is a goat, a 1 is the car."""
        self.choices = [0, 0, 1]
        rand.shuffle(self.choices)

    def make_first_choice(self):
        """Choose an index denoting the first choice in the choices."""
        return rand.choice([0, 1, 2])

    def run(self, i):
        """Run the game:

        0. The choices have already been randomly initialised.
        1. Make the first choice and save its result.
        2. Make the switch choice and save its result.
        3. Make the random switch choice value, and save its result.

        The parameter i is required by pool.map to run multiple instances, but
        isn't required in each individual game run."""

        first_choice_index = self.make_first_choice()
        first_choice_value = self.choices[first_choice_index]

        switch_value = 0 if first_choice_value else 1
        random_value = rand.choice([first_choice_value, switch_value])

        return Result(first_choice_value, switch_value, random_value)


def get_num_runs_chunk(num_tries, chunk_size):
    """A generator to help split up the number of tries into manageable chunks
    so that the lsit of results doesn't get too big."""
    if chunk_size >= num_tries:
        yield num_tries
    else:
        num_chunks = math.floor(num_tries / chunk_size)
        remainder = num_tries % chunk_size

        for i in range(num_chunks):
            yield chunk_size

        if remainder != 0:
            yield remainder


def get_args():
    """Get the one optional command-line arg."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num_tries", help="Number of tries.", default="10**3")
    args = parser.parse_args()

    return eval(args.num_tries)


def main():
    num_tries = get_args()
    print(locale.format_string("\nSimulating game %d times.", num_tries, grouping=True))
    chunk_size = 10**4

    game = Game()
    pool = Pool()
    final_result = Result()

    for num_turns in get_num_runs_chunk(num_tries, chunk_size):
        results = pool.map(game.run, range(num_turns))
        for result in results:
            final_result.first += result.first
            final_result.switch += result.switch
            final_result.random += result.random

    print(locale.format_string("\nAlways keeping first resulted in %d cars, or cars %.2f%% of the time.", (final_result.first, final_result.first/num_tries * 100), grouping=True))
    print(locale.format_string("Always switching resulted in %d cars, or cars %.2f%% of the time.", (final_result.switch, final_result.switch/num_tries * 100), grouping=True))
    print(locale.format_string("Randomly switching resulted in %d cars, or cars %.2f%%  of the time.\n", (final_result.random, final_result.random/num_tries * 100), grouping=True))


if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
