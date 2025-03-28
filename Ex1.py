# Напишите программу, в которой в бексонечном цикле пользователь вводит два числа, а программа выводит их сумму.
# Затем программа запрашивает, надо ли завершить ввод. И если пользователь вводит букву "Y" или "y", то происходит
# выход из бесконечного цикла, и программа завершается. При нажатии любой другой клавиши, программа продолжает работу.
# на выходе программы должно быть число округленное до значащих цифр

def input_numbers():
    print('Пожалуйста введите первое число')
    number1 = input()
    print('Пожалуйста введите второе число')
    number2 = input()
    print(float(number1)+float(number2))
    try:
        float(number1) and float(number2)
    except ValueError:
        print ('Необходимо ввести число, десятичная часть отделяется точкой')
        input_numbers()
    else:
        number_sum = float(number1) + float(number2)
        sum_list = list(str(number_sum))
        print(sum_list)
        print(f'длина списка составляет {len(sum_list)} элементов')
        i = -1
        while sum_list[i] == "0" or sum_list[i] == ".":
            print(f"проверяем элемент списка с индексом {i}")
            print(f"нашли ноль или точку. выкидываем элемент {sum_list[i]} с индексом {i}")
            sum_list.pop(i)
            print(sum_list)
        if '.' in sum_list:
            number_sum = float(''.join(sum_list))
        else: number_sum = int(''.join(sum_list))
        print(f'Сумма чисел составит {number_sum}')
        print("Введите Y или y, чтобы завершить ввод, или любой другой символ, чтобы продолжить")
        if str(input()) == 'y':
            print("До свидания")
        else: input_numbers()

input_numbers()
#print(2+3)





