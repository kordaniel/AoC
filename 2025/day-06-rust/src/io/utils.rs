use std::{
    env,
    fs,
};

const TEST_INPUT: [&str; 4] = [
    "123 328  51 64 ",
    " 45 64  387 23 ",
    "  6 98  215 314",
    "*   +   *   +  "
];

const SUPPORTED_ARGS_MAP: [(&str, &str, &str, ArgumentType); 2] = [
    ("-i", "--input <FILE>", "File path pointing to the input data", ArgumentType::InputFile),
    ("-h", "--help        ", "Print help", ArgumentType::Help),
];

enum InputDataSelection {
    FilePath(String),
    TestInput,
}

#[derive(Debug)]
enum ArgumentType {
    Help,
    InputFile,
}

struct Args {
    executable_fpath: String,
    input_data: InputDataSelection,
    render_help: bool,
}

fn print_usage(exec_fpath: &str) {
    println!("Usage: {} [OPTIONS]", exec_fpath);
    println!("");
    for (short_fmt, long_fmt, help_text, _) in SUPPORTED_ARGS_MAP {
        println!("{}, {} {}", short_fmt, long_fmt, help_text);
    }
}

fn read_args() -> Args {
    let exec_bin: String = env::args().take(1).collect();
    let args: Vec<String> = env::args().skip(1).collect();
    let mut has_help_arg = false;
    let mut has_input_fpath: Option<&str> = None;

    let mut i = 0usize;
    while i < args.len() {
        let cur_arg = &args[i];

        for (short_fmt, long_fmt, _, arg_type) in SUPPORTED_ARGS_MAP {
            if cur_arg == short_fmt || cur_arg == long_fmt.split_whitespace().next().unwrap() {
                match arg_type {
                    ArgumentType::Help => {
                        has_help_arg = true;
                    },
                    ArgumentType::InputFile if i+1 < args.len() => {
                        has_input_fpath = Some(&args[i+1]);
                        i += 1;
                    },
                    ArgumentType::InputFile => {
                        print_usage(&exec_bin);
                        panic!("Error: Argument input file missing. Exiting.")
                    },
                }
                break;
            }
        }
        i += 1;
    }

    Args {
        executable_fpath: exec_bin,
        input_data: match has_input_fpath {
            None => InputDataSelection::TestInput,
            Some(fpath) => InputDataSelection::FilePath(fpath.to_string()),
        },
        render_help: has_help_arg,
    }
}

fn read_input_file(fpath: &str) -> Vec<String> {
    fs::read_to_string(fpath)
        .expect("Unable to read file '{fpath}' into a UTF-8 string")
        .lines()
        .map(|line| line.to_owned())
        .collect()
}

pub fn handle_args_load_puzzle_input() -> Option<Vec<String>> {
    let parsed_args = read_args();

    if parsed_args.render_help {
        println!("Rust implementation of the solutions to the Advent of Code, day 6 challenges.");
        println!("Uses the puzzles example by default. Use the optional flag -i to specify a file containing your puzzle input.");
        println!("");
        print_usage(&parsed_args.executable_fpath);
        return None;
    }

    match parsed_args.input_data {
        InputDataSelection::FilePath(filepath) => {
            println!("Reading input data from file '{}'.", filepath);
            Some(read_input_file(&filepath))
        },
        InputDataSelection::TestInput => {
            println!("No input data file given, using example input data.");
            Some(TEST_INPUT.iter()
                .map(|line| line.to_string())
                .collect::<Vec<String>>())
        },
    }
}
