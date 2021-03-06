"""
This file contains the Map object
"""

from wind import WindVane
from gps import GPS
from lidar import Lidar


def generate_world_map(gps_top_left=(42.293559, -71.263967), gps_bottom_right=(42.193559, -71.363967)):
    """
    Generates a map of the world - a 2d matrix where each cell is labeled as being land, water, or do not enter, and
    each cell represents a grid on a flat map of the world. All grids are uniform in their size as defined by their
    width and height in latitude and longitude.
    This function should be run with an internet connection. It will use an API to pull information from google maps
    about the region bounded by gps_top_left and gps_bottom_right, parse it, and pickle and store the information.
    Along with this matrix, there will also be information stored about the lat. and long. coordinates of each square
    in this matrix.
    :return: None
    """
    # TODO
    pass


def load_world_map():
    """
    Loads the world map that is generated by generate_world_map()
    :return: world_map
    """
    # TODO
    pass


class Map:
    """
    Handles the map of the world.
    On a global scale: has a start, destination, and a list of waypoints. Coord system: GPS coordinates
    On a local scale: has a 2D polar map of the world around the boat. Coord system: moves and oriented with the boat
    """

    def __init__(self):
        self.wind_vane = WindVane()
        self.gps = GPS()
        self.lidar = Lidar()
        self.world_map = load_world_map()

    def update_surroundings(self):
        """
        Updates the computer's knowledge of the surroundings.
        :return:
        """
        self.wind_vane.read_wind_vane()
        self.gps.read_gps()
        self.lidar.read_lidar()
        # TODO: There should be more going on here most likely


if __name__ == "__main__":
    generate_world_map()
