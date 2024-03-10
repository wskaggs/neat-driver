import pyray as pr
from .texture_pack import TexturePack


class Track:
    """
    Class to represent a track, its valid play area, and its checkpoints
    """
    def __init__(self):
        """
        Constructor
        """
        self._design = TexturePack.get_texture("oval_track.png")
        self._play_area = TexturePack.get_texture("oval_track_valid.png")
        self._size = pr.Vector2(200, 100)

    def get_size(self) -> pr.Vector2:
        """
        Get the virtual size of this track

        :return: the (width, height) of this track in meters
        """
        return self._size

    def draw(self) -> None:
        """
        Draw this track to the screen
        """
        source_rect = pr.Rectangle(0, 0, self._design.width, self._design.height)
        dest_rect = pr.Rectangle(0, 0, self._size.x, self._size.y)
        pr.draw_texture_pro(self._design, source_rect, dest_rect, pr.Vector2(0, 0), 0, pr.WHITE)