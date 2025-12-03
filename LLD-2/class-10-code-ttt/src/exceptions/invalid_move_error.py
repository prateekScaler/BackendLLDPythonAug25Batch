class InvalidMoveError(Exception):
    def __init__(self, message="Invalid move"):
        self.message = message
        super().__init__(self.message)
