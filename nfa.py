# Initializare listele pentru simboluri, stari, stari finale, tranzitii si stare de start

symbols = []
stari = []
accept_states = []
tranzitii = []
stare_start= []
error = 0
block = None


# Functie care returneaza inchiderile epsilon (toate starile accesibile prin tranzitii 'e')
def epsilon(stari_initiale):
    vizitat = set()
    de_explorat = list(stari_initiale)
    while de_explorat:
        stare = de_explorat.pop(0)
        if stare not in vizitat:
            vizitat.add(stare)
            vecini = [t for (f, simbol, t) in tranzitii if f == stare and simbol == 'e']
            de_explorat.extend(vecini)
    return vizitat

# Functie care returneaza starile urmatoare pentru un simbol dat
def Stari(current_states, symbol):
    return set(
        to_state
        for from_state, s, to_state in tranzitii
        if from_state in current_states and s == symbol
    )


#Functie pentru rularea NFA-ului la primirea unui input
def input_nfa():
    print("Enter the input string to run the automaton: ")
    input_string = input().strip()
    current_state = stare_start[0]

    # Verificam daca toate simbolurile din input sunt valide
    for symbol in input_string:
        if symbol not in symbols and symbol != 'e':
            print(f"Symbol '{symbol}' is not recognized.")
            return
    current_states = epsilon([current_state])
    for symbol in input_string:
        result = Stari(current_states, symbol)
        current_states = epsilon(result)
        print(f"Current stari after processing '{symbol}': {current_states}")
    
    # Verificam dacă cel putin una din starile curente este de acceptare
    if any(state in accept_states for state in current_states):
        print("Input string is accepted by the NFA.")
    else:
        print("Input string is not accepted by the NFA.")

# Citire configuratie NFA din fisier
for line in open("file.nfa", "r"):
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

#Salvare informatie in sectiunea corespunzatoare
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


#Verificari pentru configuratie
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
    elif symbol not in symbols and symbol != 'e':
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
    print("NFA is valid.")
    input_nfa()
else:
    print("NFA is invalid.")


