# Advent of Code

But just days 1 and 19


## Installing

### Windows

```powershell
cd ~
git clone https://github.com/camratchford/advent-of-code-exercises
cd advent-of-code-exercises
python -m venv venv
venv\scripts\activate
pip install .
```

### Linux / MacOS

```bash
cd ~
git clone https://github.com/camratchford/advent-of-code-exercises
cd advent-of-code-exercises
python3 -m venv venv
source venv/scripts/activate
pip install .
```


## Running

```shell
# Runs 1000 cycles for each variant, showing you the average completion time of each
# Also displays the result of the difference between the two lists
day1
# Displays how many valid patterns exist in the list of suggested towel stripe patterns
day19
# Draws all valid suggested towel stripe pattern. They look awful.
draw-towels
```