"""Compute"""

from __future__ import annotations
from typing import Any, Union, Optional


class _Vertex:
    """A vertex in a game graph, used to represent a developer, genre, category, or tag.

    Each vertex item is either a string represents developer, genre, category, or tag.

    Instance Attributes:
        - item: The data stored in this vertex with kind, representing
        a developer, category, genre, or tag. For example: ("Action", "genre")
        - kind: The type of this vertex: 'developer', 'category', 'genre' or 'tag'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - self.kind in {'developer', 'genre', 'category', 'tag'}
    """
    item: Any
    kind: str
    neighbours: set[_GameVertex]

    def __init__(self, item: Any, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'developer', 'genre', 'category', 'tag'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class _GameVertex(_Vertex):
    """A vertex in a game graph, used to represent a game.

    Each vertex item is a string represents game.

    Instance Attributes:
        - item: The data stored in this vertex, representing a game.
        - kind: The type of this vertex: 'game'.
        - price: The price of the game.
        - rating_score: The rating score of the game, calculated by
        positive ratings / (positive ratings + negative ratings).
        - platform: The platform the game can be played.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - self.kind == 'game'
    """
    item: Any
    kind: str
    price: float
    rating_score: float
    platform: list[str]
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str,
                 price: float, rating_score: float, platform: list[str]) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind == 'game'
        """
        _Vertex.__init__(self, item, kind)
        self.price = price
        self.rating_score = rating_score
        self.platform = platform

    def similarity_score(self, other: _GameVertex, kinds: list[str]) -> float:
        """Return the similarity score between this _GameVertex and the other _GameVertex.

        Similarity score is calculated by intersection of degree in kinds of both _GameVertex over
        union of the degree in kinds of both _GameVertex.
        """
        if self.degree() == 0 or other.degree() == 0:
            return 0.0

        intersect = set()
        union = {neighbour.item for neighbour in other.neighbours if neighbour.kind in kinds}
        for x in self.neighbours:
            if x.kind in kinds:
                union.add(x.item)
                if x in other.neighbours:
                    intersect.add(x.item)

        if len(union) == 0:
            return 0.0
        else:
            return len(intersect) / len(union)


############################################################################
# Graph
############################################################################

class Graph:
    """A graph used to represent a game network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, Union[_Vertex, _GameVertex]]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str,
                   price: Optional[float] = None, rating_score: Optional[float] = None,
                   platform: Optional[list[str]] = None) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'game', 'developer', 'genre', 'category', 'tag'}
        """
        if (item, kind) not in self._vertices:
            if kind == "game":
                self._vertices[(item, kind)] \
                    = _GameVertex((item, kind), kind, price, rating_score, platform)
            else:
                self._vertices[(item, kind)] = _Vertex((item, kind), kind)

    def add_edge(self, item1: Any, item2: Any, item1_kind: str, item2_kind: str) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if (item1, item1_kind) in self._vertices and (item2, item2_kind) in self._vertices:
            v1 = self._vertices[(item1, item1_kind)]
            v2 = self._vertices[(item2, item2_kind)]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any, item1_kind: str, item2_kind: str) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if (item1, item1_kind) in self._vertices and (item2, item2_kind) in self._vertices:
            v1 = self._vertices[(item1, item1_kind)]
            return any(v2.item == (item2, item2_kind) for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any, item_kind: str) -> set:
        """Return a set of the neighbours of the given item.

        Items are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if (item, item_kind) in self._vertices:
            v = self._vertices[(item, item_kind)]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'game', 'developer', 'genre', 'category', 'tag'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def get_filtered_game_vertices(self, max_price: Optional[float] = None,
                                   platforms: Optional[list[str]] = None,
                                   min_rating_score: Optional[float] = None) -> set:
        """Return a set of _GameVertex, only if _GameVertex met all the conditions
        inputted in the function. This includes max_price, platforms, and min_rating_score.
        """
        games_so_far = set()
        for v in self._vertices.values():
            if v.kind != "game":
                continue
            if max_price and v.price > max_price:
                continue
            if platforms and all([platform not in platforms for platform in v.platform]):
                continue
            if min_rating_score and v.rating_score < min_rating_score:
                continue
            games_so_far.add(v)

        return games_so_far

    def get_vertex(self, item: str, item_kind: str) -> Union[_GameVertex, _Vertex]:
        """Return the vertex of the given item.

        Raise ValueError if item not in self._vertices
        """
        if (item, item_kind) in self._vertices:
            return self._vertices[(item, item_kind)]
        else:
            raise ValueError

    def get_similarity_score(self, item1: Any, item2: Any,
                             item1_kind: str, item2_kind: str, kinds: list[str]) -> float:
        """Return the similarity score between the two given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.
        """
        if (item1, item1_kind) not in self._vertices or (item2, item2_kind) not in self._vertices:
            raise ValueError
        else:
            v1 = self._vertices[(item1, item1_kind)]
            v2 = self._vertices[(item2, item2_kind)]

            return v1.similarity_score(v2, kinds)

    ############################################################################
    # Recommend_Games
    ############################################################################
    def recommend_games(self, game: tuple[str, str],
                        kinds: list[str], max_price: Optional[float] = None,
                        platforms: Optional[list[str]] = None,
                        min_rating_score: Optional[float] = None) -> list[tuple]:
        """Return a list of recommended games based on similarity to the given game.

        input_game_list takes in value of (game_name, type)
        For example: ("Counter-Strike", "game")

        The return value is a list tuples of the titles of recommended games and similarity score,
        sorted in descending order of similarity score. Ties are broken in which game comes first.

        The returned list should NOT contain:
            - the input game itself
            - any game with a similarity score of 0 to the input game
            - any duplicates
            - any vertices that represents a developer, genre, category, or tag.

        Games returned starting with the game with the highest similarity score,
        then the second-highest similarity score, etc.

        Preconditions:
            - game in self._vertices
            - self._vertices[game].kind == 'game'
            - limit >= 1
        """
        all_games = self.get_filtered_game_vertices(max_price, platforms, min_rating_score)

        game_vertex = self.get_vertex(game[0], "game")
        if game_vertex in all_games:
            all_games.remove(game_vertex)

        game_dict = {}
        for game1 in all_games:
            similarity_score = \
                self.get_similarity_score(game[0], game1.item[0], "game", "game", kinds)
            if similarity_score == 0:
                continue
            elif similarity_score in game_dict:
                game_dict[similarity_score].append(game1.item[0])
            else:
                game_dict[similarity_score] = [game1.item[0]]

        list_of_games_with_score = []
        for score in sorted(game_dict.keys(), reverse=True):
            for game2 in sorted(game_dict[score]):
                list_of_games_with_score.append((game2, score))

        return list_of_games_with_score

    def recommend_multiple_games(self, input_game_list: list[tuple[str, str]], limit: int,
                                 kinds: list[str], max_price: Optional[float] = None,
                                 platforms: Optional[list[str]] = None,
                                 min_rating_score: Optional[float] = None) -> list[str]:
        """Return a list of up to <limit> recommended games based on similarity to the given game.

        input_game_list takes in value of [(game_name, type)]
        For example: [("Counter-Strike", "game"), ("Team Fortress Classic", "game")]

        The return value is a list of the titles of recommended games, sorted in descending order
        of the game appear frequency. Ties are broken in descending order of sum of the similarity
        score of the game. That is, if v1 and v2 have the same frequency, then v1 comes before v2
        if and only if v1's sum of similarity score > v2's sum of similarity score.

        The returned list should NOT contain:
            - the input game itself
            - any game with a similarity score of 0 to the input game
            - any duplicates
            - any vertices that represents a developer, genre, category, or tag.

        Up to <limit> books are returned, starting with the game with the highest frequency,
        then the second-highest frequency, etc. Fewer than <limit> games are returned if
        and only if there aren't enough games that meet the above criteria.

        Preconditions:
            - game in self._vertices
            - self._vertices[game].kind == 'game'
            - limit >= 1
        """
        list_of_games_with_score = []
        for game_tuple in input_game_list:
            list_of_games = \
                self.recommend_games(game_tuple, kinds, max_price, platforms, min_rating_score)
            list_of_games_with_score.extend(list_of_games)

        game_dict = {}
        for game_tup in list_of_games_with_score:
            if game_tup[0] in input_game_list:
                continue
            if game_tup[0] in game_dict:
                game_dict[game_tup[0]]["similarity_score"] += game_tup[1]
                game_dict[game_tup[0]]["counter"] += 1
            else:
                game_dict[game_tup[0]] = {"similarity_score": game_tup[1], "counter": 1}

        sorted_game_list = sorted(game_dict, key=lambda k: (game_dict[k]["counter"],
                                                            game_dict[k]["similarity_score"]),
                                  reverse=True)

        return sorted_game_list[:limit]


# if __name__ == '__main__':
#     import python_ta
#
#     python_ta.check_all(config={
#         'extra-imports': [],  # the names (strs) of imported modules
#         'allowed-io': [],  # the names (strs) of functions that call print/open/input
#         'max-line-length': 100,
#         'disable': ['E1136']
#     })
