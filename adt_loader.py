import numpy as np
import os
import struct

class ADTLoader:
    def __init__(self):
        self.chunk_size = 64  # The grid size of a WoW ADT chunk

    def load_adt(self, file_path):
        if not os.path.isfile(file_path) or not file_path.endswith(".adt"):
            print("Invalid ADT file!")
            return None

        try:
            with open(file_path, "rb") as f:
                # Parse the binary ADT file
                heightmap = self.parse_adt(f)
                return {"heightmap": heightmap}
        except Exception as e:
            print(f"Error reading ADT file: {e}")
            return None

    def parse_adt(self, file):
        """
        Parses the heightmap from an ADT file. This implementation assumes a simplified ADT
        and focuses on the heightmap data within MCNK chunks.
        """
        heightmap = np.zeros((self.chunk_size, self.chunk_size))

        while True:
            # Read 4 bytes to get the chunk name
            chunk_name = file.read(4)
            if len(chunk_name) < 4:
                break  # End of file

            # Read the size of the chunk
            chunk_size = struct.unpack("<I", file.read(4))[0]

            # Check if this is the MCNK chunk (terrain chunk)
            if chunk_name == b"MCNK":
                chunk_data = file.read(chunk_size)
                # Extract the heightmap data (145 floats, 8x8 grid + edges)
                heightmap = self.extract_heightmap(chunk_data)
            else:
                # Skip unknown chunks
                file.seek(chunk_size, os.SEEK_CUR)

        return heightmap

    def extract_heightmap(self, chunk_data):
        """
        Extracts the heightmap data from an MCNK chunk.
        """
        # Offset to the heightmap data in the MCNK chunk
        heightmap_offset = 128
        num_points = 145  # 17x17 grid (9x9 with edges for smoothing)
        raw_heights = struct.unpack("<" + "f" * num_points, chunk_data[heightmap_offset:heightmap_offset + num_points * 4])

        # Convert to a 2D grid (17x17)
        heightmap = np.array(raw_heights).reshape((17, 17))
        return heightmap