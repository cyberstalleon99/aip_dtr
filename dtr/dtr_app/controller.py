from aip import log_in, log_out, arrival, departure, _main

def exit():
    pass

def key_switcher(key):

    switcher = {
        # Esc
        27: exit,
        # 1
        49: log_in,
        # 2
        50: log_out,
        # 3
        51: arrival,
        # 4
        52: departure
    }

    return switcher.get(key)

def main():
    key, name = _main()
    print(key)
    print(name)
    # pass
    # Get the returned name and which key pressed
    # key, name = aip.get_name()

    # key_switcher(key%256)(name)


if __name__ == "__main__":
    main()