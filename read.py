"""Read"""
import pandas as pd
import compute


def read_process(input_csv: str) -> pd.DataFrame:
    """Return a data frame corresponding to steam.csv dataset.

    Given the steam.csv file, this function will filter out non-english games and select the
    columns that will be used in the recommendation app.

    This includes ['name', 'english', 'developer', 'platforms', 'categories', 'genres',
    'steamspy_tags', 'positive_ratings', 'negative_ratings', 'price'].

    This function will also create a new column named 'rating_score', that takes in the
    positive_ratings and negative_ratings of each game and get the total positive ratings
    percentage.

    Preconditions:
        - input_csv is the path to a CSV file corresponding to the steam.csv
    """
    # 1. Filter out non-english (assuming only support Eng games)
    df = pd.read_csv(input_csv,
                     usecols=['name', 'english', 'developer', 'platforms', 'categories', 'genres',
                              'steamspy_tags', 'positive_ratings', 'negative_ratings', 'price'])
    df = df.loc[df["english"] == 1]

    # 2. Rating score (derived from) positive ratings / (positive + negative ratings)
    df["rating_score"] \
        = df['positive_ratings'] / (df['positive_ratings'] + df['negative_ratings']) * 100

    return df


def load_game_graph(file: str) -> compute.Graph:
    """Return a game graph corresponding to the steam.csv.

    The load_game_graph stores one vertex for each game, developer, genre, category, and tag
    in the steam.csv dataset.

    Each vertex stores as its item either a game or developer or genre or category or tag. Game
    will be stored in _GameVertex while developer, genre, category, and tag will be stored in
    _Vertex. The "kind" _Vertex attribute will be used to differentiate between the four vertex
    types.

    Edges represent a connection between a game and a developer, genre, category, or tag.

    Preconditions:
        - input_csv is the path to a CSV file corresponding to the steam.csv
    """
    graph = compute.Graph()
    df = read_process(file)
    df.apply(lambda row: process_row(graph, row), axis=1)

    return graph


def process_row(graph: compute.Graph, row: pd.DataFrame) -> None:
    """A helper function for load_game_graph that process the dataframe given a row.

    Process_row will take in the game, developer, genre, category, and tag and create a vertex
    based on each kinds, and create an edge between the game and the kinds.
    """
    graph.add_vertex(row["name"], "game", row.price,
                     row.rating_score, row.platforms.split(";"))

    list_of_developers = row.developer.replace("/", ";").split(";")
    add_game_neighbours(graph, list_of_developers, "developer", row["name"])

    list_of_categories = row.categories.replace("/", ";").split(";")
    add_game_neighbours(graph, list_of_categories, "category", row["name"])

    list_of_tags = row.steamspy_tags.replace("/", ";").split(";")
    add_game_neighbours(graph, list_of_tags, "tag", row["name"])

    list_of_genres = row.genres.replace("/", ";").split(";")
    add_game_neighbours(graph, list_of_genres, "genre", row["name"])


def add_game_neighbours(graph: compute.Graph, vertex_list: list, kind: str, game: str) -> None:
    """A helper function for process_row to create a vertex for each kinds from a list,
    and create an edge between the game and the kinds.

    Preconditions:
        - all kind in vertex_list should be the same
        - kind in ['developer', 'genre', 'category', 'tag']
    """
    for element in vertex_list:
        graph.add_vertex(element, kind)
        graph.add_edge(game, element, "game", kind)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pandas', 'compute'],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['E1136']
    })
