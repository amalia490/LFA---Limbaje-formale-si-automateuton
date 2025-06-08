# LFA-Limbaje formale si automate
Acest repository conține implementări ale principalelor modele teoretice din teoria automatelor: NFA (automat finit nedeterminist), DFA (automat finit determinist), PDA (automat cu stivă) și Mașina Turing. Proiectul urmărește simularea comportamentului limbajelor formale și înțelegerea modelelor de calcul studiate în cadrul disciplinei „Limbaje formale și automate”.
Fiecare program include un exemplu de fișier .txt din care se citește configurația specifică (alfabet, stări, tranziții, etc.), pentru a demonstra funcționarea modelului.
Mai jos se găsesc structurile fișierelor .txt, pentru ca utilizatorul să știe cum să scrie corect datele de intrare în fișierul de citire pentru fiecare model:

# DFA / NFA

Lista_Simboluri:
    symbol1
    symbol2
    ...
    ...
    ...
    symbolN
End

Lista_Stari:
    stare1 
    stare2 
    ...
    ...
    ...
    stareN 
End

Stare_start:
    stareX
End

Stari_finale:
    stare1
    stare2
    ...
    ...
    ...
    stareF

#δ ->  stareM - symbolN - stareL
Lista Tranzitii:
    (stare1, symbol2) - stare5
    (stare3, symbol4) - stare6
    ...
    ...
    ...
    (stareM, symbolN) - stareL
End


# PDA

Lista Simboluri:
    symbol0
    symbol1
    ...
    ...
    ...
    symbolN
End

Alfabet de stiva:
    stack0
    stack1
    ...
    ...
    ...
    stackM

Lista Stari:
    stare0 
    stare1 
    ...
    ...
    ...
    stareN 
End

Simbol_start:
    stackX

Stare_start:
    stareX
End

Stari_acceptate
    stareX
    ...
    ...
    ...

#δ ->  (stare - input_symbol - stack_top) - (urmatoarea_stare, stack_push)
Lista Tranzitii:
    (stare0, symbol, stackZ) - (stare1, stackAZ)
    ...
    ...
    ...
End

# TM

Symbols:
    simbol1
    simbol2
    ...
    simbolN
    _
End

Tape:
    simbolA simbolB ... .... ...
End

States:
    stareA
    stareB
    ...
    stareF
End

#δ ->  (stare_curenta, simbol_citit) - (stare_urmatoare, simbol_scris, directie)
Transitions:
    (stare1, simbol1) - (stare2, simbol2, R)
    (stare2, simbol2) - (stare3, simbol3, L)
    ...
    ...
    ...
    (stareN, simbolZ) - (stareE, simbolR, S)
End


-----------------------------------------------------------------------------------
-----------------------------------------------------------------------------------



