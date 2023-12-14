import unittest
import tkinter as tk
from unittest.mock import MagicMock, patch
from memorygame import Card, MemoryGame

class TestMemoryGame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.geometry("1x1") 
        self.game = None  

    """Tearing it down"""
    def tearDown(self):
        if self.game:
            self.root.destroy()

    """
    Use the patch decorator from the unittest.mock library
    Patch the simpledialog.askstring method with predefined input values
    The side_effect parameter provides the values to be returned when askstring is called
    Create an instance of the MemoryGame class and assign it to the self.game attribute
    Pass the Tkinter root window (self.root) as the master parameter
    """
    def initialize_game(self, player1_name="PlayerTwo", player2_name="PlayerOne"):
        with patch("memorygame.simpledialog.askstring", side_effect=[player1_name, player2_name]):
            self.game = MemoryGame(self.root)

    """Test card initialization"""
    def test_card_initialization(self):
        """Checks if the game instance is not already initialized"""
        if not self.game:
            """If not initialized, set up the game with default player names"""
            self.initialize_game()
            
        """Creates a new Card instance with the breed Lab"""
        card = Card(self.root, self.game, "Lab")
        
        """Assert that the breed attribute of the card is set to Lab"""
        self.assertEqual(card.breed, "Lab")
        
        """Assert that the is_matched attribute of the card is initially False"""
        self.assertFalse(card.is_matched)
        
        """Assert that the is_flipped attribute of the card is initially False"""
        self.assertFalse(card.is_flipped)
        
    """Testing the flip card function"""
    def test_flip_card(self):
        """Checks if the game instance is not already initialized"""
        if not self.game:
            """f not initialized, set up the game with default player names"""
            self.initialize_game()
            
        """Creates a new Card instance with the breed Lab"""
        card = Card(self.root, self.game, "Lab")
        
        """Call the flip method on the card instance"""
        card.flip()
        
        """Assert that the is_flipped attribute of the card is True after calling flip"""
        self.assertTrue(card.is_flipped)
        
    """Checking if the game initialization"""
    def test_memory_game_initialization(self):
        if not self.game:
            """If not initialized, set up the game with default player names"""
            self.initialize_game()
            
        """Assert that current player is initialized to 1"""
        self.assertEqual(self.game.current_player, 1)
        
        """Assert that list of selected cards is initially empty"""
        self.assertEqual(len(self.game.selected_cards), 0)
        
        """Assert that first card in the game is an instance of the Card class"""
        self.assertTrue(isinstance(self.game.cards[0], Card))
    
    """Test to update the leadership board"""
    def test_update_leaderboard(self):
        if not self.game:
            self.initialize_game()

        """Ensure the leaderboard is initially empty"""
        self.assertEqual(len(self.game.leaderboard), 0)

        """Call update_leaderboard"""
        self.game.update_leaderboard()

        """Ensure the leaderboard is not empty after the update"""
        self.assertTrue(len(self.game.leaderboard) > 0)

if __name__ == "__main__":
    unittest.main()