use std::{
    cmp::Ordering,
    process
};

use day_05_rust::io::utils::handle_args_load_puzzle_input;

struct IDRangeError(String);

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct IDRange {
    // NOTE: derived Ord compares fields in declaration order
    end: usize,
    start: usize,
}

impl IDRange {
    fn new(start: usize, end: usize) -> Result<Self, IDRangeError> {
        if start > end {
            return Err(IDRangeError("Invalid arguments for IDRange, start <= end must hold".to_string()));
        }
        Ok(Self { start, end })
    }

    fn includes_id(&self, id: &ID) -> bool {
        self.start <= id.0 && id.0 <= self.end
    }

    fn size(&self) -> usize {
        self.end - self.start + 1
    }
}

impl Ord for IDRange {
    fn cmp(&self, other: &Self) -> Ordering {
        self.start.cmp(&other.start).then_with(|| self.end.cmp(&other.end))
    }
}

impl PartialOrd for IDRange {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[derive(Debug, Eq, Ord, PartialEq, PartialOrd)]
struct ID(usize);

struct IngredientIDData {
    fresh_id_ranges: Vec<IDRange>,
    available_ids: Vec<ID>,
}

impl IngredientIDData {
    fn new(fresh_id_ranges: Vec<IDRange>, available_ids: Vec<ID>) -> Self {
        Self { fresh_id_ranges, available_ids }
    }
}

fn parse_input<'a, I, S>(input_data: I) -> IngredientIDData where
    I: IntoIterator<Item = &'a S>,
    S: AsRef<str> + 'a
{
    let mut id_ranges: Vec<IDRange> = Vec::new();
    let mut ids: Vec<ID> = Vec::new();

    let mut parsing_ranges = true;
    for line in input_data {
        let line_ref = line.as_ref();
        if line_ref.is_empty() {
            parsing_ranges = false;
            continue;
        }

        if parsing_ranges {
            let mut parts = line_ref
                .split('-')
                .map(str::trim)
                .map(|value| value.parse::<usize>().unwrap());
            match IDRange::new(parts.next().unwrap(), parts.next().unwrap()) {
                Ok(id_range) => id_ranges.push(id_range),
                Err(err) => panic!("Invalid input data: {}. Exiting.", err.0),
            }
        } else {
            ids.push(ID(line_ref.trim().parse::<usize>().unwrap()));
        }
    }

    id_ranges.sort();
    ids.sort();

    let mut combined_ids: Vec<IDRange> = Vec::with_capacity(id_ranges.len());
    combined_ids.push(id_ranges[0]);

    let mut i = 1;
    while i < id_ranges.len() {
        let prev_i = combined_ids.len()-1;
        let prev = &mut combined_ids[prev_i];
        let next = &id_ranges[i];

        if next.start <= prev.end {
            prev.end = std::cmp::max(prev.end, next.end);
        } else {
            combined_ids.push(*next);
        }
        i += 1;
    }

    IngredientIDData::new(combined_ids, ids)
}

fn prob1(input: &IngredientIDData) -> usize {
    let mut fresh_ids_cnt = 0usize;
    let mut start_i = 0usize;
    let id_ranges = &input.fresh_id_ranges;

    for id in &input.available_ids {
        for i in start_i..input.fresh_id_ranges.len() {
            if (&id_ranges[i]).includes_id(id) {
                fresh_ids_cnt += 1;
                start_i = i;
                break;
            }
        }
    }

    fresh_ids_cnt
}

fn prob2(input: &IngredientIDData) -> usize {
    input.fresh_id_ranges.iter()
        .map(|range| range.size())
        .sum()
}

fn main() {
    let data = match handle_args_load_puzzle_input() {
        Some(input_data) => input_data,
        None => process::exit(0),
    };
    let parsed_input = parse_input(&data);

    let prob1_res = prob1(&parsed_input);
    let prob2_res = prob2(&parsed_input);

    println!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 690usize);
    println!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 344323629240733usize);
}
