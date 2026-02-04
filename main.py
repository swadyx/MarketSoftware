import psycopg2
from dbADIS import add_data, delete_data, inspect_data, search_by_id, search_by_name


def login():
    try:
        db = input("database name (default: postgres): ") or "postgres"
        user2 = input("username (default: postgres): ") or "postgres"
        password2 = input("password: ")
        host2 = "127.0.0.1"
        port2 = 5432

        connection = psycopg2.connect(
            database=db,
            user=user2,
            password=password2,
            host=host2,
            port=port2
        )
        print("Connection established successfully!\n")

        return connection

    except Exception as e:
        print(f"Error: {e}")
        raise


def main():
    conn = login()

    while True:
        print("\n===== VALIKKO =====")
        print("1. Lisää tuote")
        print("2. Poista tuote")
        print("3. Näytä kaikki tuotteet")
        print("4. Hae tuotetta")
        print("5. Poistu\n")

        try:
            x = int(input("---- Valitse: "))
        except ValueError:
            print("Anna numero 1-5!")
            continue

        if x == 1:
            print("\n--- Lisää uusi tuote ---")
            x1 = input("Anna tuotteen nimi: ")
            x2 = float(input("Anna tuotteen hinta (esim. 2.99): "))
            x3 = int(input("Anna tuotteiden määrä: "))
            tiedot = (x1, x2, x3)
            try:
                add_data(conn, "tuotteet", ("nimi", "hinta", "maara"), tiedot)
            except Exception as e:
                print(f"Virhe: {e}")

        elif x == 2:
            print("\n--- Poista tuote ---")
            print("Anna ehto muodossa:")
            print("  id = 1")
            print("  nimi = 'pirkka maito 1l'")
            tieto = input("Kerro mitä haluat poistaa: ")
            try:
                delete_data(conn, "tuotteet", tieto)
            except Exception as e:
                print(f"Virhe: {e}")

        elif x == 3:
            print("\n--- Kaikki tuotteet ---")
            try:
                inspect_data(conn, "tuotteet")
            except Exception as e:
                print(f"Virhe: {e}")

        elif x == 4:
            print("\n--- Hae tuotetta ---")
            print("1. Hae ID:llä")
            print("2. Hae nimellä")
            hakutapa = input("Valitse hakutapa (1/2): ")

            if hakutapa == "1":
                try:
                    id_haku = int(input("Anna tuotteen ID: "))
                    search_by_id(conn, "tuotteet", id_haku)
                except ValueError:
                    print("Anna kelvollinen ID-numero!")
                except Exception as e:
                    print(f"Virhe: {e}")

            elif hakutapa == "2":
                nimi_haku = input("Anna tuotteen nimi (tai osa nimestä): ")
                try:
                    search_by_name(conn, "tuotteet", nimi_haku, name_column="nimi")
                except Exception as e:
                    print(f"Virhe: {e}")
            else:
                print("Valitse 1 tai 2!")

        elif x == 5:
            print("Suljetaan yhteys...")
            conn.close()
            print("Näkemiin!")
            break

        else:
            print("Valitse numero 1-5!")


if __name__ == "__main__":
    main()
