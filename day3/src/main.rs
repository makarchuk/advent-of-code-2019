use std::io::{self, Read};

struct Path {
    parts: Vec<PathPart>,
}

impl Path {
    fn parse(input: &str) -> Self {
        input.split(',')
    }

    fn iter(&self) -> PathIter {
        PathIter {
            current_position: (0, 0),
            part_num: 0,
            part_distance: 0,
            path: &self,
        }
    }
}

type Position = (i128, i128);

struct PathPart {
    distance: u128,
    direction: Direction,
}

enum Direction {
    UP(),
    DOWN(),
    LEFT(),
    RIGHT(),
}

impl Direction() {
    fn step(&self, pos: Position) -> Position {
        let (x, y) = pos;
        match self {
            Self::UP() => (x, y + 1),
            Self::DOWN() => (x, y - 1),
            Self::LEFT() => (x - 1, y),
            Self::RIGHT() => (x + 1, y),
        }
    }
}

struct PathIter {
    path: &Path,
    part_num: usize,
    part_distance: i128,
    current_position: (i128, i128),
}

impl Iterator for PathIter {
    type Item = (i128, i128);

    fn next(&mut self) -> Option<Item> {
        if self.part_distance == self.path.parts[self.part_num].distance {
            if len(self.path.parts) == self.part_num - 1 {
                return None;
            } else {
                self.part_num += 1;
                self.part_distance = 0;
            }
        }
        let direction = self.path.parts[self.part_num].direction;
        self.part_distance += 1;
        self.current_position = direction.step(self.current_position);
        Some(self.current_position)
    }
}

fn intersections(first: &Path, second: &Path) {
    first
        .iter()
        .zip(second.iter())
        .filter(|(pos1, pos2)| pos1 == pos2)
        .collect::<Vec<_>>()
}

fn main() {
    let mut buffer = String::new();
    std::io::stdin().read_to_string(&mut buffer).unwrap();
}
