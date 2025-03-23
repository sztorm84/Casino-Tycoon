from game import Game

def main():
    print("=== Casino Tycoon ===")
    
    game = Game()
    
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    finally:
        print("Thank you for playing Casino Tycoon!")

if __name__ == "__main__":
    main()