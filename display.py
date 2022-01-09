"""Display"""
import compute


def display_result(graph: compute.Graph, recommended_list: list) -> None:
    """Prints the recommended games with price, rating_score, and platform of each game.
    """
    for index, game in enumerate(recommended_list):
        game_vertex = graph.get_vertex(game, "game")
        print(f'{index + 1} {game}')
        print(f'\tprice: {game_vertex.price}')
        print(f'\trating_score: {game_vertex.rating_score}')
        print(f'\tplatform: {game_vertex.platform}')


# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'extra-imports': ['compute'],  # the names (strs) of imported modules
#         'allowed-io': [],  # the names (strs) of functions that call print/open/input
#         'max-line-length': 100,
#         'disable': ['E1136']
#     })
