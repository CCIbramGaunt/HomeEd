# Используйте циклы, чтобы вывести на консоль фигуру
# *******
#  *   *
#   * *
#    *
#   * *
#  *   *
# *******
import time
def figure():
    time_start = time.time()
    star_string_list = []
    for row in range(1, 14):
        if row == 1 or row == 13:
            for column in range(1, 8):
                star_string_list.append('*')
            star_string_list.append('\n')
        elif row == 3 or row == 11:
            for column in range(1, 8):
                if column != 2 and column != 6:
                    star_string_list.append(' ')
                else: star_string_list.append('*')
            star_string_list.append("\n")
        elif row == 5 or row == 9:
            for column in range(1, 8):
                if column != 3 and column != 5:
                    star_string_list.append(' ')
                else:
                    star_string_list.append('*')
            star_string_list.append("\n")
        elif row == 7:
            for column in range(1, 8):
                if column != 4:
                    star_string_list.append(' ')
                else:
                    star_string_list.append('*')
            star_string_list.append("\n")
    print(str(''.join(star_string_list)))
    time_end = time.time()
    print(time_end - time_start)
figure()
