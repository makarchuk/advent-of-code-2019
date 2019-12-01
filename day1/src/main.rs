use std::cmp::max;
use std::io::{self, Read};

type Input = Vec<i128>;

fn fuel_to_lift(mass: i128) -> i128 {
    max(mass / 3 - 2, 0)
}

fn parse_input(input: String) -> Input {
    input
        .split('\n')
        .map(|chunk| chunk.parse().unwrap())
        .collect()
}

fn fuel_to_launch_modules(input: &Input) -> i128 {
    input.iter().map(|mass| fuel_to_lift(*mass)).sum()
}

fn part1(input: &Input) {
    println!("Total required fuel is: {}", fuel_to_launch_modules(input))
}

fn adjusted_fuel_mass(payload_mass: i128) -> i128 {
    let fuel_mass = fuel_to_lift(payload_mass);
    let mut total_fuel = fuel_mass;
    let mut adjustment = fuel_mass;
    loop {
        let mass_to_lift_fuel = fuel_to_lift(adjustment);
        total_fuel += mass_to_lift_fuel;
        adjustment = mass_to_lift_fuel;
        if adjustment == 0 {
            break;
        }
    }
    return total_fuel;
}

fn part2(input: &Input) {
    println!(
        "Adjusted total required fueld is: {}",
        input
            .iter()
            .map(|mass| adjusted_fuel_mass(*mass))
            .sum::<i128>()
    )
}

fn main() {
    let mut buffer = String::new();
    io::stdin().read_to_string(&mut buffer).unwrap();
    let input = parse_input(buffer);
    part1(&input);
    part2(&input);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_part_2() {
        for example in vec![(12, 2), (1969, 966), (100756, 50346)] {
            assert_eq!(adjusted_fuel_mass(example.0), example.1);
        }
    }
}
