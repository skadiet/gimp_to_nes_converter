#!/path/to/bin/python

BYTES_PER_PIXEL = 3
PIXELS_PER_TILE_LENGTH = 8
PIXELS_PER_SCREEN_WIDTH = 256
PIXELS_PER_SCREEN_HEIGHT = 240
TILES_PER_SCREEN_WIDTH = int(PIXELS_PER_SCREEN_WIDTH / PIXELS_PER_TILE_LENGTH)
TILES_PER_SCREEN_HEIGHT = int(PIXELS_PER_SCREEN_HEIGHT / PIXELS_PER_TILE_LENGTH)
MAPPER = 'NROM'
CHR_FILENAME = '/path/to/gimp_to_nes_converter/basic/output.chr'
NAMETABLE_FILENAME = '/path/to/gimp_to_nes_converter/basic/background.i'
PICTURE_DATA_FILENAME = '/path/to/input/file/example_image.data'

COLOR_DICT = {'ffffff':0, 'ff0000':1, '00ff00':2, '0000ff':3}

#TODO: Add additional mapper support
MAPPER_DICT = {'NROM': 8192}

def main():
    raw_picture_data = import_raw_picture_data()
    tiles = get_tiles_for_rows(raw_picture_data)
    unique_tiles = get_unique_tiles(tiles)
    mymap = write_chr_data(unique_tiles)
    write_name_table(tiles, mymap)

def write_chr_data(unique_tiles):
    #TODO: Create a check to ensure that we do not exceed the maximum number of bytes
    chr_file_size = MAPPER_DICT[MAPPER]
    chr_end_of_file_padding = chr_file_size - len(unique_tiles) * 16
    n=BYTES_PER_PIXEL
    unique_tile_chr_position_map = {}
    with open(CHR_FILENAME, "wb") as f:
        for position, unique_tile in enumerate(unique_tiles):
            unique_tile_chr_position_map[unique_tile]=str(position)
            tile = bytearray(unique_tile)
            chunks = [tile[i:i+n] for i in range(0, len(tile), n)]
            tile = list(map(lambda x: COLOR_DICT[x.hex()], chunks))
            tile = filp_tile_vertically(tile)
            bit_plane_1, bit_plane_2 = split_tile_into_bit_planes(tile)
            f.write(bit_plane_1)
            f.write(bit_plane_2)
        f.write(int('00'*chr_end_of_file_padding, 16).to_bytes(chr_end_of_file_padding, byteorder='little'))
        return unique_tile_chr_position_map

def get_tiles_for_rows(rows):
    number_tiles = TILES_PER_SCREEN_WIDTH*TILES_PER_SCREEN_HEIGHT
    n=BYTES_PER_PIXEL*PIXELS_PER_TILE_LENGTH
    tiles = []
    [tiles.append(b'') for i in range(number_tiles)]
    row_counter = 0
    tile_index = 0
    for row in rows:
        chunks = [row[i:i+n] for i in range(0, len(row), n)]
        for tile_index_offset, chunk in enumerate(chunks):
            tiles[tile_index+tile_index_offset]+=chunk
        row_counter+=1
        if row_counter%PIXELS_PER_TILE_LENGTH == 0:
            tile_index+=TILES_PER_SCREEN_WIDTH
    return tiles

def split_tile_into_bit_planes(tile):
    bit_plane_1 = []
    bit_plane_2 = []
    for one_byte in tile:
        if one_byte==0:
            bit_plane_1.append('0')
            bit_plane_2.append('0')
        elif one_byte==1:
            bit_plane_1.append('1')
            bit_plane_2.append('0')
        elif one_byte==2:
            bit_plane_1.append('0')
            bit_plane_2.append('1')
        elif one_byte==3:
            bit_plane_1.append('1')
            bit_plane_2.append('1')
    bit_plane_1 = ''.join(bit_plane_1)
    bit_plane_2 = ''.join(bit_plane_2)
    bit_plane_1 = int(bit_plane_1, 2).to_bytes(PIXELS_PER_TILE_LENGTH, byteorder='little')
    bit_plane_2 = int(bit_plane_2, 2).to_bytes(PIXELS_PER_TILE_LENGTH, byteorder='little')
    return bit_plane_1, bit_plane_2

def get_unique_tiles(tiles):
    unique_tiles = set()
    for tile in tiles:
        unique_tiles.add(tile)
    return list(unique_tiles)

def filp_tile_vertically(tile):
    tile = [tile[line:line+8] for line in range(0,len(tile), 8)][::-1]
    return [item for sublist in tile for item in sublist]

def import_raw_picture_data():
    with open(PICTURE_DATA_FILENAME, "rb") as f:
        raw_data = []
        for i in range(PIXELS_PER_SCREEN_HEIGHT):
            line = f.read(BYTES_PER_PIXEL*PIXELS_PER_SCREEN_WIDTH)  #Read 3 bytes * 256 pixels
            raw_data.append(line)
    return raw_data

def write_name_table(tiles, mymap):
    with open(NAMETABLE_FILENAME, "w") as f:
        f.write('background1:\n')
        f.write('\n')
        tile_count = 0
        line = '  .db '
        for tile in tiles:
            tile_index = mymap[tile]
            line+= '$' + int(tile_index, 10).to_bytes(1, byteorder='little').hex()
            tile_count+=1
            if tile_count % 32 == 0:
                f.write(line+'\n')
                line = '  .db '
                f.write('\n')
            elif tile_count % 16 == 0:
                f.write(line+'\n')
                line = '  .db '
            else:
                line+=','

if __name__ == "__main__":
    main()
