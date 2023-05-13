import sys
from SB_CommonTypes import Point
from SB_Data import Field
from SB_Ships import NavyData

# from SB_Player import Player
# from SB_Player import PlayerHuman
# from SB_Player import PlayerComputer

class CoordsError(ValueError):
    pass

class CoordsError_Format(CoordsError):
    pass

class CoordsError_Format_Count(CoordsError_Format):
    pass

# class CoordsError_Format_NoFloat(CoordsError_Format):
#     pass

class CoordsError_OutOfRange(CoordsError):
    pass

class CoordsError_AlreadyUsed(CoordsError):
    pass
class IOController:
    def __init__(self):
        pass

    def show_message(self, msg: str) -> None:
        raise Exception("IOController.show_message: Abstract error!")
    def ask_menu(self, caption, items, default_item_index=0):
        raise Exception("IOController.ask_menu: Abstract error!")

    def ask_coords(self, caption, enemy_field) -> Point:
        raise Exception("IOController.ask_coords: Abstract error!")

    def show_field(self, navy_data: NavyData, is_show_full: bool):
        raise Exception("IOController.show_enemy_field: Abstract error!")

    def show_navy_data_usage_field(self, navy_data: NavyData):
        raise Exception("IOController.show_navy_data_usage_field: Abstract error!")

