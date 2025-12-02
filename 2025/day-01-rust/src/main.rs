use std::fs;

const TEST_INPUT: [&str; 10] = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"];

fn read_input_file(fpath: &str) -> Vec<String> {
    let data = fs::read_to_string(fpath)
        .expect(&format!("Unable to read file '{fpath}' into a UTF-8 string"));
    data
        .lines()
        .map(|line| line.to_owned())
        .collect::<Vec<String>>()
}

fn parse_input<I, S>(raw_input: I) -> Vec<(char, u32)> where
    I: IntoIterator<Item = S>,
    S: AsRef<str>
{
    let mut parsed: Vec<(char, u32)> = vec![];
    for row in raw_input {
        let dir = row.as_ref().chars().nth(0).unwrap();
        let val = row.as_ref().chars()
            .skip(1)
            .collect::<String>()
            .parse::<u32>()
            .expect("Input data contains an invalid line");
        parsed.push((dir, val));
    }
    parsed
}

fn prob_1(input: &Vec<(char, u32)>) -> u32 {
    let mut dial: i32 = 50;
    let mut zeros_count: u32 = 0;

    for (dir, val) in input {
        if *dir == 'L' {
            dial = (dial - (*val as i32)) % 100;
        } else if *dir == 'R' {
            dial = (dial + (*val as i32)) % 100;
        } else {
            panic!("Invalid input");
        }

        if dial == 0 {
            zeros_count += 1;
        }
    }

    zeros_count
}

fn prob_2(input: &Vec<(char, u32)>) -> u32 {
    let mut dial: i32 = 50;
    let mut zeros_count: u32 = 0;

    for (dir, val) in input {
        zeros_count += val / 100u32;
        let val_rem: i32 = (val % 100u32).try_into().unwrap();

        if *dir == 'L' {
            if dial != 0 && val_rem > dial {
                zeros_count += 1;
            }
            dial = (100 + dial - val_rem) % 100;
        } else if *dir == 'R' {
            if dial != 0 && val_rem > (100-dial) {
                zeros_count += 1;
            }
            dial = (dial + val_rem) % 100;
        } else {
            panic!("Invalid input");
        }

        if dial == 0 {
            zeros_count += 1;
        }
    }

    zeros_count
}

fn main() {
    let input = if true {
        parse_input(&read_input_file("./input.txt"))
    } else {
        parse_input(&TEST_INPUT)
    };

    println!("Prob 1: {}", prob_1(&input));
    println!("Prob 2: {}", prob_2(&input));
}
