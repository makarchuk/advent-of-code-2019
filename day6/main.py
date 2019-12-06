from collections import defaultdict
class Map:
    def __init__(self, input):
        super().__init__()
        self.orbits = {}
        self.reverse_orbits = defaultdict(list)
        for line in input.split('\n'):
            line = line.strip()
            if not line:
                continue
            center, orbit = line.split(')')
            self.orbits[orbit] = center
            self.reverse_orbits[center].append(orbit)

    def all_orbits(self):
        for orbit, center in self.orbits.items():
            yield orbit
            yield from self._recursive_orbits(orbit, center)

    def _recursive_orbits(self, orbit, current_ceneter):
        if current_ceneter in self.orbits:
            yield self.orbits[current_ceneter]
            yield from self._recursive_orbits(orbit, self.orbits[current_ceneter])

    def find_route(self, start="YOU", finish="SAN"):
        start = self.orbits[start]
        finish = self.orbits[finish]
        for path in  self._walk(current_route=(None, start)):
            if path[-1] == finish:
                return self._flatten_path(path)

    def _walk(self, current_route):
        possible_jumps = []
        location = current_route[-1]
        for jump in self._possible_jumps(location):
            if self._path_includes(current_route, jump):
                continue
            possible_jumps.append(jump)
            yield (current_route, jump)
        # print("Route: ", self._flatten_path(current_route), "Jumps:", possible_jumps)
        for jump in possible_jumps:
            yield from self._walk((current_route, jump))

    def _possible_jumps(self, location):
        if location in self.orbits:
            yield self.orbits[location]
        yield from self.reverse_orbits[location]

    @classmethod
    def _flatten_path(cls, path):
        result_path = []
        subpath, node = path
        if subpath is None:
            return [node]
        return cls._flatten_path(subpath) + [node]

    @classmethod
    def _path_includes(cls, path, node):
        return node in cls._flatten_path(path)

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(10000)
    with open('input') as f:
        orbit_map = Map(f.read())
    print("Total orbits: {}".format(len(list(orbit_map.all_orbits()))))
    route = orbit_map.find_route()
    print("Path from me to santa is {}. {} jumps".format(("->").join(route), len(route) - 1))