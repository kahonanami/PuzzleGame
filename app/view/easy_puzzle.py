from app.components.base_puzzle import BasePuzzleInterface


class EasyPuzzleInterface(BasePuzzleInterface):
    """简单难度拼图 - 4x4 网格"""
    
    def __init__(self, parent=None):
        super().__init__(grid_size=3, object_name="easy-puzzle-interface", parent=parent)