from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class GameBoard:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None

    def get_board_markup(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for i in range(9):
            if self.board[i] == " ":
                builder.add(InlineKeyboardButton(text=" ", callback_data=f"move_{i}"))
            else:
                builder.add(InlineKeyboardButton(text=self.board[i], callback_data="ignore"))
        builder.adjust(3)
        return builder.as_markup()

    def get_board_text(self):
        board_text = ""
        for i in range(0, 9, 3):
            row = []
            for cell in self.board[i:i + 3]:
                if cell == ' ':
                    row.append('·')  # Заменяем пробел на точку
                else:
                    row.append(cell)
            board_text += " ".join(row) + "\n"
        return board_text.strip()

    def make_move(self, position: int) -> bool:
        if self.board[position] == " ":
            self.board[position] = self.current_player
            self.check_winner()
            if not self.winner:
                self.switch_player()
            return True
        return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтальные
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикальные
            [0, 4, 8], [2, 4, 6]  # Диагональные
        ]
        for combination in win_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != " ":
                self.winner = self.board[combination[0]]
                return

        if " " not in self.board:
            self.winner = "Draw"

    def reset(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None

    def to_dict(self) -> dict:
        """Сериализует объект GameBoard в словарь."""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'winner': self.winner
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Десериализует словарь в объект GameBoard."""
        instance = cls()
        instance.board = data.get('board', [" "] * 9)
        instance.current_player = data.get('current_player', "X")
        instance.winner = data.get('winner', None)
        return instance
