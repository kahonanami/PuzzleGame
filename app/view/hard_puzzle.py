from app.components.base_puzzle import BasePuzzleInterface


class HardPuzzleInterface(BasePuzzleInterface):
    """困难难度拼图 - 6x6 网格"""
    
    def __init__(self, parent=None):
        super().__init__(grid_size=5, object_name="hard-puzzle-interface", parent=parent)