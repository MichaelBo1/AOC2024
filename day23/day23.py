from collections import defaultdict
import sys
from typing import Dict, List, Set, Tuple

class Graph:
    def __init__(self) -> None:
        self.adj: Dict[str, Set[str]] = defaultdict(set)
        
    def add_edge(self, u: str, v: str) -> None:
        self.adj[u].add(v)
        self.adj[v].add(u)
        
    def _dfs(self, tmp: List[str], v: str, visited: Set[str]) -> List[str]:
        visited.add(v)
        tmp.append(v)
        for neighbour in self.adj.get(v, []):
            if neighbour not in visited:
                tmp = self._dfs(tmp, neighbour, visited)
                
        return tmp
        
    def find_triangles(self) -> Set[Tuple[str, str, str]]:
        triangles: Set[Tuple[str,str,str]] = set()
        for vertex in self.adj:
            neighbours = self.adj[vertex]
            for neighbour in neighbours:
                in_common = neighbours.intersection(self.adj[neighbour])
                for other in in_common:
                    triangles.add(tuple(sorted([vertex, neighbour, other])))
        
        return triangles
    
    def _find_cliques(self, potential_clique: List[str]=[], remaining: List[str]=[], skip: List[str]=[]) -> List[List[str]]:
        if len(remaining) == 0 and len(skip) == 0:
            return [potential_clique]
        
        cliques = []
        for vertex in remaining:
            new_potential_clique = potential_clique + [vertex]
            new_remaining = [n for n in remaining if n in self.adj[vertex]]
            new_skip = [n for n in skip if n in self.adj[vertex]]
            cliques.extend(self._find_cliques(new_potential_clique, new_remaining, new_skip))

            remaining.remove(vertex)
            skip.append(vertex)
        
        return cliques
    
    def max_clique(self) -> List[str]:
        cliques = self._find_cliques(remaining=[vertex for vertex in self.adj])
        return max(cliques, key=len)
    
    def __repr__(self) -> str:
        result = []
        for k,v in self.adj.items():
            result.append(f"{k}: {v}")
        return "\n".join(result)
    
def triangle_starts_with(triangle: Tuple[str, str, str], target="t") -> bool:
    for connection in triangle:
        if connection.startswith(target):
            return True
    return False

puzzle = open(sys.argv[1], "r").read().splitlines()

network = Graph()
for connection in puzzle:
    c1, c2 = connection.split("-")
    network.add_edge(u=c1, v=c2)

sets_of_three = network.find_triangles()
part1 = list(filter(triangle_starts_with, sets_of_three))
print(f"Part 1: {len(part1)}")
max_clique = network.max_clique()
part2 = ",".join(sorted(max_clique))
print(f"Part 2: {part2}")