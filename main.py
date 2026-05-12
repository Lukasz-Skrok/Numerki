#Łukasz Skrok
#Łukasz Gołębiowski
#Wariant Zadania: 2 (wielomiany Hermite'a)
import math


# --- 1. FUNKCJE BAZOWE ---

def horner(wsp, x):
    y = wsp[0]
    n = len(wsp)
    i = 1
    while i < n:
        y = y * x + wsp[i]
        i += 1
    return y


def f(tryb, x):
    if tryb == 1:
        return 2.0 * x + 3.0  # Liniowa
    elif tryb == 2:
        return abs(x)  # Moduł
    elif tryb == 3:
        wsp = [1.0, 5.0, -17.0, -21.0]  # Wielomian
        return horner(wsp, x)
    elif tryb == 4:
        return math.sin(x)  # Trygonometryczna
    elif tryb == 5:
        return math.sin(x * x)  # Złożona (sin(x^2))
    elif tryb == 6:
        return 1.0  # Stała do testow
    return 0.0


def f_z_waga(tryb, x):
    # Zabezpieczenie przed błędem przepełnienia float dla gigantycznych X.
    # Wartość e^(-x^2) dla x > 30 jest tak bliska zera, że nie ma znaczenia.
    if abs(x) > 30.0:
        return 0.0
    return f(tryb, x) * math.exp(- (x * x))


# --- 2. METODA ZŁOŻONA SIMPSONA (NEWTONA-COTESA) ---

def simpson_krok(a, b, tryb, n):

    h = (b - a) / n
    suma = f_z_waga(tryb, a) + f_z_waga(tryb, b)

    i = 1
    while i < n:
        x_i = a + i * h
        if i % 2 != 0:
            suma += 4.0 * f_z_waga(tryb, x_i)
        else:
            suma += 2.0 * f_z_waga(tryb, x_i)
        i += 1

    return suma * (h / 3.0)


def simpson_dokladnosc(a, b, tryb, epsilon):

    n = 2
    poprzedni = simpson_krok(a, b, tryb, n)
    n = 4
    aktualny = simpson_krok(a, b, tryb, n)

    while abs(aktualny - poprzedni) >= epsilon:
        poprzedni = aktualny
        n *= 2
        aktualny = simpson_krok(a, b, tryb, n)

    return aktualny


def calka_simpson_nieskonczonosc(tryb, epsilon):

    delta = 1.0  # Długość pojedynczego badanego podprzedziału

    # KROK 1: Obliczanie granicy w kierunku +nieskończoności
    suma_dodatnia = 0.0
    a = 0.0
    dziala = True
    while dziala:
        i_part = simpson_dokladnosc(a, a + delta, tryb, epsilon)
        suma_dodatnia += i_part

        # Jeżeli całka na podprzedziale jest mniejsza od błędu, zakładamy dotarcie do nieskończoności
        if abs(i_part) < epsilon:
            dziala = False
        else:
            a += delta
            if a > 40.0:  # Awaryjne zabezpieczenie przed zawieszeniem
                dziala = False

                # KROK 2: Obliczanie granicy w kierunku -nieskończoności
    suma_ujemna = 0.0
    b = 0.0
    dziala = True
    while dziala:
        i_part = simpson_dokladnosc(b - delta, b, tryb, epsilon)
        suma_ujemna += i_part

        if abs(i_part) < epsilon:
            dziala = False
        else:
            b -= delta
            if b < -40.0:
                dziala = False

    return suma_ujemna + suma_dodatnia


# --- 3. METODA GAUSSA-HERMITE'A ---

def gauss_hermite(tryb, liczba_wezlow):

    x_wezly = []
    A_wagi = []

    if liczba_wezlow == 2:
        x_wezly = [-0.707107, 0.707107]
        A_wagi = [0.886227, 0.886227]
    elif liczba_wezlow == 3:
        x_wezly = [-1.224745, 0.0, 1.224745]
        A_wagi = [0.295409, 1.181636, 0.295409]
    elif liczba_wezlow == 4:
        x_wezly = [-1.650680, -0.534648, 0.534648, 1.650680]
        A_wagi = [0.081313, 0.804914, 0.804914, 0.081313]
    elif liczba_wezlow == 5:
        x_wezly = [-2.020183, -0.958572, 0.0, 0.958572, 2.020183]
        A_wagi = [0.019953, 0.393619, 0.945309, 0.393619, 0.019953]
    else:
        return 0.0

    suma = 0.0
    i = 0
    while i < liczba_wezlow:
        # W Gaussie NIE MNOŻYMY przez e^-x^2
        suma += A_wagi[i] * f(tryb, x_wezly[i])
        i += 1

    return suma


# --- 4. MENU ---

def main():
    dziala = True

    while dziala:
        print("\n=== CAŁKOWANIE NUMERYCZNE (WARIANT 2 - HERMITE) ===")
        print("Przedział: (-inf, +inf), Waga: e^(-x^2)")
        print("1. Liniowa (2x + 3)")
        print("2. Moduł (|x|)")
        print("3. Wielomian (x^3 + 5x^2 - 17x - 21)")
        print("4. Trygonometryczna (sin(x))")
        print("5. Złożona (sin(x^2))")
        print("6. Funkcja stała (f(x) = 1) - TESTOWA")
        print("7. Wyjdź z programu")

        wybor_str = input("Wybierz funkcję (1-7): ")

        if wybor_str == '7':
            dziala = False
        elif wybor_str in ['1', '2', '3', '4', '5', '6']:
            tryb = int(wybor_str)
            eps_str = input("Podaj żądaną dokładność epsilon (np. 0.0001): ")
            epsilon = float(eps_str)

            print("\nTrwają obliczenia, proszę czekać (przy małym epsilonie metoda Simpsona potrzebuje czasu)...\n")

            wynik_simpson = calka_simpson_nieskonczonosc(tryb, epsilon)

            wynik_g2 = gauss_hermite(tryb, 2)
            wynik_g3 = gauss_hermite(tryb, 3)
            wynik_g4 = gauss_hermite(tryb, 4)
            wynik_g5 = gauss_hermite(tryb, 5)

            print("--- WYNIKI ---")
            print(f"Metoda złożona Simpsona (epsilon = {epsilon}): {wynik_simpson:.6f}")
            print("\nMetoda Gaussa-Hermite'a:")
            print(f"2 węzły: {wynik_g2:.6f}")
            print(f"3 węzły: {wynik_g3:.6f}")
            print(f"4 węzły: {wynik_g4:.6f}")
            print(f"5 węzłów: {wynik_g5:.6f}")
            print("--------------------------------------------------")

        else:
            print("Niepoprawny wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()