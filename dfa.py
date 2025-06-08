# Initializare listele pentru simboluri, stari, stari finale, tranzitii si stare de start

symbols = []
stari = []
accept_states = []
tranzitii = []
stare_start= []
error = 0
section = None

#Functie pentru rularea DFA-ului la primirea unui input

def input_dfa():
    print("Enter the input string to run the automaton: ")
    input_string = input().strip()
    current_state = stare_start[0]  
    for symbol in input_string:
        if symbol not in symbols:
            print(f"Symbol '{symbol}' is not recognized.")
            return
        found_transition= False
        for (from_state, transition_symbol, to_state) in tranzitii:
            if from_state == current_state and transition_symbol == symbol:
                current_state = to_state
                found_transition = True
                break
        if not found_transition:
            print(f"No transition found for state '{current_state}' with symbol '{symbol}'.")
            return
    if current_state in accept_states:
        print("Input string is accepted by the DFA.")
    else:
        print("Input string is rejected by the DFA.") 

# Citire configuratie DFA din fisier

for line in open("file.dfa", "r"):
    line = line.strip()
    if not line:
        continue
    if line.startswith("Lista_Simboluri:"):
        section = "symbols"
        continue
    elif line.startswith("Lista_Stari:"):
        section = "stari"
        continue
    elif line.startswith("Stare_start:"):
        section = "stare_start"
        continue
    elif line.startswith("Stari_finale:"):
        section = "accept_states"
        continue
    elif line.startswith("Lista_Tranzitii:"):
        section = "tranzitii"
        continue
    elif line.startswith("End"):
        section = None
        continue

    if section == "symbols":
        symbols.append(line)
    elif section == "stari":
        stari.append(line)
    elif section == "stare_start":
        stare_start.append(line)
    elif section == "accept_states":
        accept_states.append(line)
    elif section == "tranzitii":
        if "-" not in line or "(" not in line or ")" not in line:
            print(f"Invalid transition: {line}")
            continue
        try:
            parts = line.split(" - ")
            left = parts[0].strip()[1:-1]
            from_state, symbol = map(str.strip, left.split(","))
            to_state = parts[1].strip()
            tranzitii.append((from_state, symbol, to_state))
        except Exception as e:
            print(f"Failed to parse transition: {line}. Error: {e}")


if len(symbols) != len(set(symbols)):
    print("Duplicate symbols.")
    error = 1
if len(stari) != len(set(stari)):
    print("Duplicate stari.")
    error = 1

for(from_state, symbol, to_state) in tranzitii:
    if from_state not in stari:
        print(f"Transition from unknown state: {from_state}")
        error = 1
    elif symbol not in symbols:
        print(f"Transition with unknown symbol: {symbol}")
        error = 1
    elif to_state not in stari:
        print(f"Transition to unknown state: {to_state}")
        error = 1

if len(stare_start) != 1:
    print("There is more than one start state.")
    error = 1
elif stare_start[0] not in stari:
    print(f"Start state {stare_start[0]} is not in the list of stari.")
    error = 1

if len(accept_states) < 1:
    print("There are no accept stari.")
    error = 1
elif not all(state in stari for state in accept_states):
    print("Some accept stari are not in the list of stari.")
    error = 1

if error == 0:
    print("DFA is valid.")
    input_dfa()
else:
    print("DFA is invalid.")


