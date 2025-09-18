from app.components.base_puzzle import BasePuzzleInterface


class NormalPuzzleInterface(BasePuzzleInterface):
    """普通难度拼图 - 4x4 网格"""
    
    def __init__(self, parent=None):
        super().__init__(grid_size=4, object_name="normal-puzzle-interface", parent=parent)