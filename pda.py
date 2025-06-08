
symbols = []
alfabet_stiva = []
stari = []
accept_stari = []
tranzitii = []
start_stiva_simb = []
stare_start = []
error = 0

# Citire fisier
with open("file.pda", "r") as f:
    section = None
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("Lista Simboluri:"):
            section = "symbols"
            continue
        elif line.startswith("Alfabet de stiva:"):
            section = "alfabet_stiva"
            continue
        elif line.startswith("Lista Stari:"):
            section = "stari"
            continue
        elif line.startswith("Simbol_start:"):
            section = "start_stiva_simb"
            continue
        elif line.startswith("Stare_start:"):
            section = "stare_start"
            continue
        elif line.startswith("Stari_acceptate:"):
            section = "accept_stari"
            continue
        elif line.startswith("Lista Tranzitii:"):
            section = "tranzitii"
            continue
        elif line.startswith("End"):
            section = None
            continue

        if section == "symbols":
            symbols.append(line)
        elif section == "alfabet_stiva":
            alfabet_stiva.append(line)
        elif section == "stari":
            stari.append(line)
        elif section == "start_stiva_simb":
            start_stiva_simb.append(line)
        elif section == "stare_start":
            stare_start.append(line)
        elif section == "accept_stari":
            accept_stari.append(line)
        elif section == "tranzitii":
            try:
                left, right = line.split(" - ")
                from_state, input_symbol, stack_top = left[1:-1].split(",")
                to_state, stack_push = right[1:-1].split(",")
                tranzitii.append((
                    from_state.strip(),
                    input_symbol.strip(),
                    stack_top.strip(),
                    to_state.strip(),
                    stack_push.strip().split() if stack_push.strip() != 'e' else []
                ))
            except:
                print(f"Invalid transition format: {line}")
                error = 1

# Validare config PDA
if len(symbols) != len(set(symbols)):
    print("Duplicate symbols found in the alphabet.")
    error = 1
if len(alfabet_stiva) != len(set(alfabet_stiva)):
    print("Duplicate stack symbols found in the stack alphabet.")
    error = 1
if len(stari) != len(set(stari)):
    print("Duplicate states found in the list of states.")
    error = 1

if len(stare_start) != 1:
    print("There should be exactly one start state.")
    error = 1
elif stare_start[0] not in stari:
    print(f"Start state '{stare_start}' is not in the list of stari.")
    error = 1
if len(start_stiva_simb) != 1:
    print("There should be exactly one start stack symbol.")
    error = 1
elif start_stiva_simb[0] not in alfabet_stiva:
    print(f"Start stack symbol '{start_stiva_simb}' not in stack alphabet.")
    error = 1
if not set(accept_stari).issubset(set(stari)):
    print("Some accept stari are not defined in stari list.")
    error = 1

for (from_state, input_symbol, stack_top, to_state, stack_push) in tranzitii:
    if from_state not in stari:
        print(f"Transition from unknown state: {from_state}")
        error = 1
    if input_symbol not in symbols and input_symbol != 'e':
        print(f"Transition with unknown symbol: {input_symbol}")
        error = 1
    if stack_top not in alfabet_stiva:
        print(f"Transition with unknown stack top symbol: {stack_top}")
        error = 1
    if to_state not in stari:
        print(f"Transition to unknown state: {to_state}")
        error = 1
    for symbol in stack_push:
        if symbol not in alfabet_stiva and symbol != 'e':
            print(f"Transition with unknown stack push symbol: {symbol}")
            error = 1

# PDA simulation
def simulate_pda(input_string):
    from collections import deque
    queue = deque()
    queue.append((stare_start[0], 0, [start_stiva_simb[0]], []))  

    while queue:
        current_state, input_index, stack, path = queue.popleft()


        #if current_state in accept_stari:
         #   print("Merge1")
        if input_index == len(input_string) and current_state in accept_stari:
            # Afisare traseu dupa acceptarea input-ului
            print("Input ACCEPTED.\nTrace:")
            for step in path:
                print(step)
            print(f"Reached accept state: {current_state} with stack: {stack}")
            return

        for (from_state, input_sym, stack_top, to_state, push_stack) in tranzitii:
            if from_state == current_state:
                if stack and stack[0] == stack_top:
                    if input_sym == 'e' or (input_index < len(input_string) and input_string[input_index] == input_sym):
                        # Pregătim noul input index
                        new_index = input_index if input_sym == 'e' else input_index + 1
                        # Noua stivă
                        new_stack = push_stack + stack[1:]
                        # Construim mesajul pentru acest pas
                        step_msg = (f"({from_state}, {input_sym}, {stack_top}) -> "
                                    f"({to_state}, push: {' '.join(push_stack) if push_stack else 'e'}, "
                                    f"input: {input_string[input_index:]}, stack: {stack})")
                        # Adăugăm în coadă cu traseul actualizat
                        queue.append((to_state, new_index, new_stack, path + [step_msg]))

    print("Input REJECTED. No valid tranzitii lead to an accept state.")


# Run PDA
if error == 0:
    print("PDA loaded successfully.")
    test_input = input("Enter the input string: ").strip()
    simulate_pda(test_input)
else:
    print("PDA configuration invalid.")
