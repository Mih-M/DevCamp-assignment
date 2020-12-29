class InvalidInput(Exception):
    """Raised when input is invalid"""
    pass


class BrickWall:
    """Class used to represent a wall of bricks"""

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._bricks = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        if not (2 <= value <= 100 and value % 2 == 0):
            raise InvalidInput('Input for rows should be an even number between 2 and 100.')

        self._rows = value

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, value):
        if not (2 <= value <= 100 and value % 2 == 0):
            raise InvalidInput('Input for columns should be an even number between 2 and 100.')

        self._cols = value

    def show_brick(self, row_idx, col_idx):
        """Returns the value of the position with given coordinates from the bricks matrix."""

        return self._bricks[row_idx][col_idx]

    def change_brick(self, row_idx, col_idx, value):
        """Changes the value of the position with given coordinates from the bricks matrix."""

        self._bricks[row_idx][col_idx] = value

    def fill_bricks_from_console(self):
        """Fills the wall with bricks as given from the console."""

        message = 'Please enter brick lines from start.'

        while True:
            try:
                bricks = []
                for _ in range(self.rows):
                    row = self._read_line_from_console()
                    bricks.append(row)

                self._bricks = bricks
                break

            except InvalidInput as exc:
                print(exc, message)

            except ValueError:
                print('Bricks can be only integers.', message)

        if not self.validate_bricks():
            print('Invalid input for bricks positions. Please enter brick lines from start.')
            return self.fill_bricks_from_console()
        return

    def _read_line_from_console(self):
        """Reads a line of input from the console and returns a list of integers
           or raises exception if input is invalid."""

        row = list(map(int, input().split()))

        if len(row) != self.cols:
            raise InvalidInput(f'Input should contain {self.rows} lines of '
                               f'{self.cols} positive numbers separated by single space.')
        return row

    def validate_bricks(self):
        """Checks if bricks values meet all requirements. Returns True or False."""

        return self._validate_bricks_are_only_pairs_of_consecutive_numbers() \
               and self._validate_all_halves_of_bricks_are_connected()

    def _validate_bricks_are_only_pairs_of_consecutive_numbers(self):
        """Checks if each brick takes exactly 2 positions and all numbers are consecutive.
           Returns True or False."""

        unique_numbers = set([num for row in self._bricks for num in row])
        count_bricks = self.rows * self.cols / 2

        return len(unique_numbers) == count_bricks and min(unique_numbers) == 1 and max(unique_numbers) == count_bricks

    def _is_position_valid(self, row_idx, col_idx):
        """Checks if given position is inside the brick matrix. Returns True or False."""

        return 0 <= row_idx < self.rows and 0 <= col_idx < self.cols

    def _validate_all_halves_of_bricks_are_connected(self):
        """Checks if all pairs of numbers are connected. Returns True or False."""

        directions = [
            (0, 1),
            (1, 0)
        ]

        # set to keep values for all positions that have been already checked.
        checked = set()

        for ri in range(self.rows):
            for ci in range(self.cols):

                if (ri, ci) in checked:
                    continue

                # variable to keep True or False statement for matching numbers.
                match_found = False

                for i in range(len(directions)):
                    # coordinates of neighbour's position.
                    neighbour_ri = ri + directions[i][0]
                    neighbour_ci = ci + directions[i][1]

                    if self._is_position_valid(neighbour_ri, neighbour_ci):

                        if self.show_brick(ri, ci) == self.show_brick(neighbour_ri, neighbour_ci):
                            match_found = True
                            checked.add((neighbour_ri, neighbour_ci))
                            break

                if not match_found:
                    return False

        return True

    def display_wall(self):
        """Returns a string representation of the wall with borders between bricks."""

        def format_value(v):
            """Adds space in front of value to match the length of the biggest number in the wall."""

            # variable for the length of the given number.
            num_len = len(str(v))
            return f'{" " * (max_num_len - num_len)}{v}'

        # variable for the length of the biggest number in the wall.
        max_num_len = len(str(int(self.rows * self.cols / 2)))

        # variable to keep the separator between bricks.
        sep = '* '
        # variable to keep the empty space inside a brick.
        empty = '  '
        # variable to keep the empty space needed between separators.
        space_sep = ' ' * int(max_num_len / 2)
        # variable to keep the empty space needed between number and separator.
        space_num = '  ' if max_num_len % 2 == 0 else ' '

        # variable to keep the output.
        output = f'{(sep + space_sep) * (self.cols * 2 + 1)}\n'

        for ri in range(self.rows):
            first_row = sep
            second_row = sep
            for ci in range(self.cols):
                if ci != self.cols - 1 and self.show_brick(ri, ci) == self.show_brick(ri, ci + 1):
                    first_row += f'{format_value(self.show_brick(ri, ci))}{space_num}{empty}'
                else:
                    first_row += f'{format_value(self.show_brick(ri, ci))}{space_num}{sep}'

                if ri != self.rows - 1 and self.show_brick(ri, ci) == self.show_brick(ri + 1, ci):
                    second_row += f'{space_sep}{empty}{space_sep}{sep}'
                else:
                    second_row += f'{space_sep}{sep}{space_sep}{sep}'
            output += first_row.rstrip() + '\n'
            output += second_row.rstrip() + '\n'

        return output.rstrip()

    def __str__(self):
        return '\n'.join(' '.join(map(str, row)) for row in self._bricks)


def create_wall():
    """Creates new instance of class BrickWall by accepting values from the console."""

    while True:
        try:
            rows, cols = (map(int, input().split()))
            wall = BrickWall(rows, cols)
            break

        except InvalidInput as exc:
            print(exc)

        except ValueError:
            print('Input should be two even numbers separated by single space.')

    return wall


def combine_walls(f_wall: BrickWall, s_wall: BrickWall):
    """Fills the second wall with bricks, according to the bricks from the first wall."""

    # variables to keep the count of rows and columns in both matrices.
    rows_count = f_wall.rows
    cols_count = f_wall.cols

    # variable to keep track of used bricks.
    curr_brick = 1

    for ri in range(0, rows_count - 1, 2):
        for ci in range(0, cols_count - 1, 2):

            s_wall.change_brick(ri, ci, curr_brick)

            if f_wall.show_brick(ri, ci) == f_wall.show_brick(ri, ci + 1) \
                    or f_wall.show_brick(ri + 1, ci) == f_wall.show_brick(ri + 1, ci + 1):

                s_wall.change_brick(ri + 1, ci, curr_brick)
                s_wall.change_brick(ri, ci + 1, curr_brick + 1)
                s_wall.change_brick(ri + 1, ci + 1, curr_brick + 1)

            else:
                s_wall.change_brick(ri, ci + 1, curr_brick)
                s_wall.change_brick(ri + 1, ci, curr_brick + 1)
                s_wall.change_brick(ri + 1, ci + 1, curr_brick + 1)

            curr_brick += 2


# variable to keep the instance of the first wall.
first_layer = create_wall()
first_layer.fill_bricks_from_console()

# variable to keep the instance of the second wall.
second_layer = BrickWall(first_layer.rows, first_layer.cols)

combine_walls(first_layer, second_layer)

print(second_layer)
print(second_layer.display_wall())
