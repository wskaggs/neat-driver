from pyray import *
import os


class TexturePack:
    """
    A singleton for managing raylib textures
    """
    _textures: dict[str, Texture] = {}

    @classmethod
    def load_all(cls, images_dir: str) -> None:
        """
        Load all textures from a directory

        This function assumes that all loaded textures have a different filename

        :param images_dir: the path to the images directory
        """
        for filename in os.listdir(images_dir):
            absolute_path = os.path.abspath(os.path.join(images_dir, filename))
            texture = load_texture(absolute_path)

            if is_texture_ready(texture):
                set_texture_filter(texture, TextureFilter.TEXTURE_FILTER_BILINEAR)
                cls._textures[filename] = texture

    @classmethod
    def unload_all(cls) -> None:
        """
        Unload all stored textures
        """
        for texture in cls._textures.values():
            unload_texture(texture)

        cls._textures.clear()

    @classmethod
    def get_texture(cls, filename: str) -> Texture:
        """
        Get a loaded texture

        :param filename: the filename of the texture to get
        :return: the loaded texture if found, None otherwise
        """
        return cls._textures.get(filename, None)
