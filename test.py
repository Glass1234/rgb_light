import threading, time
import multiprocessing
import concurrent.futures


def work(n):
    for i in range(n):
        continue


def foo(n):
    start = time.time()
    for i in range(1):
        work(50_000_000)
    end = time.time() - start
    print(f'[{n}]', end)
    return True


ns = []


def main():
    for i in range(100):
        ns.append(i)

    st = time.time()

    th_name = threading.current_thread().name
    print(f'{th_name}: запущен...')
    with concurrent.futures.ProcessPoolExecutor(max_workers=10) as ex:
        res = ex.map(foo, ns)
    results = list(res)

    print(f'{th_name}: результаты => {results}')

    en = time.time() - st
    print(en)


if __name__ == "__main__":
    main()
