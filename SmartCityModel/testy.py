from ui import show_menu

sensors = {
    "ghjkjhgfd": 1,
    "str": 2,
    "uuuu": 3
}
def hh():
    ops=[(ke,v) for ke,v in sensors.items()]
    k=show_menu(ops, input, print)
    print(f"'{k}'")

lis=["t", "k", "l"]
homes=[(i, home) for i,home in enumerate(lis, 1)]

if __name__=='__main__':
    hh()