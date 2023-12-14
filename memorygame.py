"""
***************************************************************
* Name : Final Project - Memory Game
* Author: Tiffany Monroe
* Created : 12/13/2023
* Course: CIS 152 - Data Structure
* Version: 1.0
* OS: Windows 10
* IDE: Visual Studio Code
* Copyright : This is my own original work 
* based on specifications issued by our instructor
* Description : Application that has 6 matches and the player 
*             : who gets the most matches wins.
*            Input: Name
*            Output: GUI will show players name, current player 
*                 : turn, and a leadership board
* Academic Honesty: I attest that this is my original work.
* I have not used unauthorized source code, either modified or
* unmodified. I have not given other fellow student(s) access
* to my program.
***************************************************************
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class Card:
    def __init__(self, master, game, breed):
        """Initializing the card attributes"""
        self.master = master
        self.game = game
        self.breed = breed
        self.is_matched = False
        self.is_flipped = False

        """Setting up button appearance"""
        button_font = ("Helvetica", 18)
        button_width = 8
        button_height = 4

        self.button = tk.Button(master, text="?", width=button_width, height=button_height, font=button_font, command=self.flip)
        self.button.grid(row=0, column=0)
        self.show_back()
        
    """Showing the front of the card by setting button text to the breed"""
    def show_front(self):
        self.button.config(text=self.breed)
        
    """Showing the back of the card by setting button text to '?' """
    def show_back(self):
        self.button.config(text="?")

    """Flips the card only if it is not matched and not already flipped"""
    def flip(self):
        if not self.is_matched and not self.is_flipped:
            self.show_front()
            self.is_flipped = True
            self.game.check_match(self)

class MemoryGame:
    def __init__(self, master):
        """Initializes the memory game attributes"""
        self.master = master
        self.player1_name = self.get_player_name("Enter Player 1's name:")
        self.player2_name = self.get_player_name("Enter Player 2's name:")
        self.current_player = 1
        self.selected_cards = []
        self.create_cards()
        self.shuffle_cards()
        self.create_board()
        self.create_labels()
        self.leaderboard = []

        """Create a text widget for displaying the leaderboard"""
        self.leaderboard_text = tk.Text(self.master, height=10, width=40, font=("Helvetica", 14))
        self.leaderboard_text.grid(row=1, column=5, rowspan=6, padx=10, pady=10, sticky="e")

    """Get the player's name using a dialog box"""
    """Uses Input Validation. Will give an error message if user enters in anything other than letters"""
    def get_player_name(self, prompt):
        while True:
            player_name = simpledialog.askstring("Player Name", prompt)
            if player_name is None: 
                exit() 
            elif player_name.isalpha():
                return player_name
            else:
                messagebox.showerror("Error", "Please enter your name using only letters.")

    """Create a list of Card instances for different dogs and cats"""
    def create_cards(self):
        breeds = ["Beagle", "Pug", "Lab", "Persian", "Siamese", "Sphynx"]
        self.cards = [Card(self.master, self, breed) for breed in breeds * 2]

    """Shuffle the cards randomly"""
    def shuffle_cards(self):
        random.shuffle(self.cards)

    """Places card buttons in a grid"""
    def create_board(self):
        row, col = 1, 0
        for card in self.cards:
            card.button.grid(row=row, column=col, padx=20, pady=20)
            col += 1
            if col > 3:
                col = 0
                row += 1

    """Creates and place labels for player names, current player, and player turn"""
    def create_labels(self):
        player1_label = tk.Label(self.master, text=f"Player 1: {self.player1_name}")
        player1_label.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        player2_label = tk.Label(self.master, text=f"Player 2: {self.player2_name}")
        player2_label.grid(row=0, column=2, padx=5, pady=10, sticky="w")

        current_player_label = tk.Label(self.master, text="Current Player:")
        current_player_label.grid(row=0, column=4, padx=5, pady=10, sticky="e")

        self.player_turn_label = tk.Label(self.master, text=self.current_player_name())
        self.player_turn_label.grid(row=0, column=5, padx=5, pady=10, sticky="e")
        
        """Creates an Exit button and places it on the board"""
        exit_button = tk.Button(self.master, text="Exit Game", command=self.exit_game)
        exit_button.grid(row=7, column=4, padx=5, pady=10, sticky="e")

    """Determine the name of the current player"""
    def current_player_name(self):
        return self.player1_name if self.current_player == 1 else self.player2_name
    
    """Handle checking for a match when two cards are selected"""
    def check_match(self, card):
        self.selected_cards.append(card)
        if len(self.selected_cards) == 2:
            self.master.after(1000, self.check_match_after_delay)
            
    """Check for a match after a delay and handle flipping the cards back if no match is found"""
    def check_match_after_delay(self):
        if self.selected_cards[0].breed == self.selected_cards[1].breed:
            self.selected_cards[0].is_matched = True
            self.selected_cards[1].is_matched = True
            self.selected_cards = []
            self.check_winner()
        else:
            for card in self.selected_cards:
                card.show_back()
                card.is_flipped = False
            self.selected_cards = []
            self.switch_player()
            
    """Switch the current player"""
    def switch_player(self):
        self.current_player = 3 - self.current_player
        self.player_turn_label.config(text=self.current_player_name())
        
    """Checks if all cards are matched and update the leaderboard"""
    def check_winner(self):
        if all(card.is_matched for card in self.cards):
            self.update_leaderboard()
            self.display_leaderboard()
            
    """Updates the leaderboard with the current player's score"""
    def update_leaderboard(self):
        player_score = sum(card.is_matched for card in self.cards)
        self.leaderboard.append((self.current_player_name(), player_score))
        self.leaderboard.sort(key=lambda x: x[1], reverse=True)
        
    """Displays the leaderboard in the text widget"""
    def display_leaderboard(self):
        self.leaderboard_text.delete(1.0, tk.END)
        self.leaderboard_text.insert(tk.END, f"{'Player':<20}{'Cards Won'}\n")
        self.leaderboard_text.insert(tk.END, "="*30 + "\n")
        for rank, (player, score) in enumerate(self.leaderboard, start=1):
            self.leaderboard_text.insert(tk.END, f"{player:<20}{score}\n")
    
    """Exits the game"""
    def exit_game(self):
        self.master.destroy()

if __name__ == "__main__":
    """Creates the main window for the GUI"""
    root = tk.Tk()
    root.title("Memories Are Furever")
    root.geometry("950x550")
    
    """Create an instance of the MemoryGame class"""
    game = MemoryGame(root)

    """Center the board on the screen"""
    for i in range(6):  
        root.grid_rowconfigure(i, weight=1)
    for i in range(8):  
        root.grid_columnconfigure(i, weight=1)

    """Run the Tkinter event loop to start the GUI application"""
    root.mainloop()