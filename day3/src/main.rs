use std::collections::HashSet;
use std::io::Read;

struct Path {
    parts: Vec<PathPart>,
}

impl Path {
    fn parse(input: &str) -> Self {
        Path {
            parts: input
                .split(',')
                .map(|piece| PathPart::parse(piece))
                .collect(),
        }
    }

    fn iter(&self) -> PathIter {
        PathIter {
            current_position: Position { x: 0, y: 0 },
            part_num: 0,
            part_distance: 0,
            path: &self,
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, Hash)]
struct Position {
    x: i128,
    y: i128,
}

impl Position {
    fn manhattan_distance(&self) -> i128 {
        self.x.abs() + self.y.abs()
    }
}

#[derive(Debug, PartialEq)]
struct PathPart {
    distance: i128,
    direction: Direction,
}

impl PathPart {
    fn parse(input: &str) -> Self {
        let mut chars = input.chars();
        let direction = match chars.next().unwrap() {
            'U' => Direction::UP(),
            'D' => Direction::DOWN(),
            'L' => Direction::LEFT(),
            'R' => Direction::RIGHT(),
            _ => panic!("Invalid direction: {}", input),
        };
        Self {
            distance: chars.collect::<String>().parse().unwrap(),
            direction,
        }
    }
}

#[derive(Debug, PartialEq)]
enum Direction {
    UP(),
    DOWN(),
    LEFT(),
    RIGHT(),
}

impl Direction {
    fn step(&self, pos: &Position) -> Position {
        let &Position { x, y } = pos;
        match self {
            Self::UP() => Position { x, y: y + 1 },
            Self::DOWN() => Position { x, y: y - 1 },
            Self::LEFT() => Position { x: x - 1, y },
            Self::RIGHT() => Position { x: x + 1, y },
        }
    }
}

struct PathIter<'a> {
    path: &'a Path,
    part_num: usize,
    part_distance: i128,
    current_position: Position,
}

impl Iterator for PathIter<'_> {
    type Item = Position;

    fn next(&mut self) -> Option<Self::Item> {
        if self.part_distance == self.path.parts[self.part_num].distance {
            if self.part_num == self.path.parts.len() - 1 {
                return None;
            } else {
                self.part_num += 1;
                self.part_distance = 0;
            }
        }
        let direction = &self.path.parts[self.part_num].direction;
        self.part_distance += 1;
        self.current_position = direction.step(&self.current_position);
        Some(self.current_position.clone())
    }
}

fn intersections_with_delay(first: &Path, second: &Path) -> Vec<(Position, usize)> {
    let intersections = intersections(&first, &second);
    intersections
        .into_iter()
        .map(|int| {
            (
                int.clone(),
                first.iter().position(|pos| pos == int.clone()).unwrap()
                    + second.iter().position(|pos| pos == int.clone()).unwrap()
                    + 2,
            )
        })
        .collect()
}

fn intersections(first: &Path, second: &Path) -> Vec<Position> {
    first
        .iter()
        .collect::<HashSet<_>>()
        .intersection(&second.iter().collect())
        .map(|pos| pos.clone())
        .collect::<Vec<_>>()
}

fn part1(first: &Path, second: &Path) {
    let min_intersection = intersections(first, second)
        .iter()
        .map(|pos| pos.manhattan_distance())
        .min()
        .unwrap();
    println!("Closest intersection is {}", min_intersection)
}

fn part2(first: &Path, second: &Path) {
    let min_delay = intersections_with_delay(first, second)
        .iter()
        .min_by_key(|(_, delay)| delay)
        .unwrap()
        .1;
    println!("Minimum delay is: {}", min_delay);
}

fn main() {
    let mut buffer = String::new();
    std::io::stdin().read_to_string(&mut buffer).unwrap();
    let lines = buffer.split("\n").collect::<Vec<_>>();
    let first = Path::parse(lines[0]);
    let second = Path::parse(lines[1]);
    part1(&first, &second);
    part2(&first, &second);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_parse() {
        for (input, result) in vec![
            (
                "U128",
                PathPart {
                    direction: Direction::UP(),
                    distance: 128,
                },
            ),
            (
                "R999",
                PathPart {
                    direction: Direction::RIGHT(),
                    distance: 999,
                },
            ),
            (
                "D1",
                PathPart {
                    direction: Direction::DOWN(),
                    distance: 1,
                },
            ),
        ] {
            let part = PathPart::parse(input);
            assert_eq!(part, result)
        }
    }

    #[test]
    fn test_part1() {
        for (path1, path2, result) in vec![
            (
                "R75,D30,R83,U83,L12,D49,R71,U7,L72",
                "U62,R66,U55,R34,D71,R55,D58,R83",
                159,
            ),
            (
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
                135,
            ),
        ] {
            assert_eq!(
                intersections(&Path::parse(path1), &Path::parse(path2))
                    .iter()
                    .map(|pos| pos.manhattan_distance())
                    .min()
                    .unwrap(),
                result
            )
        }
    }

    #[test]
    fn test_part2() {
        for (path1, path2, result) in vec![
            (
                "R75,D30,R83,U83,L12,D49,R71,U7,L72",
                "U62,R66,U55,R34,D71,R55,D58,R83",
                610,
            ),
            (
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
                410,
            ),
        ] {
            assert_eq!(
                intersections_with_delay(&Path::parse(path1), &Path::parse(path2))
                    .iter()
                    .min_by_key(|(pos, delay)| delay)
                    .unwrap()
                    .1,
                result
            )
        }
    }
}
