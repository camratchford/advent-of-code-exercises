import logging

from time import perf_counter_ns
from typing import Callable
from pathlib import Path
from re import split

from advent_of_code_exercises.colors import Colors


ZippedList = list[tuple[int, int]]
ListCompareFuncType = Callable[[ZippedList], int]

timed_results = {}


def measure_runtime(compare_func: ListCompareFuncType):
    def wrapper(unzipped_list: ZippedList) -> int:

        before = perf_counter_ns()
        result = compare_func(unzipped_list)
        timed = perf_counter_ns() - before

        if not timed_results.get(compare_func.__name__):
            timed_results[compare_func.__name__] = []
        timed_results[compare_func.__name__].append(timed)

        return result

    return wrapper


def split_by_space(string: str):
    return tuple(int(i) for i in split(r"\s+", string))


def load_example_data(file: Path) -> str:
    with open(str(file), "r") as example_file:
        example_data = example_file.read()
        return list(map(split_by_space, example_data.splitlines()))


def sort_zip(unsorted_zip: ZippedList) -> (list[int], list[int]):
    """
    I didn't experiment with this one, but I'm sure there's a faster way
    """
    sorted_a = sorted([i[0] for i in unsorted_zip])
    sorted_b = sorted([i[1] for i in unsorted_zip])
    return zip(sorted_a, sorted_b)


@measure_runtime
def main(unsorted_zip: ZippedList) -> int:
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
def main_but_using_map(unsorted_zip: ZippedList) -> int:
    # I really thought this would be faster, but it's somehow slower than even the naive solution in 'main'
    return sum(map(highest_minus_lowest, sort_zip(unsorted_zip)))


@measure_runtime
def main_but_a_list_comp(unsorted_zip: ZippedList) -> int:
    return sum([
        a - b if a > b else b - a
        for a, b in sort_zip(unsorted_zip)
    ])


def run_exercise_1():


    # Test if the theory works
    example_file = Path(__file__).parent / "2024_1_example.txt"
    example_data_set = load_example_data(example_file)
    assert main_but_using_map(example_data_set) == 11
    assert main_but_a_list_comp(example_data_set) == 11
    assert main_but_a_list_comp(example_data_set) == 11

    # Run the exercise
    exercise_file = Path(__file__).parent / "2024_1_input.txt"
    exercise_data_set = load_example_data(exercise_file)
    result = 0
    for i in range(1000):
        res_1 = main(exercise_data_set)
        res_2 = main_but_using_map(exercise_data_set)
        res_3 = main_but_a_list_comp(exercise_data_set)
        assert res_1 == res_2 == res_3
        result = res_1

    print(f"{Colors.LIGHT_WHITE}Result is {Colors.GREEN}{result}{Colors.END}")
    for func_name, time_list in timed_results.items():
        print(
            f"{Colors.CYAN}{func_name}{Colors.LIGHT_WHITE} has an average run time of "
            f"{Colors.GREEN}{sum(time_list) // 1000}{Colors.LIGHT_WHITE} milliseconds."
            f"{Colors.END}"
        )


if __name__ == "__main__":
    run_exercise_1()
