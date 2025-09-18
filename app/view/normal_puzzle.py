from app.components.base_puzzle import BasePuzzleInterface


class NormalPuzzleInterface(BasePuzzleInterface):
    """普通难度拼图 - 5x5 网格"""
    
    def __init__(self, parent=None):
        # 调用基类构造函数，设置为 5x5 网格
        super().__init__(grid_size=4, object_name="normal-puzzle-interface", parent=parent)