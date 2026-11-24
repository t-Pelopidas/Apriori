from types import NoneType

def pretty_print(C: list, title: str | None = None, f: str | None = None):
    if not type(f) == NoneType:
        with open(f, 'a') as f:
            if title:
                print(title, file = f)
            for name, c in C:
                print(name, c, file = f)
    else:
        if title:
            print(title)
        for name, c in C:
            print(name, c)

def print_opts():
    print('''
          ---Options---
          i: insert items, separated by a comma
          h: show this menu
          a: print all the valid items
          q: quit
          ''')

def get_items():
    items = input("Input a list of items: ")
    return items

def handle_opt(dataset_item_labels):
    opt = input(">>: ")
    match opt:
        case 'h':
            print_opts()
            return
        case 'i':
            return get_items()
        case 'a':
            for item in dataset_item_labels:
                print(item)
            return
        case 'q':
            print('Quitting')
            return -1
        case _:
            print("Invalid option (input 'h' for help)")
            return

