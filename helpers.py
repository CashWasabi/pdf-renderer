from datetime import datetime


def timed(func, args, kwargs) -> None:
    start = datetime.now()
    func(args, kwargs)
    print(datetime.now() - start)


def read_file(filepath) -> str:
    with open(filepath) as open_file:
        return open_file.read()


def write_file(filepath, data) -> None:
    with open(filepath, 'w') as write_file:
        write_file.write(data)


def write_pdf(filepath, data) -> None:
    with open(filepath, 'wb') as write_file:
        write_file.write(data)
