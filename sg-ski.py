#!/usr/bin/env python

import sys

def parse_map_file(path):
    map_grid = []
    # Create a two-dimensional list based on the input data
    with open(path, 'r') as f:
        width, height = map(int, f.readline().split())
        for line in f:
            row = map(int, line.split())
            map_grid.append(row)
    # Input checking
    if height < 1 or width < 1:
        raise ValueError('grid height and width should be >= 1')
    elif height != len(map_grid) or width != len(map_grid[0]):
        raise ValueError('actual map does not match declared map dimensions')

    return width, height, map_grid


def make_grid(width, height, initial_value):
    return [width*[initial_value] for i in range(height)]


def get_length_and_elevation(x, y, map_grid, path_lengths, final_elevations):
    path_length = path_lengths[y][x]
    if path_length != -1:
        return path_length, final_elevations[y][x]

    current_elevation = map_grid[y][x]
    longest_path = 0
    lowest_elevation = current_elevation

    neighbors = [
        (x, y - 1), # up
        (x, y + 1), # down
        (x - 1, y), # left
        (x + 1, y), # right
    ]
    for xn, yn in neighbors:
        try:
            neighbor = map_grid[yn][xn]
        except IndexError:
            continue
        if neighbor < current_elevation:
            path_length, final_elevation = get_length_and_elevation(xn, yn, map_grid, path_lengths, final_elevations)
            if path_length > longest_path or (path_length == longest_path and final_elevation < lowest_elevation):
                longest_path = path_length
                lowest_elevation = final_elevation

    path_length = longest_path + 1
    path_lengths[y][x] = path_length
    final_elevations[y][x] = lowest_elevation
    return path_length, lowest_elevation


def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: {} <map file>'.format(sys.argv[0]))

    print 'Parsing map data...'
    try:
        width, height, map_grid = parse_map_file(sys.argv[1])
    except IOError as e:
        sys.exit('Unable to read map file: {}'.format(e))
    except ValueError as e:
        sys.exit('Invalid map file: {}: {}'.format(sys.argv[1], e))

    # Initialize corresponding grids for path lengths and final elevations
    path_lengths = make_grid(width, height, -1)
    final_elevations = make_grid(width, height, -1)

    print 'Finding the best path...'
    longest_path = -1
    steepest_drop = -1

    for y, row in enumerate(map_grid):
        for x, initial_elevation in enumerate(row):
            path_length, final_elevation = get_length_and_elevation(x, y, map_grid, path_lengths, final_elevations)
            drop = initial_elevation - final_elevation
            if path_length > longest_path or (path_length == longest_path and drop > steepest_drop):
                longest_path = path_length
                steepest_drop = drop

    print '\nlength = {}, drop = {}\n'.format(longest_path, steepest_drop)


if __name__ == '__main__':
    main()
