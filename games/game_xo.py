from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class GameBoard:
    def __init__(self, size):
        self.size = size # Размер поля
        self.board = ["⬜"] * self.size ** 2 # Игровое поле
        self.current_player = "❌" # Текущий игрок
        self.win_length = 3 if self.size == 3 else 4 # Кол-во символов, идущих подряд для победы
        self.winner = None # Победитель

    def get_board_markup(self) -> InlineKeyboardMarkup:
        """
        Функция для отрисовки игрового поля
        :return:
        """
        builder = InlineKeyboardBuilder()
        for i in range(self.size ** 2):
            if self.board[i] == "⬜":
                builder.add(InlineKeyboardButton(text=" ⬜ ", callback_data=f"move_{i}", row_width=3))
            else:
                builder.add(InlineKeyboardButton(text=self.board[i], callback_data="ignore", row_width=3))
        builder.adjust(self.size)
        return builder.as_markup()

    def get_board_text(self):
        """
        Функция для получения поля в текстовом виде
        :return:
        """
        board_text = ""
        for i in range(0, self.size ** 2, self.size):
            row = []
            for cell in self.board[i:i + self.size]:
                if cell == ' ':
                    row.append('⬜')  # Заменяем пробел квадратом
                else:
                    row.append(cell)
            board_text += " ".join(row) + "\n"
        return board_text.strip()

    def make_move(self, position: int) -> bool:
        """
        Функция для имитации хода игрока
        :param position:
        :return:
        """
        if self.board[position] == "⬜":
            self.board[position] = self.current_player
            self.check_winner(position)
            if not self.winner:
                self.switch_player()
            return True
        return False

    def switch_player(self):
        """
        Функция для смены хода
        :return:
        """
        self.current_player = "⭕" if self.current_player == "❌" else "❌"

    def check_winner(self, last_move: int):
        """
        Функция для проверки победителя
        :param last_move:
        :return:
        """
        row = last_move // self.size  # Номер строки
        col = last_move % self.size  # Номер столбца
        player = self.board[last_move]  # Символ игрока, сделавшего ход

        # Проверяем горизонтальную, вертикальную и диагональные линии
        if (
            self.check_direction(row, col, 0, 1, player)  # Горизонтальная
            or self.check_direction(row, col, 1, 0, player)  # Вертикальная
            or self.check_direction(row, col, 1, 1, player)  # Главная диагональ
            or self.check_direction(row, col, 1, -1, player)  # Побочная диагональ
        ):
            self.winner = player
            return

        # Проверяем ничью
        if "⬜" not in self.board:
            self.winner = "Draw"

    def check_direction(self, row: int, col: int, d_row: int, d_col: int, player: str):
        """Проверяет линию от точки в двух направлениях."""
        count = 1  # Количество подряд стоящих символов игрока

        # Проверяем в одном направлении (d_row, d_col)
        count += self.count_in_direction(row, col, d_row, d_col, player)

        # Проверяем в противоположном направлении (-d_row, -d_col)
        count += self.count_in_direction(row, col, -d_row, -d_col, player)

        # Если количество подряд символов >= win_length, игрок победил
        return count >= self.win_length

    def count_in_direction(self, row: int, col: int, d_row: int, d_col: int, player: str):
        """Считает количество подряд символов игрока в одном направлении."""
        count = 0
        for _ in range(self.win_length - 1):  # Проверяем максимум win_length - 1 клеток
            row += d_row
            col += d_col
            if 0 <= row < self.size and 0 <= col < self.size:  # Проверяем, что не вышли за границы
                index = row * self.size + col
                if self.board[index] == player:
                    count += 1
                else:
                    break
            else:
                break
        return count

    def reset(self):
        """
        Функция для перезапуска игры
        :return:
        """
        self.board = ["⬜"] * self.size ** 2
        self.current_player = "❌"
        self.winner = None

    def to_dict(self) -> dict:
        """Сериализует объект GameBoard в словарь."""
        return {
            'board': self.board,
            'current_player': self.current_player,
            'winner': self.winner,
            'size': self.size
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Десериализует словарь в объект GameBoard."""
        size = data.get("size")
        instance = cls(size)
        instance.board = data.get('board', ["⬜"] * size ** 2)
        instance.current_player = data.get('current_player', "X")
        instance.winner = data.get('winner', None)
        return instance
