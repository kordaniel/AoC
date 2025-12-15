use std::{
    cmp::max,
    collections::HashMap,
    io::{self, Write}
};

use day_03_rust::io::utils::handle_args_load_puzzle_input;

fn parse_input<I, S>(raw_input: I) -> Vec<Vec<u8>> where
    I: IntoIterator<Item = S>,
    S: AsRef<str>
{
    raw_input.into_iter()
        .map(|v| v.as_ref()
                .chars()
                .map(|c| (c as u8) - ('0' as u8) )
                .collect::<Vec<u8>>()
        )
        .collect::<Vec<Vec<u8>>>()
}

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct BankNode<'source> {
    pick_n_batts: u32,
    batts_bank: &'source [u8],
}

impl<'source> BankNode<'source> {
    fn new(batts_pick_left: u32, batts_bank: &'source [u8]) -> Self {
        Self { pick_n_batts: batts_pick_left, batts_bank }
    }
}

fn compute_bank_n_batts_max_joltage<'a>(bank_node: BankNode<'a>, cache: &mut HashMap<BankNode<'a>, u64>) -> u64 {
    if (bank_node.pick_n_batts as usize) > bank_node.batts_bank.len() {
        return 0u64;
    }
    if bank_node.pick_n_batts == 1 {
        let m = bank_node.batts_bank.iter().max().unwrap();
        return *m as u64;
    }
    let mut max_joltage: u64 = 0;

    for i in 0..bank_node.batts_bank.len() {
        let mut current = 10u64.pow(bank_node.pick_n_batts - 1) * (bank_node.batts_bank[i] as u64);
        let next = BankNode::new(bank_node.pick_n_batts - 1, &bank_node.batts_bank[i+1..]);

        let rest = match cache.entry(next) {
            std::collections::hash_map::Entry::Occupied(entry) => *entry.get(),
            std::collections::hash_map::Entry::Vacant(_) => compute_bank_n_batts_max_joltage(next, cache),
        };
        if rest == 0 {
            continue;
        }
        current += rest;
        max_joltage = max(current, max_joltage);
    }

    cache.insert(bank_node, max_joltage);

    max_joltage
}

fn compute_n_batts_combined_max_joltage(input: &Vec<Vec<u8>>, n_batteries: u32) -> u64 {
    let mut cache: HashMap<BankNode, u64> = HashMap::new();

    print!("Computing max total joltage for {n_batteries} batteries of each bank..");
    io::stdout().flush().unwrap();

    let total_joltage: u64 = input.iter()
        .map(|bank| compute_bank_n_batts_max_joltage(
            BankNode::new(n_batteries, bank), &mut cache
        ))
        .sum();

    println!(" Done");
    total_joltage
}

fn main() {
    let data = handle_args_load_puzzle_input();
    let parsed_input = parse_input(data);

    let prob1_res = compute_n_batts_combined_max_joltage(&parsed_input, 2);
    let prob2_res = compute_n_batts_combined_max_joltage(&parsed_input, 12);

    println!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 16993u64);
    println!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 168617068915447u64);
}
