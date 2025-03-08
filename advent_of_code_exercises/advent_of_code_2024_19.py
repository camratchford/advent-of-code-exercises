from pathlib import Path
from re import compile, Pattern
from itertools import combinations_with_replacement, filterfalse
from bisect import bisect_right

from advent_of_code_exercises.colors import Colors


def load_example_data(file: Path):
    wanted_pattern_list = file.read_text().splitlines()
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
    matches = [i for i in compiled_regex.findall(pattern) if i != '' and i != pattern]
    return matches



def try_combinations(subpattern_list, match_pattern):
    subpattern_list = sorted(subpattern_list, key=len, reverse=True)
    meta_patterns = [sub for sub in subpattern_list if len(sub) >= 2]
    single_patterns = ['w', 'u', 'b', 'r', 'g']
    meta_substitutions = {k: [] for k in meta_patterns}
    for meta in meta_patterns:
        list_slice = bisect_right(meta_patterns, meta)
        meta_substitutions[meta] = split_by_subpattern(meta_patterns[list_slice:], meta)

    combination_count = 0
    for s in meta_patterns:

        combination_count += 1      # The meta pattern
        combination_count += len(s) # The single-letter patterns
        if s in meta_substitutions.keys():
            combination_count += len(meta_substitutions[s]) # Every sub-pattern substitution of meta

    return combination_count


def test_towel_permutations(valid_pattern_list, valid_designs):
    valid_combination = 0
    for design in valid_designs:
        subpatterns_found = split_by_subpattern(valid_pattern_list, design)
        if len(subpatterns_found):
            found = try_combinations(subpatterns_found, design)
            valid_combination += found
    return valid_combination


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
    print(example_result)

    # exercise_data_file = Path(__file__).parent / "2024_19_input.txt"
    # exercise_valid_patterns, exercise_wanted_patterns = load_example_data(exercise_data_file)
    # valid_designs = get_valid_designs(exercise_valid_patterns, exercise_wanted_patterns)
    # exercise_result = test_towel_permutations(exercise_valid_patterns, valid_designs)
    #
    # print(f"{Colors.LIGHT_WHITE}Result is {Colors.GREEN}{exercise_result}{Colors.END}")


if __name__ == "__main__":
    run_exercise_19()
