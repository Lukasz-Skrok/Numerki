#Łukasz Skrok
#Łukasz Gołębiowski
#Wariant Zadania: 3B (bisekcja i falsi)
import sys
import math

def potega(x , y): #podnosi x do potegi y
    wynik = 1
    for i in range(y):
        wynik *= x
    return wynik

def Horner(x):
    wsp = [1, 5, -17, -21] #miejsca zerowe to -7, -1 i 3
    y = wsp[0]
    for i in range(1, len(wsp)):
        y = y * x +wsp[i]
    return y

def f(var, x): #zwraca wartosc funkcji w danym x
    match var:
        case 1:
            return Horner(x)
        case 2:
            return math.sin(x)
        case 3:
            return potega(2, x) - 0.5
        case 4:
            return math.sin(potega(2, x) - 0.5)
        case _:
            print("coś poszło nie tak :(")
            return None


def Bisekcja(x1, x2, tryb, wariant, wartosc): #wariant - 1 dla iteracji, 2 dla dokladnosci, wartosc koresponduje do epsilon albo ilosci operacji
    iter = 0                                  #tryb steruje tym ktora funkcje mamy, zgodnie z powyzsza funkcja f(var,x)
    x0 = 0
    maks = 90000
    if wariant == 1:
        maks = wartosc
    elif wariant == 2:
        dokladnosc = wartosc + 1.0
    while wariant == 1 and iter < maks or wariant == 2 and dokladnosc < wartosc:
        fA = f(tryb, x1)
        x0 = (x1 + x2) / 2
        fx0 = f(tryb, x0)
        if fA * fx0 < 0:
            x2 = x0
        else:
            x1 = x0
        iter += 1
        dokladnosc = abs(fx0)
    return x0, iter, dokladnosc

def Falsi(x1, x2, tryb, wariant, wartosc):
    iter = 0
    x0 = 0
    maks = 90000
    if wariant == 1:
        maks = wartosc
    elif wariant == 2:
        dokladnosc = wartosc + 1.0
    while wariant == 1 and iter < maks or wariant == 2 and dokladnosc < wartosc:
        fA = f(tryb, x1)
        fB = f(tryb, x2)
        x0 = (x1 * fB - x2 * fA) / (fB - fA)
        fx0 = f(tryb, x0)
        if fA * fx0 < 0:
            x1 = x0
        else:
            x2 = x0
        iter += 1
        dokladnosc = abs(fx0)
    return x0, iter, dokladnosc
def pomoc():
    print("""
Struktura komendy:
    --funkcja --metoda sprawdzania <x1> <x2> <ogranicznik>
Dostępne funkcje:
    wielomian
    tryg
    wyklad
    zlozona
Dostępne metody sprawdzania:
    iter
    epsilon
Ogranicznik to wartość numeryczna odpowiadająca metodzie sprawdzania (liczba iteracji bądź wartość epsilon)
    """)

if len(sys.argv) != 5:
    pomoc()
    sys.exit(0)

args = sys.argv[1:]
funkcja = args[0]
metoda = args[1]
x1 = float(args[2])
x2 = float(args[3])
limit = float(args[4])

if funkcja == "--wielomian":
    tryb = 1
elif funkcja == "--tryg":
    tryb = 2
elif funkcja == "--wyklad":
    tryb = 3
elif funkcja == "--zlozona":
    tryb = 4
else:
    print("Niepoprawna funkcja.")
    pomoc()
    sys.exit(0)

if metoda == "--iter":
    wariant = 1
elif metoda == "--epsilon":
    wariant = 2
else:
    print("Niepoprawna metoda.")
    pomoc()
    sys.exit(0)

Bisekcja(x1, x2, tryb, wariant, limit)