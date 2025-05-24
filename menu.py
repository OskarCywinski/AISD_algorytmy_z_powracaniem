import argparse
import sys
import os
from graph import Graph_Matrix

sys.setrecursionlimit(10**6)

def help():
    print("\nCommands:")
    print("  Help     > Show this message")
    print("  Print    > Print the graph")
    print("  Euler    > Check if a Eulerian cycle exists")
    print("  Hamilton > Check if a Hamiltonian cycle exists")
    print("  Export   > Export the graph to tickzpicture")
    print("  Exit     > Exits the program\n")

def print_graph():
    global graph
    graph.display()

def euler():
    global graph
    print(graph.fleury_eulerian_cycle())

def hamilton():
    global graph
    print(graph.roberts_flores_hamiltonian_cycle())

def export():
    global graph
    print(graph.export_to_tikz())

def exit():
    print("Exiting the program.")
    sys.exit(0)

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
        if nodes < 3:
            print("Liczba węzłów musi być większa od 2.")
            continue
        break
    except:
        print("Invalid input. Please enter an integer.")

graph = Graph_Matrix(nodes)

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
    graph.generate_hamilton_graph(nodes, saturation)

if args.non_hamilton:
    saturation = 50
    graph.generate_non_hamilton_graph(nodes, saturation)


while True:
    print("\nNode Count>")
    action = input("Action> ").strip().lower()
    match action:
        case "help" | "print" | "euler" | "hamilton" | "export" | "exit":
            globals()[action.replace(" ", "_").replace("-","_")]() if action != "print" else print_graph()
        case _:
            print("Invalid command. Type 'help' for a list of available commands.")
            print(action)


