/*
 * Rust implementation of AoC 2025, Day 6 - Problem 2.
 * This implementation is intensionally over-engineered and does not focus on performance, especially
 * considering cache utilization during the parsing of the input data. The primary goal is to
 * explore rust concepts beyond the very basics and gather experience utilizing them.
 */

use std::{
    fmt,
    ops::{
        AddAssign,
        MulAssign,
        Shr,
    },
    process
};

use day_06_rust::io::utils::handle_args_load_puzzle_input;

#[derive(Clone, Copy, Debug)]
enum MathOperator {
    ADD,
    MUL,
}

impl fmt::Display for MathOperator {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> Result<(), fmt::Error> {
        match *self {
            Self::ADD => write!(f, "+"),
            Self::MUL => write!(f, "*"),
        }
    }
}

trait UnsignedInteger: AddAssign + Copy + MulAssign + PartialOrd + Shr<u32, Output = Self> {
    fn from_u8(n: u8) -> Self;
    fn max_val() -> Self;
    fn to_u64(self) -> u64;
    fn zero() -> Self;

    fn half_max() -> Self {
        Self::max_val() >> 1
    }
}

impl UnsignedInteger for u8 {
    fn from_u8(n: u8) -> Self { n }
    fn max_val() -> u8 { u8::MAX }
    fn to_u64(self) -> u64 { self as u64 }
    fn zero() -> Self { 0u8 }
}

impl UnsignedInteger for u16 {
    fn from_u8(n: u8) -> Self { n as u16 }
    fn max_val() -> u16 { u16::MAX }
    fn to_u64(self) -> u64 { self as u64 }
    fn zero() -> Self { 0u16 }
}

impl UnsignedInteger for u32 {
    fn from_u8(n: u8) -> Self { n as u32 }
    fn max_val() -> u32 { u32::MAX }
    fn to_u64(self) -> u64 { self as u64 }
    fn zero() -> Self { 0u32 }
}

impl UnsignedInteger for u64 {
    fn from_u8(n: u8) -> Self { n as u64 }
    fn max_val() -> u64 { u64::MAX }
    fn to_u64(self) -> u64 { self }
    fn zero() -> Self { 0u64 }
}

#[derive(Debug)]
struct Problem<T: UnsignedInteger> {
    numbers: Vec<T>,
    operator: MathOperator,
}

impl<T: UnsignedInteger> Problem<T>
{
    fn new(operator: MathOperator, numbers_cnt: usize) -> Self {
        Self {
            numbers: vec![T::zero(); numbers_cnt],
            operator
        }
    }

    fn from_input_data_rows<DT>(
        operator: MathOperator,
        col_width: usize, // NOTE: Includes col separator char ' '
        rows: &mut Vec<std::str::Chars<'_>>
    ) -> Problem<DT> where DT: UnsignedInteger {
        let mut new_prob = Problem::<DT>::new(operator, col_width-1);

        rows.iter_mut().for_each(|row| {
            for i in 0..col_width {
                let digit: u8 = match row.next() {
                    Some(d) if d != ' ' => d as u8 - b'0',
                    _ => continue,
                };
                new_prob.push_new_least_significant_digit(i, digit);
            }
        });

        new_prob
    }

    fn push_new_least_significant_digit(&mut self, num_i: usize, digit: u8) {
        if self.numbers[num_i] > T::half_max() {
            panic!("UnsignedInt overflow result when attempted to add a new digit to a too narrow uint type");
        }
        self.numbers[num_i] *= T::from_u8(10u8);
        self.numbers[num_i] += T::from_u8(digit);
    }

    fn solve(&self) -> u64 {
        let values = self.numbers
            .iter()
            .filter(|n| **n > T::zero())
            .map(|n| n.to_u64());

        match self.operator {
            MathOperator::ADD => values.sum(),
            MathOperator::MUL => values.product(),
        }
    }
}

enum InputData {
    Tiny(Vec<Problem<u8>>),
    Small(Vec<Problem<u16>>),
    Medium(Vec<Problem<u32>>),
    Large(Vec<Problem<u64>>)
}

impl InputData {
    fn new(max_digits_in_prob_num: usize) -> Self {
        match max_digits_in_prob_num {
            ..3   => InputData::Tiny(Vec::<Problem<u8>>::new()),
            3..5  => InputData::Small(Vec::<Problem<u16>>::new()),
            5..10 => InputData::Medium(Vec::<Problem<u32>>::new()),
            10..  => InputData::Large(Vec::<Problem<u64>>::new()),
        }
    }
}

fn parse_input(input_data: &Vec<String>) -> InputData {
    let digits_in_problem_num = input_data.len() - 1;
    let op_indexes_str = input_data.last().expect("Invalid input, operators line missing");
    let mut problems = InputData::new(digits_in_problem_num);

    let mut op_indexes = op_indexes_str
        .char_indices()
        .map(|(i, c)| match c {
            '+' => Some((i, MathOperator::ADD)),
            '*' => Some((i, MathOperator::MUL)),
            _   => None
        })
        .filter(|pair| pair.is_some())
        .map(|pair| pair.unwrap());

    let mut prev = match op_indexes.next() {
        Some(opi) => opi,
        None => panic!("Invalid state"),
    };

    let mut col_widths_operators = op_indexes.clone().map(|cur| {
        let new = (cur.0 - prev.0, prev.1);
        prev = cur;
        return new;
    }).collect::<Vec<_>>();

    col_widths_operators.push((op_indexes_str.len() + 1 - prev.0, op_indexes.last().unwrap().1));

    let mut rows = input_data.iter()
        .take(digits_in_problem_num)
        .map(|row| row.chars())
        .collect::<Vec<_>>();

    let mut col_width_op_iter = col_widths_operators.into_iter().peekable();

    while col_width_op_iter.peek().is_some() {
        let (col_width, op) = col_width_op_iter.next().unwrap(); // Includes col separator ' '
        match &mut problems {
            InputData::Tiny(probs) =>
                probs.push(Problem::<u8>::from_input_data_rows(op, col_width, &mut rows)),
            InputData::Small(probs) =>
                probs.push(Problem::<u16>::from_input_data_rows(op, col_width, &mut rows)),
            InputData::Medium(probs) =>
                probs.push(Problem::<u32>::from_input_data_rows(op, col_width, &mut rows)),
            InputData::Large(probs) =>
                probs.push(Problem::<u64>::from_input_data_rows(op, col_width, &mut rows)),
        }
    }

    problems
}

fn prob2(input: &InputData) -> u64 {
    match input {
        InputData::Tiny(probs) => probs.iter().map(|p| p.solve()).sum(),
        InputData::Small(probs) => probs.iter().map(|p| p.solve()).sum(),
        InputData::Medium(probs) => probs.iter().map(|p| p.solve()).sum(),
        InputData::Large(probs) => probs.iter().map(|p| p.solve()).sum(),
    }
}

fn main() {
    let data = match handle_args_load_puzzle_input()  {
        Some(input_data) => input_data,
        None => process::exit(0),
    };

    let parsed_input = parse_input(&data);

    let prob2_res = prob2(&parsed_input);

    println!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 7903168391557u64);
}
