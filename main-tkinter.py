import tkinter as tk
from tkinter import font as tkFont
import random

class NimGame(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("950x900+450+0")
        self.title("Nim Game")
        
        self.theCanvas = tk.Canvas(self, width=800, height=900, bg="#ddddff")
        self.theCanvas.grid(row=0, column=0)
        self.buttonfont = tkFont.Font(family="Consolas", weight="bold")

        self.reset_button = tk.Button(self, text="Reset Game", font=self.buttonfont, command=self.reset_game)
        self.reset_button.grid(row=0, column=1)

        self.theCanvas.bind("<Motion>", self.mouseMoved)
        self.theCanvas.bind("<Button-1>", self.mouseClicked)

        self.canvasbutton = self.theCanvas.create_rectangle(150, 800, 250, 850, fill="blue", outline="black")
        self.theCanvas.create_text(200, 825, text="End Turn", font=self.buttonfont, fill="white")
        self.theCanvas.tag_bind(self.canvasbutton, "<Button-1>", self.canvasButtonClicked)
        
        self.movetext = None
        self.clickText = None
        self.buttonText = None
        self.turn_text = None
        self.stones = []
        self.is_player_turn = True
        self.selected_stones = 0
        
        self.DrawStones()
        self.update_turn_display()
        self.mainloop()

    def DrawStones(self):
        self.piles = [7, 5, 3, 1]
        x = 100
        self.stones = []
        
        for pile_idx, pilesize in enumerate(self.piles):
            pile_stones = []
            y = 100
            for i in range(pilesize):
                stone = self.theCanvas.create_oval(x-20, y-20, x+20, y+20, fill="gray", tags=f"pile{pile_idx}")
                self.theCanvas.tag_bind(stone, "<Button-1>", lambda e, p=pile_idx: self.select_stone(p))
                pile_stones.append(stone)
                y += 50
            self.stones.append(pile_stones)
            x += 100

    def select_stone(self, pile_idx):
        if self.is_player_turn and self.piles[pile_idx] > 0:
            self.selected_stones += 1
            self.piles[pile_idx] -= 1
            stone = self.stones[pile_idx].pop()
            self.theCanvas.delete(stone)
            self.update_status(f"Player removed stone from pile {pile_idx + 1}")
            self.check_game_state()
    def computer_move(self):
        available_piles = [i for i, size in enumerate(self.piles) if size > 0]
        if not available_piles:
            return
        
        pile = random.choice(available_piles)
        stones_to_remove = min(random.randint(1, 3), self.piles[pile])
        
        for _ in range(stones_to_remove):
            if self.piles[pile] > 0:
                self.piles[pile] -= 1
                stone = self.stones[pile].pop()
                self.theCanvas.delete(stone)
        
        self.update_status(f"Computer removed {stones_to_remove} stone(s) from pile {pile + 1}")
        self.after(1000, self.check_game_state)  
        self.is_player_turn = True
        self.update_turn_display()

    def mouseMoved(self, e):
        self.theCanvas.delete(self.movetext)
        self.movetext = self.theCanvas.create_text(20, 20, text=f"moved to {e.x}, {e.y}", anchor="nw")

    def mouseClicked(self, e):
        self.theCanvas.delete(self.clickText)
        self.clickText = self.theCanvas.create_text(750, 20, text=f"Clicked at {e.x}, {e.y}", anchor="ne")

    def canvasButtonClicked(self, e):
        if self.is_player_turn and self.selected_stones > 0:
            self.theCanvas.itemconfigure(self.canvasbutton, fill="green")
            self.after(500, self.restorebutton)
            self.is_player_turn = False
            self.selected_stones = 0
            self.update_turn_display()
            self.after(1000, self.computer_move)  # Computer moves after player

    def restorebutton(self):
        self.theCanvas.itemconfigure(self.canvasbutton, fill="blue")

    def update_turn_display(self):
        if sum(self.piles) > 0 :
            self.theCanvas.delete(self.turn_text)
            turn_msg = "Your Turn" if self.is_player_turn else "Computer's Turn"
            self.turn_text = self.theCanvas.create_text(400, 50, text=turn_msg, font=self.buttonfont, fill="black")

    def update_status(self, message):
        self.theCanvas.delete(self.buttonText)
        self.buttonText = self.theCanvas.create_text(400, 20, text=message, font=self.buttonfont)

    def check_game_state(self):
        if sum(self.piles) == 0:
            winner = "You Win!" if not self.is_player_turn else "Computer Wins!"
            self.theCanvas.delete(self.turn_text)
            self.turn_text = self.theCanvas.create_text(400, 50,text=winner, font=self.buttonfont, fill="red")
            self.theCanvas.unbind("<Button-1>")
            self.theCanvas.tag_unbind(self.canvasbutton, "<Button-1>")

    def reset_game(self):
        for pile in self.stones:
            for stone in pile:
                self.theCanvas.delete(stone)
        self.theCanvas.delete(self.turn_text)
        self.theCanvas.delete(self.buttonText)
        self.theCanvas.delete(self.clickText)
        self.theCanvas.delete(self.movetext)
        self.is_player_turn = True
        self.selected_stones = 0
        self.DrawStones()
        self.update_turn_display()
        self.theCanvas.bind("<Button-1>", self.mouseClicked)
        self.theCanvas.tag_bind(self.canvasbutton, "<Button-1>", self.canvasButtonClicked)

if __name__ == "__main__":
    app = NimGame()
