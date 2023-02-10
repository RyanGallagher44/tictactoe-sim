from random import randrange;
import matplotlib.pyplot as plt;
import numpy as np;

# simulates a random computer controlled game of Tic-Tac-Toe (3x3)
# returns a triple
# - grid when winner is determined
# - winner (X or O or Tie)
# - total moves during game
def simulate_random_game ():
    # original grid
    grid = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']
    ];

    # positions that X or O can choose from at random
    positions = [
        [0,0], [0,1], [0,2],
        [1,0], [1,1], [1,2],
        [2,0], [2,1], [2,2]
    ];

    # counter for game moves
    total_moves = 0;

    # loop that executes all 9 moves of the game
    # moves start with X, and then alternate O, X, O... until all 9 moves are complete
    while (total_moves < 9):
        random_pos = randrange(9 - total_moves);    # choose random position for move
        if (total_moves % 2 == 0): # if counter is even, X's turn
            grid[positions[random_pos][0]][positions[random_pos][1]] = 'X';
        else: # if counter is odd, O's turn
            grid[positions[random_pos][0]][positions[random_pos][1]] = 'O';
        positions.remove(positions[random_pos]); # remove position from positions as it has now been used
        total_moves = total_moves + 1; # increment game moves counter

        # check grid for winner on current move
        # if winner is determined, then stop the game and return the result
        # if winner is not determined, continue the gam
        if (determine_winner(grid, total_moves) != ''):
            break;

    return (grid, determine_winner(grid, total_moves), total_moves);

def determine_winner (grid, total_moves):
    winner = '';

    # checks every row for three of a kind
    for i in range(0,3):
        if (grid[i][0] == grid[i][1] and grid[i][1] == grid[i][2] and grid[i][2] != '_'):
            winner = grid[i][0];
            break;

    # checks every column for three of a kind
    for i in range(0,3):
        if (grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i] and grid[2][i] != '_'):
            winner = grid[0][i];
            break;

    # checks top-left to bottom-right diagonal for three of a kind
    if (grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2] and grid[2][2] != '_'):
        winner = grid[0][0];

    # checks bottom-left to top-right diagonal for three of a kind
    if (grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0] and grid[2][0] != '_'):
        winner = grid[0][0];

    # if moves are done and no winner determined, we have a tie
    if (winner == '' and total_moves == 9):
        winner = 'Tie'

    return winner;

def get_random_game_data():
    num_rand_games = 10000;
    total_moves = 0;
    num_times_x_won = 0;
    num_times_o_won = 0;
    num_times_tie = 0;
    for i in range(num_rand_games):
        game = simulate_random_game()
        if (game[1] == 'X'):
            num_times_x_won = num_times_x_won + 1;
        elif (game[1] == 'O'):
            num_times_o_won = num_times_o_won + 1;
        else:
            num_times_tie = num_times_tie + 1;
        total_moves = total_moves + game[2]

    print(f'x won {num_times_x_won}/{num_rand_games} - {num_times_x_won/num_rand_games*100}%');
    print(f'o won {num_times_o_won}/{num_rand_games} - {num_times_o_won/num_rand_games*100}%');
    print(f'tie occurred {num_times_tie}/{num_rand_games} - {num_times_tie/num_rand_games*100}%');
    print(f'avg. total moves/game - {total_moves/num_rand_games}');

    data = np.array([num_times_x_won, num_times_o_won, num_times_tie]);
    mylabels = [f'X - {num_times_x_won/num_rand_games*100}%', f'O - {num_times_o_won/num_rand_games*100}%', f'Tie - {num_times_tie/num_rand_games*100}%'];

    plt.pie(data, labels = mylabels);
    plt.show();

# get_random_game_data();

