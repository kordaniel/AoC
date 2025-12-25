use std::process;

use day_06_rust::io::utils::handle_args_load_puzzle_input;

#[derive(Clone, Copy)]
enum MathOperator {
    ADD,
    MUL,
}

impl std::fmt::Display for MathOperator {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> Result<(), std::fmt::Error> {
        match *self {
            Self::ADD => write!(f, "+"),
            Self::MUL => write!(f, "*"),
        }
    }
}
struct Problem {
    numbers: Vec<u32>,
    operator: MathOperator,
}

impl Problem {
    fn new(numbers: Vec<u32>, operator: MathOperator) -> Self {
        Self { numbers, operator }
    }

    fn solve(&self) -> u64 {
        match self.operator {
            MathOperator::ADD => self.numbers.iter().map(|n| u64::from(*n)).sum(),
            MathOperator::MUL => self.numbers.iter().map(|n| u64::from(*n)).product(),
        }
    }
}

struct InputData {
    problems: Vec<Problem>,
}

impl InputData {
    fn new(problems: Vec<Problem>) -> Self {
        Self { problems }
    }
}

fn parse_input(input_data: &Vec<String>) -> InputData {
    let operators = input_data.last()
        .expect("Invalid input, operators line missing")
        .split_whitespace()
        .map(|op| match op {
            "+" => MathOperator::ADD,
            "*" => MathOperator::MUL,
            _   => panic!("Invalid input..")
        });

    let mut row_iterators = input_data.iter()
            .take(input_data.len()-1)
            .map(|row| row
                .split_whitespace()
                .map(|val| val.parse::<u32>().expect("Encountered invalid u32 in input"))
            )
            .collect::<Vec<_>>();

    // Transpose of numbers grid
    let problems_numbers = std::iter::from_fn(move || {
        let mut column = Vec::with_capacity(row_iterators.len());

        for row in row_iterators.iter_mut() {
            match row.next() {
                Some(v) => column.push(v),
                None => {
                    println!("Discarded a column from the input due to to a shorter line");
                    return None;
                },
            }
        }

        Some(column)
    });

    // Assume both are of same length, even if a row might not contain all cols (TODO: check => panic)
    let problems = operators.into_iter()
        .zip(problems_numbers)
        .map(|(operator, numbers)| Problem::new(numbers, operator))
        .collect::<Vec<Problem>>();

    InputData::new(problems)
}

fn prob1(input: &InputData) -> u64 {
    input.problems.iter().map(|p| p.solve()).sum()
}

fn main() {
    let data = match handle_args_load_puzzle_input()  {
        Some(input_data) => input_data,
        None => process::exit(0),
    };

    let parsed_input = parse_input(&data);

    let prob1_res = prob1(&parsed_input);

    println!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 4076006202939u64);
}
