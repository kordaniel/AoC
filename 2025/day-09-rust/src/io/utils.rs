use std::{
    env,
    fs,
};

const TEST_INPUT: [&str; 8] = [
    "7,1",
    "11,1",
    "11,7",
    "9,7",
    "9,5",
    "2,5",
    "2,3",
    "7,3"
];

const SUPPORTED_ARGS_MAP: [(&str, &str, &str, ArgumentType); 3] = [
    ("-d", "--dump        ", "Dump ASCII formatted result and exit", ArgumentType::DumpASCII),
    ("-i", "--input <FILE>", "File path pointing to the input data", ArgumentType::InputFile),
    ("-h", "--help        ", "Print help", ArgumentType::Help),
];

enum InputDataSelection {
    FilePath(String),
    TestInput,
}

#[derive(Debug)]
enum ArgumentType {
    DumpASCII,
    Help,
    InputFile,
}

struct Args {
    executable_fpath: String,
    input_data: InputDataSelection,
    invalid_arg: Option<String>,
    dump_ascii: bool,
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
    let mut has_dump_arg = false;
    let mut has_help_arg = false;
    let mut has_input_fpath: Option<&str> = None;
    let mut has_invalid_arg: Option<String> = None;

    let mut i = 0usize;
    while i < args.len() {
        let mut was_handled = false;
        let cur_arg = &args[i];

        for (short_fmt, long_fmt, _, arg_type) in SUPPORTED_ARGS_MAP {
            if cur_arg == short_fmt || cur_arg == long_fmt.split_whitespace().next().unwrap() {
                match arg_type {
                    ArgumentType::DumpASCII => has_dump_arg = true,
                    ArgumentType::Help => has_help_arg = true,
                    ArgumentType::InputFile if i+1 < args.len() => {
                        has_input_fpath = Some(&args[i+1]);
                        i += 1;
                    },
                    ArgumentType::InputFile =>
                        has_invalid_arg = Some(format!("Flag '{}' requires a file", cur_arg)),
                }
                was_handled = true;
                break;
            }
        }
        if !was_handled {
            has_invalid_arg = Some(cur_arg.to_owned());
            break;
        }
        i += 1;
    }

    Args {
        executable_fpath: exec_bin,
        input_data: match has_input_fpath {
            None => InputDataSelection::TestInput,
            Some(fpath) => InputDataSelection::FilePath(fpath.to_string()),
        },
        render_help: has_help_arg || has_invalid_arg.is_some(),
        dump_ascii: has_dump_arg,
        invalid_arg: has_invalid_arg,
    }
}

fn read_input_file(fpath: &str) -> Vec<String> {
    fs::read_to_string(fpath)
        .expect("Unable to read file '{fpath}' into a UTF-8 string")
        .lines()
        .map(|line| line.to_owned())
        .collect()
}

pub fn handle_args_load_puzzle_input() -> (bool, Option<Vec<String>>) {
    let parsed_args = read_args();

    if parsed_args.invalid_arg.is_some() {
        println!("Invalid argument: '{}'\n", parsed_args.invalid_arg.unwrap());
    }
    if parsed_args.render_help {
        println!("Rust implementation of the solutions to the Advent of Code, day 9 challenges.");
        println!("Uses the puzzles example input by default. Use the optional flag -i to specify a file containing your puzzle input.");
        println!("");
        print_usage(&parsed_args.executable_fpath);
        return (parsed_args.dump_ascii, None);
    }

    match parsed_args.input_data {
        InputDataSelection::FilePath(filepath) => {
            println!("Reading input data from file '{}'.", filepath);
            (parsed_args.dump_ascii, Some(read_input_file(&filepath)))
        },
        InputDataSelection::TestInput => {
            println!("No input data file given, using example input data.");
            (parsed_args.dump_ascii, Some(TEST_INPUT.iter()
                .map(|line| line.to_string())
                .collect::<Vec<String>>(),
            ))
        },
    }
}