# find block opportunities for current move
def find_blocks (grid, opponent):
    blocks = [];
    for i in range(0,3):
        if (grid[i][0] == grid[i][1] and grid[i][1] == opponent and grid[i][2] == '_'):
            blocks.append([i, 2]);
        if (grid[i][0] == grid[i][2] and grid[i][2] == opponent and grid[i][1] == '_'):
            blocks.append([i, 1]);
        if (grid[i][1] == grid[i][2] and grid[i][2] == opponent and grid[i][0] == '_'):
            blocks.append([i, 0]);

    for i in range(0,3):
        if (grid[0][i] == grid[1][i] and grid[1][i] == opponent and grid[2][i] == '_'):
            blocks.append([2, i]);
        if (grid[0][i] == grid[2][i] and grid[2][i] == opponent and grid[1][i] == '_'):
            blocks.append([1, i]);
        if (grid[1][i] == grid[2][i] and grid[2][i] == opponent and grid[0][i] == '_'):
            blocks.append([0, i]);

    if (grid[0][0] == grid[1][1] and grid[1][1] == opponent and grid[2][2] == '_'):
        blocks.append([2, 2]);
    if (grid[1][1] == grid[2][2] and grid[2][2] == opponent and grid[0][0] == '_'):
        blocks.append([0, 0]);
    if (grid[0][0] == grid[2][2] and grid[2][2] == opponent and grid[1][1] == '_'):
        blocks.append([1, 1]);

    if (grid[0][2] == grid[1][1] and grid[1][1] == opponent and grid[2][0] == '_'):
        blocks.append([2, 0]);
    if (grid[2][0] == grid[0][2] and grid[0][2] == opponent and grid[1][1] == '_'):
        blocks.append([1, 1]);
    if (grid[2][0] == grid[1][1] and grid[2][2] == opponent and grid[0][2] == '_'):
        blocks.append([0, 2]);

    # remove duplicate block options
    *deduplicated_blocks,=map(list,{*map(tuple, blocks)});

    return deduplicated_blocks;

# find game winning opportunities for current move
def find_next_move (grid, you):
    moves = [];
    for i in range(0,3):
        if (grid[i][0] == grid[i][1] and grid[i][1] == you and grid[i][2] == '_'):
            moves.append([i, 2]);
        if (grid[i][0] == grid[i][2] and grid[i][2] == you and grid[i][1] == '_'):
            moves.append([i, 1]);
        if (grid[i][1] == grid[i][2] and grid[i][2] == you and grid[i][0] == '_'):
            moves.append([i, 0]);

    for i in range(0,3):
        if (grid[0][i] == grid[1][i] and grid[1][i] == you and grid[2][i] == '_'):
            moves.append([2, i]);
        if (grid[0][i] == grid[2][i] and grid[2][i] == you and grid[1][i] == '_'):
            moves.append([1, i]);
        if (grid[1][i] == grid[2][i] and grid[2][i] == you and grid[0][i] == '_'):
            moves.append([0, i]);

    if (grid[0][0] == grid[1][1] and grid[1][1] == you and grid[2][2] == '_'):
        moves.append([2, 2]);
    if (grid[1][1] == grid[2][2] and grid[2][2] == you and grid[0][0] == '_'):
        moves.append([0, 0]);
    if (grid[0][0] == grid[2][2] and grid[2][2] == you and grid[1][1] == '_'):
        moves.append([1, 1]);

    if (grid[0][2] == grid[1][1] and grid[1][1] == you and grid[2][0] == '_'):
        moves.append([2, 0]);
    if (grid[2][0] == grid[0][2] and grid[0][2] == you and grid[1][1] == '_'):
        moves.append([1, 1]);
    if (grid[2][0] == grid[1][1] and grid[2][2] == you and grid[0][2] == '_'):
        moves.append([0, 2]);

    # remove duplicate move options
    *deduplicated_moves,=map(list,{*map(tuple, moves)});

    return deduplicated_moves;

def find_adjacent_positions (grid, you):
    positions = [];
    for i in range(0,3):
        for j in range(0,3):
            if (grid[i][j] == you):
                if (i-1 >= 0 and j-1 >= 0):
                    if (grid[i-1][j-1] == '_'):
                        positions.append([i-1,j-1])
                if (i-1 >= 0 and j >= 0):
                    if (grid[i-1][j] == '_'):
                        positions.append([i-1,j])
                if (i >= 0 and j-1 >= 0):
                    if (grid[i][j-1] == '_'):
                        positions.append([i,j-1])
                if (i-1 >= 0 and j+1 <= 2):
                    if (grid[i-1][j+1] == '_'):
                        positions.append([i-1,j+1])
                if (i+1 <= 2 and j-1 >= 0):
                    if (grid[i+1][j-1] == '_'):
                        positions.append([i+1,j-1])
                if (i+1 <= 2 and j+1 <= 2):
                    if (grid[i+1][j+1] == '_'):
                        positions.append([i+1,j+1])
                if (i+1 <= 2 and j >= 0):
                    if (grid[i+1][j] == '_'):
                        positions.append([i+1,j])
                if (i >= 0 and j+1 <= 2):
                    if (grid[i][j+1] == '_'):
                        positions.append([i,j+1])

    *deduplicated_positions,=map(list,{*map(tuple, positions)});

    return deduplicated_positions;

