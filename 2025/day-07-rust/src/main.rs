use std::{
    collections,
    fmt,
    process
};

use day_07_rust::io::utils::handle_args_load_puzzle_input;

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct Point2D {
    y: usize,
    x: usize,
}

impl Point2D {
    fn new(y: usize, x: usize) -> Self {
        Self { y, x }
    }
}

impl fmt::Display for Point2D {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({},{})", self.y, self.x)?;
        Ok(())
    }
}

#[derive(Clone, PartialEq)]
enum Cell {
    Beam,
    Empty,
    Splitter,
    Start,
}

impl Cell {
    fn from(c: char) -> Self {
        match c {
            '|' => Cell::Beam,
            '.' => Cell::Empty,
            '^' => Cell::Splitter,
            'S' => Cell::Start,
            _   => panic!("Invalid input: Contains invalid character: '{}'", c),
        }
    }
}

impl fmt::Display for Cell {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", match self {
            Cell::Beam => '|',
            Cell::Empty => '.',
            Cell::Splitter => '^',
            Cell::Start => 'S',
        })?;
        Ok(())
    }
}

#[derive(Clone)]
struct Grid(Vec<Vec<Cell>>);

impl fmt::Display for Grid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.0 {
            for col in row {
                write!(f, "{}", col)?;
            }
            writeln!(f, "")?;
        }
        Ok(())
    }
}

struct InputData {
    grid: Grid,
    start_pos: Point2D,
}

impl InputData {
    fn new(grid: Vec<Vec<Cell>>, start_pos: Point2D) -> Self {
        Self { grid: Grid(grid), start_pos }
    }
}

impl fmt::Display for InputData {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.grid.0 {
            for col in row {
                write!(f, "{}", col)?;
            }
            writeln!(f, "")?;
        }
        writeln!(f, "Start pos: {}", self.start_pos)?;
        Ok(())
    }
}

fn parse_input(input_data: &Vec<String>) -> InputData {
    let mut start_pos: Option<Point2D> = None;

    let grid = input_data
        .iter()
        .enumerate()
        .map(|(y, row)| row
            .chars()
            .enumerate()
            .map(|(x, c)| {
                let cur_cell = Cell::from(c);
                if cur_cell == Cell::Start {
                    if !start_pos.is_none() {
                        panic!("Invalid input: Contains several starting positions");
                    }
                    start_pos = Some(Point2D::new(y, x));
                }
                cur_cell
            })
            .collect::<Vec<_>>()
        )
        .collect::<Vec<_>>();

    InputData::new(grid, start_pos.expect("Invalid input: Missing starting position"))
}

fn prob1(grid: &mut Grid) -> u64 {
    let mut total_splits_cnt = 0u64;
    let cells = &mut grid.0;

    for y in 0..(cells.len()-1) {
        for x in 0..cells[y].len() {
            match cells[y][x] {
                Cell::Beam | Cell::Start => {
                    match cells[y+1][x] {
                        Cell::Beam => continue,
                        Cell::Empty => {
                            cells[y+1][x] = Cell::Beam;
                        },
                        Cell::Splitter => {
                            let mut beam_splitted = false;
                            if x > 0 && cells[y+1][x-1] == Cell::Empty {
                                beam_splitted = true;
                                cells[y+1][x-1] = Cell::Beam;
                            }
                            if x < cells[y].len()-1 && cells[y+1][x+1] == Cell::Empty {
                                beam_splitted = true;
                                cells[y+1][x+1] = Cell::Beam;
                            }
                            if beam_splitted {
                                total_splits_cnt += 1;
                            }
                        },
                        Cell::Start => continue,
                    }
                },
                _ => continue,
            }
        }
    }

    total_splits_cnt
}

fn count_total_timelines(grid: &Vec<Vec<Cell>>, pos: Point2D, cache: &mut collections::HashMap<Point2D, u64>) -> u64 {
    if let collections::hash_map::Entry::Occupied(entry) = cache.entry(pos) {
        return *entry.get();
    };
    if pos.y == grid.len()-1 {
        return 1;
    }

    let timelines_cnt = match grid[pos.y][pos.x] {
        Cell::Empty | Cell::Start => count_total_timelines(grid, Point2D::new(pos.y + 1, pos.x), cache),
        Cell::Splitter => {
            let mut cell_count = 0u64;
            if pos.x > 0 {
                cell_count += count_total_timelines(grid, Point2D::new(pos.y, pos.x - 1), cache);
            }
            if pos.x < grid[pos.y].len()-1 {
                cell_count += count_total_timelines(grid, Point2D::new(pos.y, pos.x + 1), cache);
            }
            cell_count
        },
        Cell::Beam => panic!("Prob2: Invalid grid state"),
    };

    cache.insert(pos, timelines_cnt);
    timelines_cnt
}

fn prob2(input_data: &InputData) -> u64 {
    let mut cache: collections::HashMap<Point2D, u64> = collections::HashMap::new();
    count_total_timelines(&input_data.grid.0, input_data.start_pos, &mut cache)
}

fn main() {
    let data = match handle_args_load_puzzle_input() {
        Some(input_data) => input_data,
        None => process::exit(0),
    };

    let parsed_input = parse_input(&data);
    let mut prob1_grid = parsed_input.grid.clone();

    let prob1_res = prob1(&mut prob1_grid);
    let prob2_res = prob2(&parsed_input);

    //println!("{}", prob1_grid);
    println!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 21u64 || prob1_res == 1672u64);
    println!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 40u64 || prob2_res == 231229866702355u64);
}
