from engine import CheckersEngine

def main():
    game = CheckersEngine()
    
    while True:
        game.display() # Metoda de afișare ASCII
        print(f"\nRândul jucătorului: {game.turn}")
        
        try:
            # Exemplu input: 5,0 4,1
            move_input = input("Introdu mutarea (ex: r1,c1 r2,c2) sau 'exit': ")
            if move_input.lower() == 'exit': break

            parts = move_input.split()
            if len(parts) != 2:
                print("(!) Introdu două coordonate separate prin spațiu.")
                continue
            
            # Parsare sumară
            start_str, end_str = move_input.split()
            start = tuple(map(int, start_str.split(',')))
            end = tuple(map(int, end_str.split(',')))
            
            success = game.make_move(start, end)
            if not success:
                print("(!) Mutare ilegală. Reîncearcă.")
                
        except ValueError:
            print("(!) Format invalid. Folosește: row,col row,col")

if __name__ == "__main__":
    main()