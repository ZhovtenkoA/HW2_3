import time

# Синхронная версия
def factorize(numbers):
    def factorize_number(number):
        factors_list = []
        for i in range(1, number + 1):
            if number % i == 0:
                factors_list.append(i)
        return factors_list

    start_time = time.time()

    factors = []
    for number in numbers:
        factors.append(factorize_number(number))

    end_time = time.time()
    execution_time = end_time - start_time

    return factors, execution_time


numbers = [128, 255, 99999, 10651060]

factors_sync, execution_time_sync = factorize(numbers)
print("Синхронная версия:")
assert factors_sync[0] == [1, 2, 4, 8, 16, 32, 64, 128]
assert factors_sync[1] == [1, 3, 5, 15, 17, 51, 85, 255]
assert factors_sync[2] == [1, 3, 9, 41, 123,
                               271, 369, 813, 2439, 11111, 33333, 99999]
assert factors_sync[3] == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158,
                               304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]

print("Проверка завершена. Результаты верны.")
print("Результаты:", factors_sync)
print("Время выполнения:", execution_time_sync)
