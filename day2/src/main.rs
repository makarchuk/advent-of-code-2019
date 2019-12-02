use std::io::{self, Read};

type State = Vec<i128>;

struct Program {
    state: State,
    position: usize,
}

impl Program {
    fn new(state: State) -> Self {
        Self { position: 0, state }
    }

    //step returns true if program had halted
    fn step(&mut self) -> bool {
        let op = self.pop();
        match op {
            1 => {
                let left = self.pop() as usize;
                let right = self.pop() as usize;
                let result = self.pop() as usize;
                self.state[result] = self.get(left) + self.get(right);
            }
            2 => {
                let left = self.pop() as usize;
                let right = self.pop() as usize;
                let result = self.pop() as usize;
                self.state[result] = self.get(left) * self.get(right);
            }
            99 => return true,
            _ => panic!("Unexpected operation: {}", op),
        }
        false
    }

    fn pop(&mut self) -> i128 {
        let val = self.state[self.position];
        self.position += 1;
        val
    }

    fn get(&self, pos: usize) -> i128 {
        self.state[pos]
    }

    fn run_until_complete(&mut self) {
        while !self.step() {}
    }
}

fn part1(original_state: &State) {
    let mut state = original_state.clone();
    state[1] = 12;
    state[2] = 2;
    let mut prog = Program::new(state);
    prog.run_until_complete();
    println!("Value at position 0 is: {}", prog.state[0]);
}

fn part2(original_state: &State) {
    for i in 0..=99 {
        for j in 0..=99 {
            let mut state = original_state.clone();
            state[1] = i;
            state[2] = j;
            let mut prog = Program::new(state);
            prog.run_until_complete();
            let output = prog.state[0];
            if output == 19690720 {
                println!("100*noun + verb = {}", 100 * i + j);
                break;
            }
        }
    }
}

fn main() {
    let mut buffer = String::new();
    std::io::stdin().read_to_string(&mut buffer).unwrap();
    let initial_state: State = buffer.split(",").map(|num| num.parse().unwrap()).collect();
    part1(&initial_state);
    part2(&initial_state);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part1() {
        for (original_state, final_state) in vec![
            (vec![1, 0, 0, 0, 99], vec![2, 0, 0, 0, 99]),
            (vec![2, 3, 0, 3, 99], vec![2, 3, 0, 6, 99]),
            (vec![2, 4, 4, 5, 99, 0], vec![2, 4, 4, 5, 99, 9801]),
            (
                vec![1, 1, 1, 4, 99, 5, 6, 0, 99],
                vec![30, 1, 1, 4, 2, 5, 6, 0, 99],
            ),
            (
                vec![1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
                vec![3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
            ),
        ] {
            let mut prog = Program::new(original_state);
            prog.run_until_complete();
            assert_eq!(prog.state, final_state)
        }
    }
}
