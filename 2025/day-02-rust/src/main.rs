use std::fs;

const TEST_INPUT: [&str; 11] = [
    "11-22",
    "95-115",
    "998-1012",
    "1188511880-1188511890",
    "222220-222224",
    "1698522-1698528",
    "446443-446449",
    "38593856-38593862",
    "565653-565659",
    "824824821-824824827",
    "2121212118-2121212124"
];

fn read_input_file(fpath: &str) -> Vec<String> {
    let data = fs::read_to_string(fpath)
        .expect(&format!("Unable to read file '{fpath}' into a UTF-8 string"));
    data
        .lines()
        .flat_map(|line| line
            .split(',')
            .map(|part| part.to_owned())
        )
        .collect::<Vec<String>>()
}

fn parse_input<I, S>(raw_input: I) -> Vec<(u64, u64)> where
    I: IntoIterator<Item = S>,
    S: AsRef<str>
{
    let mut parsed: Vec<(u64, u64)> = vec![];
    for row in raw_input {
        let mut parts = row.as_ref().split('-');
        parsed.push((
            parts.next().expect("Invalid row").parse::<u64>().expect("Invalid uint in row"),
            parts.next().expect("Invalid row").parse::<u64>().expect("Invalid uint in row")
        ));
    }
    parsed
}

fn is_part1_invalid_id(id: u64) -> bool {
    let str_id = id.to_string();
    let str_id_len = str_id.chars().count();

    if str_id_len % 2 != 0 {
        return false;
    }

    let half_str_id_len = str_id_len / 2;
    let a = &str_id[..half_str_id_len];
    let b = &str_id[half_str_id_len..];

    return a == b;
}

fn is_part2_invalid_id(id: u64) -> bool {
    let mut is_invalid = false;
    let str_id = id.to_string();
    let str_id_len = str_id.chars().count();

    (1..=(str_id_len/2)).for_each(|i| {
        let mut same = true;
        let slice = &str_id[0..i];

        for j in (i..=str_id_len).step_by(i) {
            if j+i > str_id_len || slice != &str_id[j..j+i] {
                same = false;
                break;
            } else if j+i == str_id_len {
                is_invalid = true;
                return;
            }
        }
        if same {
            is_invalid = true;
            return;
        }
    });

    is_invalid
}

fn count_invalid_ids(
    input: &Vec<(u64, u64)>,
    invalid_id_predicate: &dyn Fn(u64) -> bool
) -> u64 {
    let mut invalid_ids_sum: u64 = 0;
    for (start, end) in input {
        for id in *start..=*end {
            if invalid_id_predicate(id) {
                invalid_ids_sum += id;
            }
        }
    }

    invalid_ids_sum
}

fn main() {
    let input = if true {
        parse_input(&read_input_file("./input.txt"))
    } else {
        parse_input(&TEST_INPUT)
    };

    let prob1_res = count_invalid_ids(&input, &is_part1_invalid_id);
    let prob2_res = count_invalid_ids(&input, &is_part2_invalid_id);

    println!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 35367539282);
    println!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 45814076230u64);
}
