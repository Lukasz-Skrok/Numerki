#Łukasz Skrok
#Łukasz Gołębiowski
#Wariant Zadania: 3 (metoda iteracyjna Jacobiego (iteracji prostej))

def read_matrix(nazwa_pliku):
    try:
        with open(nazwa_pliku, 'r') as plik:
            dane = plik.read().split()

        if not dane:
            return None

        row = int(dane[0])
        column = int(dane[1])

        A = []
        idx = 2
        for i in range(row):
            wiersz = []
            for j in range(column):
                wiersz.append(float(dane[idx]))
                idx += 1
            A.append(wiersz)

        return A
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{nazwa_pliku}'.")
        return None


def print_matrix(A):
    if A is None:
        print("[ NULL matrix ]")
    else:
        row = len(A)
        column = len(A[0])

        for i in range(row):
            print("[", end="")
            for j in range(column):
                if j < row:
                    print(f"{A[i][j]:8.2f}", end="")
                else:
                    print("  | ", end="")
                    print(f"{A[i][row]:8.2f} ", end="")
            print("]")


def is_convergent(A):
    row = len(A)
    column = len(A[0])
    convergence = True
    i = 0

    while i < row and convergence:
        suma = 0.0
        for j in range(column - 1):
            if i != j:
                suma += abs(A[i][j])

        if abs(A[i][i]) <= suma:
            convergence = False
        i += 1

    if convergence and row == column - 1:
        print("Warunek zbieznosci zostal spelniony i macierz jest kwadratowa. Metoda Jacobiego zadziala\n")
    else:
        print("Warunek zbieznosci nie zostal spelniony. Metoda Jacobiego nie zadziala.\n")

    return convergence


def jacobi_solve(A, tryb, limit):

    n = len(A)
    x = [0.0 for _ in range(n)]
    x_nowe = [0.0 for _ in range(n)]
    iteracja = 0
    dokladnosc = limit + 1.0

    while (tryb == 1 and iteracja < limit) or (tryb == 2 and dokladnosc > limit):
        for i in range(n):
            suma = 0.0
            for j in range(n):
                if i != j:
                    suma += A[i][j] * x[j]
            x_nowe[i] = (A[i][n] - suma) / A[i][i]

        max_roznica = 0.0
        for i in range(n):
            roznica = abs(x_nowe[i] - x[i])
            if roznica > max_roznica:
                max_roznica = roznica

        dokladnosc = max_roznica
        iteracja += 1

        for i in range(n):
            x[i] = x_nowe[i]

    return x, iteracja, dokladnosc


def main():
    macierz_A = None
    dziala = True

    while dziala:
        print("\n--- MENU GŁÓWNE ---")
        print("1. Wczytaj macierz z pliku")
        print("2. Wyświetl macierz")
        print("3. Rozwiąż układ równań (Metoda Jacobiego)")
        print("4. Wyjdź")

        wybor = input("Wybierz opcję: ")

        if wybor == '1':
            nazwa = input("Podaj nazwę pliku (np. dane.txt): ")
            macierz_A = read_matrix(nazwa)
            if macierz_A:
                print("Macierz wczytana pomyślnie.")

        elif wybor == '2':
            print("\nAktualna macierz:")
            print_matrix(macierz_A)

        elif wybor == '3':
            if not macierz_A:
                print("Błąd: Najpierw wczytaj macierz!")
            else:
                print("\nSprawdzanie warunków zbieżności...")
                if not is_convergent(macierz_A):
                    print("UWAGA: Macierz nie spełnia silnego warunku zbieżności.")
                    print("Metoda Jacobiego może nie znaleźć rozwiązania. Przerwano.")
                else:
                    print("\nWybierz kryterium stopu:")
                    print("1. Ilość iteracji")
                    print("2. Dokładność (epsilon)")
                    tryb_stopu = input("Twój wybór (1/2): ")

                    if tryb_stopu == '1' or tryb_stopu == '2':
                        tryb = int(tryb_stopu)
                        if tryb == 1:
                            limit = float(input("Podaj maksymalną liczbę iteracji: "))
                        else:
                            limit = float(input("Podaj dokładność epsilon (np. 0.001): "))

                        wynik, ilosc_iter, osiagnieta_dokladnosc = jacobi_solve(macierz_A, tryb, limit)

                        print("\n--- WYNIKI ---")
                        print(f"Ilość wykonanych iteracji: {ilosc_iter}")
                        print(f"Osiągnięta dokładność: {osiagnieta_dokladnosc:.6e}")
                        print("Rozwiązania (wektor X):")
                        for i, val in enumerate(wynik):
                            print(f"x[{i}] = {val:.6f}")
                    else:
                        print("Nieprawidłowy wybór kryterium stopu.")

        elif wybor == '4':
            print("Koniec programu.")
            dziala = False

        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()