def simulate_logical_game ():
    # original grid
    grid = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_']
    ];

    # positions that X or O can choose from
    positions = [
        [0,0], [0,1], [0,2],
        [1,0], [1,1], [1,2],
        [2,0], [2,1], [2,2]
    ];

    # counter for game moves
    total_moves = 0;

    # execute all 9 moves of the game
    # moves start with X, and then alternate O, X, O... until all 9 moves are complete
    while (total_moves < 9):
        if (total_moves < 3):
            random_pos = randrange(9 - total_moves); # choose random position for first move
            if (total_moves % 2 == 0):
                grid[positions[random_pos][0]][positions[random_pos][1]] = 'X';
            else:
                grid[positions[random_pos][0]][positions[random_pos][1]] = 'O';
            positions.remove(positions[random_pos]); # remove position from positions as it has now bee used
        else:
            random_pos = randrange(9 - total_moves);
            if (total_moves % 2 == 0): # X move
                if (len(find_blocks(grid, 'O')) != 0):
                    block_position = find_blocks(grid, 'O')[0];
                    first_index = block_position[0];
                    second_index = block_position[1];
                    grid[first_index][second_index] = 'X';
                    positions.remove(positions[positions.index(block_position)]);
                elif (len(find_next_move(grid, 'X')) != 0):
                    move_position = find_next_move(grid, 'X')[0];
                    first_index = move_position[0];
                    second_index = move_position[1];
                    grid[first_index][second_index] = 'X';
                    positions.remove(positions[positions.index(move_position)]);
                else:
                    move_position = find_adjacent_positions(grid, 'X')[0];
                    first_index = move_position[0];
                    second_index = move_position[1];
                    grid[first_index][second_index] = 'X';
                    positions.remove(positions[positions.index(move_position)]);
            else: # O move
                if (len(find_blocks(grid, 'X')) != 0):
                    block_position = find_blocks(grid, 'X')[0];
                    first_index = block_position[0];
                    second_index = block_position[1];
                    grid[first_index][second_index] = 'O';
                    positions.remove(positions[positions.index(block_position)]);
                elif (len(find_next_move(grid, 'O')) != 0):
                    move_position = find_next_move(grid, 'O')[0];
                    first_index = move_position[0];
                    second_index = move_position[1];
                    grid[first_index][second_index] = 'O';
                    positions.remove(positions[positions.index(move_position)]);
                else:
                    move_position = find_adjacent_positions(grid, 'O')[0];
                    first_index = move_position[0];
                    second_index = move_position[1];
                    grid[first_index][second_index] = 'O';
                    positions.remove(positions[positions.index(move_position)]);
            if (determine_winner(grid, total_moves) != ''):
                break;
        total_moves = total_moves + 1; # increment game moves counter

    return (grid, determine_winner(grid, total_moves), total_moves);

def get_logical_game_data():
    num_logical_games = 10000;
    total_moves = 0;
    num_times_x_won = 0;
    num_times_o_won = 0;
    num_times_tie = 0;
    for i in range(num_logical_games):
        game = simulate_logical_game()
        if (game[1] == 'X'):
            num_times_x_won = num_times_x_won + 1;
        elif (game[1] == 'O'):
            num_times_o_won = num_times_o_won + 1;
        else:
            num_times_tie = num_times_tie + 1;
        total_moves = total_moves + game[2]

    print(f'x won {num_times_x_won}/{num_logical_games} - {num_times_x_won/num_logical_games*100}%');
    print(f'o won {num_times_o_won}/{num_logical_games} - {num_times_o_won/num_logical_games*100}%');
    print(f'tie occurred {num_times_tie}/{num_logical_games} - {num_times_tie/num_logical_games*100}%');
    print(f'avg. total moves/game - {total_moves/num_logical_games}');

    data = np.array([num_times_x_won, num_times_o_won, num_times_tie]);
    mylabels = [f'X - {num_times_x_won/num_logical_games*100}%', f'O - {num_times_o_won/num_logical_games*100}%', f'Tie - {num_times_tie/num_logical_games*100}%'];

    plt.pie(data, labels = mylabels);
    plt.show();

get_logical_game_data();