import argparse
import sys
import os

sys.setrecursionlimit(10**6)

def help():
    print("\nCommands:")
    print("  Help   > Show this message")
    print("  Print  > Print the graph")
    print("  Find   > Check if an edge exists")
    print("  DFS    > Perform Depth First Search")
    print("  BFS    > Perform Breadth First Search")
    print("  Kahn   > Sort the graph using Kahn's algorithm")
    print("  Tarjan > Sort the graph using Tarjan's algorithm")
    print("  Export > Export the graph to tickzpicture")
    print("  Exit   > Exits the program\n")

parser = argparse.ArgumentParser()
parser.add_argument('--hamilton', action='store_true')
parser.add_argument('--non-hamilton', action='store_true')
args = parser.parse_args()

selected_args = sum([args.hamilton, args.non_hamilton])

if selected_args == 0:
    print("Błąd: Musisz podać jeden z argumentów: --user-provided lub --generate")
    sys.exit(1)
elif selected_args > 1:
    print("Błąd: Nie możesz podać obu argumentów jednocześnie. Wybierz tylko jeden z: --hamilton lub --non-hamilton")
    sys.exit(1)


while True:
    try:
        nodes = int(input("nodes> "))
        if args.hamilton and nodes < 3:
            print("Liczba węzłów musi być większa od 2.")
            continue
        if args.non_hamilton and nodes < 2:
            print("Liczba węzłów musi być większa od 1.")
            continue
        break
    except:
        print("Invalid input. Please enter an integer.")

if args.hamilton:
    while True:
        try:
            saturation = int(input("saturation> "))
            if saturation not in [30,70]:
                print("Saturation must be equal to 30 or 70.")
                continue
            break
        except:
            print("Invalid input. Please enter an integer.")

if args.non_hamilton:
    saturation = 50