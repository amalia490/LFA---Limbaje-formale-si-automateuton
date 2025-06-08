def inputFile(filename):

     # Dictionar pentru a stoca fiecare sectiune
    sections = {'symbols': [], 'tape': [], 'tranzitii': [], 'stari': []}
    current = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line == "End":
                current = None
                continue

            if line.endswith(':'):
                current = line[:-1]
                continue

            if current:
                sections[current].append(line)

    return sections


def turingM(sections):
    tape = sections['tape'][0].split()
    head = 0
    stare = sections['stari'][0]
    final_stari = {sections['stari'][-1]}  
    tranzitii = {}

    for t in sections['tranzitii']:
        left, right = t.split("->")
        curr_stare, curr_symbol = left.strip()[1:-1].split(',')
        new_stare, new_symbol, move = right.strip()[1:-1].split(',')
        tranzitii[(curr_stare, curr_symbol)] = (new_stare, new_symbol, move)

    return tape, head, stare, tranzitii, final_stari


def print_tape(tape, head, stare):
    print("tape:", ' '.join(tape))
    print("Head:", '    ' * head + '^')
    print("stare:", stare)
    print()

# Functie care executa masina Turing

def runTM(tape, head, stare, tranzitii, final_stari):
    print("Initial stare:")
    print_tape(tape, head, stare)

    while stare not in final_stari:
        symbol = tape[head]
        key = (stare, symbol)

        if key not in tranzitii:
            print("No transition found.")
            break

        new_stare, new_symbol, directie = tranzitii[key]
        tape[head] = new_symbol
        stare = new_stare

        if directie == 'R':
            head += 1
            if head == len(tape):
                tape.append('_')
        elif directie == 'L':
            if head > 0:
                head -= 1

        print_tape(tape, head, stare)

    print("Final stare reached.")
    print_tape(tape, head, stare)


if __name__ == "__main__":
    filename = "file.tm"  # Numele fisierului cu definitia masinii
    sections = inputFile(filename)  
    tape, head, stare, tranzitii, final_stari = turingM(sections)
    runTM(tape, head, stare, tranzitii, final_stari)
