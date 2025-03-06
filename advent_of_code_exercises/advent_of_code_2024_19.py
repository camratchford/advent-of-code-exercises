from pathlib import Path
from re import compile, Pattern
from itertools import combinations_with_replacement

from advent_of_code_exercises.colors import Colors


def load_example_data(file: Path):
    wanted_pattern_list = file.read_text().splitlines()
    # Uncertain if sorting from largest to smallest is *all* I have to do
    # I feel that there's more required more edge cases
    valid_pattern_list = sorted(
        wanted_pattern_list.pop(0).split(", "),
        key=len,
        reverse=True
    )
    wanted_pattern_list.pop(0)
    return valid_pattern_list, wanted_pattern_list


def generate_regex(valid_pattern_list):
    regex = "|".join([fr"{i}" for i in valid_pattern_list])
    return compile(regex)


def is_valid_pattern(regex: Pattern, towel_pattern: str):
    remained = regex.sub("", towel_pattern)
    # Casting to bool is unnecessary, but reads better
    return not bool(len(remained))


def count_valid_patterns(valid_pattern_list, wanted_pattern_list):
    compiled_regex = generate_regex(valid_pattern_list)
    return len([i for i in wanted_pattern_list if is_valid_pattern(compiled_regex, i)])


def get_valid_designs(valid_pattern_list, wanted_pattern_list):
    compiled_regex = generate_regex(valid_pattern_list)
    return [i for i in wanted_pattern_list if is_valid_pattern(compiled_regex, i)]


def split_by_subpattern(valid_pattern_list, pattern):
    compiled_regex = compile("|".join([fr"{i}" for i in valid_pattern_list]))
    matches = [i for i in compiled_regex.findall(pattern) if i != '']

    return matches


def try_n_combination(subpattern_list, match_pattern, n):

    for combination in combinations_with_replacement(subpattern_list, n):
        if combination:
            attempted_match = "".join(list(combination))
            if attempted_match == match_pattern:
                yield list(combination)


def try_combinations(subpattern_list, match_pattern):
    results = []
    for i in range(2, len(subpattern_list)+1):
        output = []
        for c in try_n_combination(subpattern_list, match_pattern, i):
            output.append(c)

        for another_list in output:
            if len(another_list):
                results.extend(another_list)
    return output



def test_towel_permutations(valid_pattern_list, valid_designs):
    valid_combination = []
    for design in valid_designs:
        subpatterns_found = split_by_subpattern(valid_pattern_list, design)
        if len(subpatterns_found):
            found = try_combinations(subpatterns_found, design)
            if found is not None:
                valid_combination.append(list(found))
    return len([i for i in valid_combination if i])


def render_towel(sub_pattern: str):
    full_block = '\N{FULL BLOCK}'
    color_map = {
        "w": Colors.LIGHT_WHITE,
        "u": Colors.BLUE,
        "b": Colors.BLACK,
        "r": Colors.RED,
        "g": Colors.GREEN
    }
    towel = ""
    for char in sub_pattern:
        towel += f"{color_map[char]}{full_block}{Colors.END}"

    return towel


def draw_towels():
    exercise_data_file = Path(__file__).parent / "2024_19_input.txt"
    exercise_valid_patterns, exercise_wanted_patterns = load_example_data(exercise_data_file)
    patterns = get_valid_designs(exercise_valid_patterns, exercise_wanted_patterns)
    for pattern in patterns:
        towel_stack = ""
        for sub_pattern in split_by_subpattern(exercise_valid_patterns, pattern):
            towel_stack += "".join([render_towel(i) for i in sub_pattern])
            towel_stack += "   "
        print(towel_stack)
        print(towel_stack)
        print(towel_stack)


def run_exercise_19():

    example_data_file = Path(__file__).parent / "2024_19_example.txt"
    example_valid_patterns, example_wanted_patterns = load_example_data(example_data_file)
    example_result = test_towel_permutations(example_valid_patterns, example_wanted_patterns)
    assert example_result == 6

    exercise_data_file = Path(__file__).parent / "2024_19_input.txt"
    exercise_valid_patterns, exercise_wanted_patterns = load_example_data(exercise_data_file)
    valid_designs = get_valid_designs(exercise_valid_patterns, exercise_wanted_patterns)
    exercise_result = test_towel_permutations(exercise_valid_patterns, valid_designs)

    print(f"{Colors.LIGHT_WHITE}Result is {Colors.GREEN}{exercise_result}{Colors.END}")


if __name__ == "__main__":
    run_exercise_19()
