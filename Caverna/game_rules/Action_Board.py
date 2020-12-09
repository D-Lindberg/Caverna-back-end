from action_space_panels import PANELS

def generate_board_template(number_of_players):
    board = []
    if number_of_players == 7:
        board.extend(PANELS.Equals_7)
    if number_of_players == 5:
        board.extend(PANELS.Equals_5)
    if number_of_players > 5:
        board.extend(PANELS.More_Than_5)
    if number_of_players == 3:
        board.extend(PANELS.Equals_3)

    if number_of_players > 3:
        board.extend(PANELS.More_Than_3)
    else:
        board.extend(PANELS.Not_More_Than_3)

    if number_of_players == 2:
        board.extend(PANELS.Equals_2)
    else:
        board.extend(PANELS.Not_Equals_2)

    board.extend(PANELS.All)
    return board

