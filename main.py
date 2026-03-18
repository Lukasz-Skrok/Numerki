#Łukasz Skrok
#Łukasz Gołębiowski
#Wariant Zadania: 3B (bisekcja i falsi)
import sys
import math
import matplotlib.pyplot as plt
import numpy as np


def potega(podstawa, wykladnik): #bo nie mamy uzywac wbudowanych dla poteg calkowitych, ale dla pozostalych mozna? idk
    if isinstance(wykladnik, int) or (isinstance(wykladnik, float) and wykladnik.is_integer()):
        wynik = 1.0
        ile_razy = abs(int(wykladnik))

        for i in range(ile_razy):
            wynik *= podstawa

        if wykladnik < 0:
            return 1.0 / wynik
        else:
            return wynik
    else:
        return podstawa ** wykladnik

def Horner(x):
    wsp = [1, 5, -17, -21] #miejsca zerowe to -7, -1 i 3
    y = wsp[0]
    for i in range(1, len(wsp)):
        y = y * x + wsp[i]
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
    while (wariant == 1 and iter < maks) or (wariant == 2 and dokladnosc > wartosc):
        fA = f(tryb, x1)
        x0 = (x1 + x2) / 2
        fx0 = f(tryb, x0)
        if fA * fx0 <= 0:
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
    while (wariant == 1 and iter < maks) or (wariant == 2 and dokladnosc > wartosc):
        fA = f(tryb, x1)
        fB = f(tryb, x2)
        x0 = (x1 * fB - x2 * fA) / (fB - fA)
        fx0 = f(tryb, x0)
        if fA * fx0 <= 0:
            x2 = x0
        else:
            x1 = x0
        iter += 1
        dokladnosc = abs(fx0)
    return x0, iter, dokladnosc

def rysuj_wykres(tryb, x1, x2, r1, r2):
    margin = abs(x2 - x1) * 0.2
    x = np.linspace(x1 - margin, x2 + margin, 500)
    y = [f(tryb, val) for val in x]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label='f(x)', color='blue', linewidth=2)
    plt.axhline(0, color='black', linestyle='--', linewidth=1)

    # Zaznaczenie wyników
    plt.scatter([r1], [0], color='red', zorder=5, label=f'Bisekcja: {r1:.4f}')
    plt.scatter([r2], [0], color='green', marker='x', s=100, zorder=5, label=f'Falsi: {r2:.4f}')

    plt.title(f"Porównanie metod dla wybranej funkcji")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.show()

def pomoc():
    print("""
Struktura komendy:
    --funkcja --metoda_sprawdzania <x1> <x2> <ogranicznik>
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

if len(sys.argv) != 6:
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


if f(tryb, x1) * f(tryb, x2) >= 0:
    print(f"BŁĄD: Funkcja na końcach przedziału [{x1}, {x2}] ma ten sam znak!")
    print(f"f({x1}) = {f(tryb, x1):.4f}, f({x2}) = {f(tryb, x2):.4f}")
    sys.exit(1)

res_b, it_b, ep_b = Bisekcja(x1, x2, tryb, wariant, limit)
res_f, it_f, ep_f = Falsi(x1, x2, tryb, wariant, limit)

# Wyniki w konsoli
print(f"{'Metoda':<15} | {'Miejsce zerowe':<15} | {'Iteracje':<8} | {'Błąd |f(x)|'}")
print("-" * 50)
print(f"{'Bisekcja':<15} | {res_b:<15.8f} | {it_b:<8} | {ep_b:.2e}")
print(f"{'Regula Falsi':<15} | {res_f:<15.8f} | {it_f:<8} | {ep_f:.2e}")

rysuj_wykres(tryb, x1, x2, res_b, res_f)