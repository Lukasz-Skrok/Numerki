#Łukasz Skrok
#Łukasz Gołębiowski
#Wariant Zadania: 1 (metoda Lagrange'a dla węzłów równoodległych)

import math
import matplotlib.pyplot as plt
import numpy as np

def horner(wsp, x):
    y = wsp[0]
    for i in range(1, len(wsp)):
        y = y * x + wsp[i]
    return y


def potega(podstawa, wykladnik):
    if isinstance(wykladnik, int) or (isinstance(wykladnik, float) and wykladnik.is_integer()):
        wynik = 1.0
        ile_razy = abs(int(wykladnik))
        for _ in range(ile_razy):
            wynik *= podstawa
        return 1.0 / wynik if wykladnik < 0 else wynik
    return podstawa ** wykladnik


def f(wybor, x):
    match wybor:
        case 1:
            return 2 * x + 3  # Liniowa
        case 2:
            return abs(x)  # |x|
        case 3:
            return horner([1, 5, -17, -21], x)  # Wielomian
        case 4:
            return math.sin(x)  # Trygonometryczna
        case 5:
            return math.sin(potega(2, x) - 0.5)  # Złożona
        case _:
            return 0


# Logika Interpolacji

def lagrange(x_wezly, y_wezly, x_punkt):
    n = len(x_wezly)
    wynik = 0
    for i in range(n):
        li = 1
        for j in range(n):
            if i != j:
                li *= (x_punkt - x_wezly[j]) / (x_wezly[i] - x_wezly[j])
        wynik += y_wezly[i] * li
    return wynik


# Obsługa Interfejsu

def rysuj_wynik(wybor_f, x_wezly, y_wezly, a, b):
    x_plot = np.linspace(a, b, 500)
    y_oryginalna = [f(wybor_f, val) for val in x_plot]
    y_interpolowana = [lagrange(x_wezly, y_wezly, val) for val in x_plot]

    plt.figure(figsize=(12, 7))
    plt.plot(x_plot, y_oryginalna, label='Funkcja oryginalna', color='blue', alpha=0.6)
    plt.plot(x_plot, y_interpolowana, '--', label='Wielomian Lagrange\'a', color='red')
    plt.scatter(x_wezly, y_wezly, color='black', zorder=5, label='Węzły interpolacji')

    plt.title(f"Interpolacja Lagrange'a (Liczba węzłów: {len(x_wezly)})")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def main():
    while True:
        print("\nMENU INTERPOLACJI (LAGRANGE)")
        print("1. Wybierz funkcję i parametry")
        print("2. Wyjdź")

        opcja = input("Wybierz opcję: ")
        if opcja == '2': break
        if opcja != '1': continue

        print("\nDostępne funkcje:")
        print(
            "1. Liniowa (2x + 3)\n2. Moduł (|x|)\n3. Wielomian (x^3 + 5x^2 - 17x - 21)\n4. Trygonometryczna (sin(x))\n5. Złożona (sin(2^x - 0.5))")
        wybor_f = int(input("Wybór: "))

        a = float(input("Początek przedziału (a): "))
        b = float(input("Koniec przedziału (b): "))
        n = int(input("Liczba węzłów (n): "))

        if n > 1:
            h = (b - a) / (n - 1)
        else:
            h = 0

        x_wezly = []
        for i in range(n):
            xi = a + i * h
            x_wezly.append(xi)

        y_wezly = [f(wybor_f, val) for val in x_wezly]

        print("\nWęzły [x, f(x)]:")
        for i in range(n):
            print(f"[{x_wezly[i]:.4f}, {y_wezly[i]:.4f}]")

        rysuj_wynik(wybor_f, x_wezly, y_wezly, a, b)


if __name__ == "__main__":
    main()