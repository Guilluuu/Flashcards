import os
import queue
import shutil
from termcolor import colored

class Flashcard:
    def __init__(self, question, answer, difficulty=4):
        self.question = question
        self.answer = answer
        self.difficulty = difficulty

    def __lt__(self, other):
        return self.difficulty > other.difficulty  # Mayor dificultad, mayor prioridad

class Deck:
    def __init__(self, name):
        self.name = name
        self.subdecks = []
        self.flashcards = queue.PriorityQueue()
        self.flashcard_list = []

    def add_flashcard(self, flashcard):
        self.flashcards.put(flashcard)
        self.flashcard_list.append(flashcard)

    def add_subdeck(self, subdeck):
        self.subdecks.append(subdeck)

    def remove_flashcard(self, index):
        if 0 <= index < len(self.flashcard_list):
            self.flashcard_list.pop(index)

    def __str__(self):
        return self.name

def load_deck(deck_name):
    deck = Deck(deck_name)
    file_path = os.path.join(deck_name, "flashcards.txt")

    try:
        with open(file_path, 'r') as file:
            for line in file:
                question, answer, difficulty = line.strip().split('|')
                difficulty = int(difficulty)
                flashcard = Flashcard(question, answer, difficulty)
                deck.add_flashcard(flashcard)
    except FileNotFoundError:
        print(f"El mazo '{deck_name}' no existe o no contiene tarjetas.")
    except ValueError:
        print("Error en el formato del archivo. Asegúrate de que sea Pregunta|Respuesta|Dificultad.")

    return deck

def save_deck(deck):
    file_path = os.path.join(deck.name, "flashcards.txt")
    os.makedirs(deck.name, exist_ok=True)

    with open(file_path, 'w') as file:
        for flashcard in deck.flashcard_list:
            file.write(f"{flashcard.question}|{flashcard.answer}|{flashcard.difficulty}\n")

def quiz(deck):
    while not deck.flashcards.empty():
        flashcard = deck.flashcards.get()

        print(f"\nPregunta: {flashcard.question}")
        input("Presiona Enter para ver la respuesta...")

        print(f"Respuesta correcta: {flashcard.answer}")

        while True:
            try:
                new_difficulty = int(input("¿Cuál fue la dificultad de esta pregunta (0-4)? "))
                if 0 <= new_difficulty <= 4:
                    flashcard.difficulty = new_difficulty
                    break
                else:
                    print("Por favor, ingresa un valor entre 0 y 4.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

        deck.add_flashcard(flashcard)

        stop_study = input("¿Deseas parar el estudio? (s/n): ").strip().lower()
        if stop_study == 's':
            break

def delete_flashcard(deck):
    print("\n--- Preguntas en el mazo ---")
    for index, flashcard in enumerate(deck.flashcard_list):
        print(f"{index}. Pregunta: {flashcard.question} | Respuesta: {flashcard.answer}")

    while True:
        try:
            index_to_delete = int(input("Selecciona el número de la pregunta que deseas eliminar: "))
            if 0 <= index_to_delete < len(deck.flashcard_list):
                deck.remove_flashcard(index_to_delete)
                print("Pregunta eliminada exitosamente.")
                break
            else:
                print("Número no válido. Por favor, intenta de nuevo.")
        except ValueError:
            print("Por favor, ingresa un número válido.")

def display_decks(base_path, level=0):
    for item in os.listdir(base_path):
        path = os.path.join(base_path, item)
        if os.path.isdir(path):
            print("  " * level + f"📁 {item}")
            display_decks(path, level + 1)
        elif item.endswith(".txt"):
            print("  " * level + f"📄 {item}")

def delete_deck(deck_path):
    if os.path.isdir(deck_path):
        confirmation = input(f"¿Estás seguro de que deseas eliminar el mazo '{deck_path}' y todo su contenido? (s/n): ").strip().lower()
        if confirmation == 's':
            shutil.rmtree(deck_path)
            print(f"Mazo '{deck_path}' eliminado exitosamente.")
        else:
            print("Operación cancelada.")
    else:
        print("El mazo especificado no existe.")

def navigate_decks(base_path):
    while True:
        print("\n--- Estructura de Mazos ---")
        display_decks(base_path)

        print("\n--- Menú ---")
        print("1. 📚 Estudiar un mazo")
        print("2. ➕ Añadir tarjeta a un mazo")
        print("3. 🗂️ Añadir un nuevo mazo")
        print("4. 🗑️ Eliminar pregunta de un mazo")
        print("5. ❌ Eliminar un mazo")
        print("6. 🔙 Volver al menú principal")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            deck_name = input("Escribe el nombre del mazo que quieres estudiar (incluyendo submazos): ")
            if os.path.isdir(deck_name):
                deck = load_deck(deck_name)
                quiz(deck)
                save_deck(deck)
            else:
                print("El mazo no existe.")

        elif choice == "2":
            deck_name = input("Escribe el nombre del mazo donde quieres añadir la tarjeta (incluyendo submazos): ")
            deck = load_deck(deck_name) if os.path.isdir(deck_name) else Deck(deck_name)
            question = input("Pregunta: ")
            answer = input("Respuesta: ")
            flashcard = Flashcard(question, answer)
            deck.add_flashcard(flashcard)
            print("Tarjeta añadida exitosamente.")
            save_deck(deck)

        elif choice == "3":
            new_deck_name = input("Escribe el nombre del nuevo mazo (incluyendo la ruta): ")
            if not os.path.isdir(new_deck_name):
                os.makedirs(new_deck_name)
                print(f"Mazo '{new_deck_name}' creado exitosamente.")
            else:
                print(f"El mazo '{new_deck_name}' ya existe.")

        elif choice == "4":
            deck_name = input("Escribe el nombre del mazo del que deseas eliminar una pregunta (incluyendo submazos): ")
            if os.path.isdir(deck_name):
                deck = load_deck(deck_name)
                delete_flashcard(deck)
                save_deck(deck)
            else:
                print("El mazo no existe.")

        elif choice == "5":
            deck_name = input("Escribe el nombre del mazo que deseas eliminar (incluyendo submazos): ")
            delete_deck(deck_name)

        elif choice == "6":
            break

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display_decks('.')

        print("\n--- Menú Principal ---")
        print("1. 📁 Navegar entre mazos")
        print("2. ❌ Salir")

        choice = input("Selecciona una opción: ")

        if choice == "1":
            navigate_decks('.')

        elif choice == "2":
            print("Saliendo...")
            break

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main()
