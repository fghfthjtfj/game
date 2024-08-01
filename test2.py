import multiprocessing
import time

def my_function(x):
    time.sleep(2.2)
    return x * x

if __name__ == '__main__':
    # Создание пула процессов с 4 процессами
    with multiprocessing.Pool(processes=4) as pool:
        # Создание списка аргументов для функции
        arguments = [(5,) for _ in range(25)]

        # Запуск нескольких задач в пуле процессов параллельно
        result = pool.map_async(my_function, arguments)

        # Ожидание завершения всех задач
        result.wait()

    # Получение результата
    print(result.get())
