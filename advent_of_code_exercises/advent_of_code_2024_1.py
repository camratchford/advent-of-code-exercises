
from time import perf_counter_ns
from typing import Callable
from pathlib import Path
from re import split

from advent_of_code_exercises.colors import Colors


ZippedList = list[tuple[int, int]]
ListCompareFuncType = Callable[[ZippedList], int]

timed_results = {}


def measure_runtime(compare_func: ListCompareFuncType):
    def wrapper(*args, **kwargs) -> int:

        before = perf_counter_ns()
        result = compare_func(*args, **kwargs)
        timed = perf_counter_ns() - before

        if not timed_results.get(compare_func.__name__):
            timed_results[compare_func.__name__] = []
        timed_results[compare_func.__name__].append(timed)

        return result

    return wrapper


def split_by_space(string: str):
    return tuple(int(i) for i in split(r"\s+", string))


def load_example_data(file: Path) -> list[tuple[int, ...]]:
    example_data = file.read_text().splitlines()
    return list(map(split_by_space, example_data))


def load_example_data_split(file: Path):
    example_data = file.read_text().splitlines()
    list_a = []
    list_b = []
    for line in example_data:
        a, b = split_by_space(line)
        list_a.append(a)
        list_b.append(b)
    return list_a, list_b


def sort_zip(unsorted_zip: ZippedList) -> (list[int], list[int]):
    """
    I didn't experiment with this one, but I'm sure there's a faster way
    """
    sorted_a = sorted([i[0] for i in unsorted_zip])
    sorted_b = sorted([i[1] for i in unsorted_zip])
    return zip(sorted_a, sorted_b)


def count_occurrences(a, list_b):
    i = 0
    for b in list_b:
        if a == b:
            i += 1
    return i


@measure_runtime
def part_2(list_a: list[int], list_b: list[int]):
    tally = []
    for a in list_a:
        tally.append(a * count_occurrences(a, list_b))
    return sum(tally)


@measure_runtime
def part_2_with_sorted_lists(list_a: list[int], list_b: list[int]):
    tally = []
    sorted_a = sorted(list_a)
    sorted_b = sorted(list_b)
    for a in sorted_a:
        try:
            index = sorted_b.index(a)
        except ValueError:
            continue
        list_b_slice = sorted_b[index:]
        tally.append(a * count_occurrences(a, list_b_slice))
    return sum(tally)


@measure_runtime
def part_1(unsorted_zip: ZippedList) -> int:
    diff = 0
    for a, b in sort_zip(unsorted_zip):
        high = a
        low = b
        if b > a:
            high = b
            low = a
        diff += high - low
    return diff


def highest_minus_lowest(ab: tuple[int, int]) -> int:
    return max(ab) - min(ab)


@measure_runtime
def part_1_but_using_map(unsorted_zip: ZippedList) -> int:
    # I really thought this would be faster, but it's somehow slower than even the naive solution in 'part_1'
    return sum(map(highest_minus_lowest, sort_zip(unsorted_zip)))


@measure_runtime
def part_1_but_a_list_comp(unsorted_zip: ZippedList) -> int:
    return sum([
        a - b if a > b else b - a
        for a, b in sort_zip(unsorted_zip)
    ])


def run_exercise_1():
    # Test if the theory works
    example_file = Path(__file__).parent / "2024_1_example.txt"
    example_data_set = load_example_data(example_file)
    assert part_1_but_using_map(example_data_set) == 11
    assert part_1_but_a_list_comp(example_data_set) == 11
    assert part_1_but_a_list_comp(example_data_set) == 11

    # Run the exercise
    exercise_file = Path(__file__).parent / "2024_1_input.txt"
    exercise_data_set = load_example_data(exercise_file)
    result = 0
    for i in range(1000):
        res_1 = part_1(exercise_data_set)
        res_2 = part_1_but_using_map(exercise_data_set)
        res_3 = part_1_but_a_list_comp(exercise_data_set)
        assert res_1 == res_2 == res_3
        result = res_1

    print(f"{Colors.LIGHT_WHITE}Pert 1 Result is {Colors.GREEN}{result}{Colors.END}")

    list_a, list_b = load_example_data_split(exercise_file)
    part_2_result = part_2(list_a, list_b)
    part_2_result_again = part_2_with_sorted_lists(list_a, list_b)
    assert part_2_result == part_2_result_again

    print()
    print(f"{Colors.LIGHT_WHITE}Part 2 result is {Colors.GREEN}{part_2_result}{Colors.END}")
    print()
    for func_name, time_list in timed_results.items():
        print(
            f"{Colors.CYAN}{func_name}{Colors.LIGHT_WHITE} has an average run time of "
            f"{Colors.GREEN}{sum(time_list) // 1000}{Colors.LIGHT_WHITE} milliseconds."
            f"{Colors.END}"
        )


if __name__ == "__main__":
    run_exercise_1()
