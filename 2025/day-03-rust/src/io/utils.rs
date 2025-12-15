const TEST_INPUT: [&str; 4] = [
    "987654321111111",
    "811111111111119",
    "234234234234278",
    "818181911112111"
];

enum InputDataSelection {
    FilePath(String),
    TestInput,
}

fn read_args() -> InputDataSelection {
  let cmd = clap::Command::new("AoC Day 3")
        .version("0.9")
        .author("kordaniel")
        .about(
            "Rust implementation of the solutions to the Advent of Code, day 3 challenges.\n\
             Uses the puzzles example input by default. Use the optional flag -i to specify a file containg your puzzle input."
        )
        .arg(
            clap::Arg::new("input fpath")
                .short('i')
                .long("input")
                .action(clap::ArgAction::Set)
                .value_name("FILE")
                .help("File path pointing to the input data")
        )
        .get_matches();

      let arg_fpath = cmd.get_one::<String>("input fpath");

      match arg_fpath {
        Some(filepath) => InputDataSelection::FilePath(filepath.to_string()),
        None => InputDataSelection::TestInput,
      }
}

pub fn handle_args_load_puzzle_input() -> Vec<String> {
    let input_fpath = read_args();

    match input_fpath {
      InputDataSelection::FilePath(fpath) => {
        println!("Reading input data from file '{}'.", fpath);
        read_input_file(&fpath)
      },
      InputDataSelection::TestInput => {
        println!("No input data file given, using example input data.");
        TEST_INPUT.iter()
          .map(|line| line.to_string())
          .collect()
      },
    }
}

pub fn read_input_file(fpath: &str) -> Vec<String> {
    std::fs::read_to_string(fpath)
        .expect(&format!("Unable to read file '{fpath}' into a UTF-8 string"))
        .lines()
        .map(|line| line.to_owned())
        .collect::<Vec<String>>()
}