class IOControllerConsole(IOController):

    def show_message(self, msg: str) -> None:
        print(msg)
    def ask_menu(self, caption, items, default_item_index=0):
        if len(items) == 0:
            raise ValueError("IOControllerConsole.ask_menu: Wrong len(items)")

        print(caption)
        for curr_item_index, curr_item in enumerate(items):
            print(f"{curr_item_index + 1}. {curr_item}")

        answer = input("Your choice: ")
        if answer.isdigit():
            selected_num = int(answer)
            if selected_num > len(items):
                selected_num = default_item_index + 1
        else:
            selected_num = default_item_index + 1

        if selected_num > len(items):
            selected_num = 1
        selected_index = selected_num - 1

        print(f"You selected: {selected_num}. {items[selected_index]}")

        return selected_index

    def ask_coords(self, caption, enemy_field) -> Point:
        while True:
            new_point = None
            try:
                coord_s = input(caption)
                if coord_s.lower() in ['exit', 'quit']:
                    sys.exit(0)

                coord_values = coord_s.split()
                # if len(coord_values) < 2:
                #     # print("Wrong coordinates - less then two numbers. Re-enter your coordinates!")
                #     raise CoordsError_Format_Count
                # elif not coord_values[0].isnumeric() or not coord_values[1].isnumeric():
                #     # print("Wrong coordinates - not a number. Re-enter your coordinates!")
                #     raise CoordsError_Format_NoFloat
                # else:
                #     a_ix = int(coord_values[0]) - 1
                #     a_iy = int(coord_values[1]) - 1
                #     new_point = Point(a_ix, a_iy)
                #
                #     if not enemy_field.is_point_in_field(new_point):
                #         # print("Wrong coordinates - point is out of range. Re-enter your coordinates!")
                #         raise CoordsError_OutOfRange
                #     elif enemy_field.is_point_used(new_point):
                #         # print("Wrong coordinates - point is already used. Re-enter your coordinates!")
                #         raise CoordsError_AlreadyUsed
                if len(coord_values) < 2:
                    # print("Wrong coordinates - less then two numbers. Re-enter your coordinates!")
                    raise CoordsError_Format_Count
                else:
                    a_ix = int(coord_values[0]) - 1
                    a_iy = int(coord_values[1]) - 1
                    new_point = Point(a_ix, a_iy)

                    if not enemy_field.is_point_in_field(new_point):
                        # print("Wrong coordinates - point is out of range. Re-enter your coordinates!")
                        raise CoordsError_OutOfRange
                    elif enemy_field.is_point_used(new_point):
                        # print("Wrong coordinates - point is already used. Re-enter your coordinates!")
                        raise CoordsError_AlreadyUsed
                    # else:
                    #     return new_point
            except CoordsError_Format_Count:
                print("Wrong coordinates - less then two values. Re-enter your coordinates!")
            except CoordsError_OutOfRange:
                print("Wrong coordinates - point is out of range. Re-enter your coordinates!")
            except CoordsError_AlreadyUsed:
                print("Wrong coordinates - point is already used. Re-enter your coordinates!")
            except ValueError:
                print("Wrong coordinates - not a number. Re-enter your coordinates!")
            else:
                return new_point

    def show_field(self, navy_data: NavyData, is_show_full: bool):
        is_draw_nums = max(navy_data.usage_field.size_x, navy_data.usage_field.size_x) <= 9

        def get_symbol_of_field(x, y):
            is_hit = navy_data.hit_field.get_field_value(x, y)
            is_ship = navy_data.usage_field.get_field_value(x, y) > 0
            if is_hit and is_ship:
                return "X"
            elif is_hit and not is_ship:
                return "T"
            elif is_show_full and is_ship and not is_hit:
                return "■"
            else:
                return 0

        if is_draw_nums:
            col_nums = [1 + curr_col_index for curr_col_index in range(navy_data.usage_field.size_x)]
            col_nums_s = map(str, col_nums)
            curr_line = " |" + "|".join(col_nums_s) + '|'
            print(curr_line)

        for curr_row_index in range(navy_data.usage_field.size_y):
            field_values = \
                [get_symbol_of_field(x, curr_row_index) for x in range(navy_data.usage_field.size_x)]
            field_values_s = map(str, field_values)
            curr_line = "|".join(field_values_s)
            if is_draw_nums:
                curr_line = f"{1 + curr_row_index}|" + curr_line
            print(curr_line)

        print()

    def show_fields(self, navy_datas, player_names, selected_player_index: int, player_human_index: int):
        def get_symbol_of_field(navy_data, player_index, x, y):
            # is_show_full = player_index in [-1, player_human_index]
            is_show_full = player_human_index in [-1, player_index]
            is_hit = navy_data.hit_field.get_field_value(x, y)
            is_ship = navy_data.usage_field.get_field_value(x, y) > 0
            if is_hit and is_ship:
                return "X"
            elif is_hit and not is_ship:
                return "T"
            elif is_show_full and is_ship and not is_hit:
                return "■"
            else:
                return 0

        size_x = navy_datas[0].usage_field.size_x
        size_y = navy_datas[0].usage_field.size_y
        is_draw_nums = size_x <= 9

        offset = 12

        # print("Current state:")

        #player names
        curr_line = ""
        for curr_player_index, curr_player_name in enumerate(player_names):
            if curr_player_index == selected_player_index:
                curr_mark = ">>>"
            else:
                curr_mark = ""
            curr_width = 4 * size_x + 1
            curr_format_str = "{:" + str(curr_width) + "s}"
            curr_line += curr_format_str.format(curr_mark + curr_player_name) + offset * " "
        print(curr_line)

        # num row
        if is_draw_nums:
            curr_line = ""
            for curr_player_index, curr_navy_data in enumerate(navy_datas):
                col_nums = [1 + curr_col_index for curr_col_index in range(curr_navy_data.usage_field.size_x)]
                col_nums_s = map(str, col_nums)
                curr_line += "  | " + " | ".join(col_nums_s) + " " * offset
            print(curr_line)

        # rows
        for curr_row_index in range(size_y):
            curr_line = ""
            for curr_player_index, curr_navy_data in enumerate(navy_datas):
                field_values = [get_symbol_of_field(curr_navy_data, curr_player_index, x, curr_row_index)
                                for x in range(curr_navy_data.usage_field.size_x)]
                field_values_s = map(str, field_values)

                if is_draw_nums:
                    curr_line_num = f"{1 + curr_row_index} | "
                else:
                    curr_line_num = ""

                curr_line += curr_line_num + " | ".join(field_values_s)

                    # curr_line = f"{1 + curr_row_index}|" + curr_line
                curr_line += " " * offset
            print(curr_line)

        print()

    def show_navy_data_usage_field(self, navy_data: NavyData):
        for curr_row_index in range(navy_data.usage_field.size_y):
            curr_line = ""
            for curr_col_index in range(navy_data.usage_field.size_x):
                curr_line = curr_line + f" {navy_data.usage_field.get_field_value(curr_col_index, curr_row_index):3d}"
            print(curr_line)