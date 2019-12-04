use itertools::Itertools;
use std::io::Read;
type Passord = Vec<u32>;

fn password_to_num(pass: &Passord) -> u32 {
    pass.iter().fold(0, |acc, digit| acc * 10 + digit)
}

fn part1(min_digits: Passord, max_digits: Passord) {
    let min_num = password_to_num(&min_digits);
    let max_num = password_to_num(&max_digits);
    let mut part1_counter = 0;
    let mut part2_counter = 0;
    for d1 in min_digits[0]..=max_digits[0] {
        for d2 in d1..=9 {
            for d3 in d2..=9 {
                for d4 in d3..=9 {
                    for d5 in d4..=9 {
                        for d6 in d5..=9 {
                            let password = vec![d1, d2, d3, d4, d5, d6];
                            if check_password(&password, min_num, max_num) {
                                part1_counter += 1
                            }
                            if check_part_2(&password, min_num, max_num) {
                                part2_counter += 1
                            }
                        }
                    }
                }
            }
        }
    }
    println!("Found {} matching passwords for part1", part1_counter);
    println!("Found {} matching passwords for part2", part2_counter);
}

fn check_part_2(password: &Passord, min_num: u32, max_num: u32) -> bool {
    if !password
        .iter()
        .group_by(|d| *d)
        .into_iter()
        .any(|(_k, group)| group.into_iter().map(|_| 1).sum::<i32>() == 2)
    {
        return false;
    }
    let num = password_to_num(&password);
    if !(min_num..=max_num).contains(&num) {
        return false;
    }
    true
}

fn check_password(password: &Passord, min_num: u32, max_num: u32) -> bool {
    if !password
        .iter()
        .zip(password.iter().skip(1))
        .any(|(d1, d2)| d1 == d2)
    {
        return false;
    }
    let num = password_to_num(&password);
    if !(min_num..=max_num).contains(&num) {
        return false;
    }
    true
}

fn main() {
    let mut buffer = String::new();
    std::io::stdin().read_to_string(&mut buffer).unwrap();
    let numbers = buffer.split("-").collect::<Vec<_>>();
    let min_password = numbers[0]
        .chars()
        .map(|c| c.to_string().parse().unwrap())
        .collect::<Passord>();
    let max_password = numbers[1]
        .chars()
        .map(|c| c.to_string().parse().unwrap())
        .collect::<Passord>();
    part1(min_password, max_password);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_match() {
        for (password, result) in vec![
            (vec![1, 2, 2, 3, 4, 5], true),
            (vec![1, 1, 1, 1, 2, 3], true),
            (vec![1, 3, 5, 6, 7, 9], false),
            (vec![1, 1, 1, 1, 1, 1], true),
            (vec![1, 2, 3, 7, 8, 9], false),
        ] {
            dbg!(&password);
            assert_eq!(check_password(&password, 0, 999999), result)
        }
    }
}
