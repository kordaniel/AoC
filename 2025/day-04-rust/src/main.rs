use std::fmt;

use day_04_rust::io::utils::handle_args_load_puzzle_input;

enum Cell {
    Empty,
    Roll,
}

impl fmt::Display for Cell {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> Result<(), fmt::Error> {
        match self {
            Cell::Empty => write!(f, "."),
            Cell::Roll  => write!(f, "@"),
        }
    }
}

struct GridRow(Vec<Cell>);
struct Grid(Vec<GridRow>);

impl fmt::Display for GridRow {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> Result<(), fmt::Error> {
        for c in &self.0 {
            write!(f, "{c}")?;
        }
        Ok(())
    }
}

impl fmt::Display for Grid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> Result<(), fmt::Error> {
        let rows = self.0.len();
        if rows == 0 {
            return Ok(());
        }
        let rows_col_width: usize = rows.ilog10() as usize + 1;

        let title_row = (0..self.0[0].0.len())
            .map(|n| u32::try_from(n).unwrap())
            .map(|n| char::from_digit(n, 16))
            .collect::<Option<String>>();
        let title_separator = std::iter::repeat_n('-', self.0[0].0.len()).collect::<String>();

        match title_row {
            None => (),
            Some(title) => {
                writeln!(f, "{:>width$}|{}", "", title, width = rows_col_width)?;
                writeln!(f, "{:>width$}+{}", "-", title_separator, width = rows_col_width)?;
            },
        }

        for (i, row) in (&self.0[..self.0.len()-1]).iter().enumerate() {
            writeln!(f, "{:>width$}|{row}", i, width = rows_col_width)?;
        }
        write!(f, "{:>width$}|{}", self.0.len()-1, self.0[self.0.len()-1], width = rows_col_width)?;

        Ok(())
    }
}

impl FromIterator<GridRow> for Grid {
    fn from_iter<T: IntoIterator<Item = GridRow>>(iter: T) -> Self {
        Self(iter.into_iter().collect())
    }
}

struct Matrix {
    data: Vec<u8>,
    height: usize,
    width: usize,
}

impl Matrix {
    fn new(height: usize, width: usize) -> Self {
        Self {
            data: vec![0u8; height * width],
            height,
            width
        }
    }

    fn get(&self, row: usize, col: usize) -> u8 {
        self.data[row * self.width + col]
    }

    fn set(&mut self, row: usize, col: usize, val: u8) {
        self.data[row * self.width + col] = val;
    }

    fn dec_by_one_if_positive(&mut self, row: usize, col: usize) {
        let prev_v = self.get(row, col);
        match prev_v {
            1.. => self.set(row, col, prev_v-1),
            0 => ()
        }
    }

}

impl fmt::Display for Matrix {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> Result<(), fmt::Error> {
        let output_radix = 16u32; // Assume all values are < 16. Larger values will break the formatting

        if std::cmp::max(self.width, self.height) > output_radix as usize {
            writeln!(f, "Matrix size exceeds display constraints and cannot be printed, size: ({}x{})", self.height, self.width)?;
            return Ok(());
        }

        let mut row_buf: Vec<char> = Vec::with_capacity(self.width);
        let title_row  = (0..self.width)
                .map(|n| u32::try_from(n).unwrap())
                .map(|n| char::from_digit(n, output_radix).unwrap())
                .collect::<String>();
        let title_separator = std::iter::repeat_n('-', self.width).collect::<String>();

        writeln!(f, " |{}", title_row)?;
        writeln!(f, "-+{}", title_separator)?;

        for y in 0..self.height {
            for x in 0..self.width {
                row_buf.push(char::from_digit(self.get(y, x).into(), output_radix).unwrap());
            }
            writeln!(f, "{}|{}", char::from_digit(y.try_into().unwrap(), output_radix).unwrap(), row_buf.iter().collect::<String>())?;
            row_buf.clear();
        }
        Ok(())
    }
}

fn parse_input<I, S>(raw_input: I) -> Grid where
    I: IntoIterator<Item = S>,
    S: AsRef<str>
{
    raw_input.into_iter()
        .map(|row| row.as_ref()
            .chars()
            .map(|cell_x| match cell_x {
                '@' => Cell::Roll,
                '.' => Cell::Empty,
                _ => panic!("Invalid input")
            })
            .collect::<Vec<Cell>>()
    )
    .map(|row| GridRow(row))
    .collect::<Grid>()
}

fn count_adjacent_rolls(grid: &Grid, y: usize, x: usize) -> u8 {
    let mut adjacent_rolls_count = 0;

    for dy in -1..=1isize {
        let y_pos = match y.checked_add_signed(dy) {
            Some(y_sum) if y_sum < grid.0.len() => y_sum,
            _ => continue,
        };

        for dx in -1..=1isize {
            if dy == 0 && dx == 0 {
                continue;
            }

            let x_pos = match x.checked_add_signed(dx) {
                Some(x_sum) if x_sum < grid.0[y_pos].0.len() => x_sum,
                _ => continue,
            };

            adjacent_rolls_count += match grid.0[y_pos].0[x_pos] {
                Cell::Empty => 0,
                Cell::Roll  => 1,
            };
        }
    }

    adjacent_rolls_count
}

fn prob1(input: &Grid, max_allowed_adjacent_rolls: u8) -> u32 {
    let mut accessible_rolls_count: u32 = 0;

    for y in 0..input.0.len() {
        let row = &input.0[y].0;
        for x in 0..row.len() {
            accessible_rolls_count += match row[x] {
                Cell::Roll if
                count_adjacent_rolls(input, y, x) < max_allowed_adjacent_rolls
                    => 1,
                _   => 0,
            };
        }
    }

    accessible_rolls_count
}

fn remove_roll(adjacent_rolls_cnt_map: &mut Matrix, y: usize, x: usize) {
    for dy in -1..=1isize {
        let y_pos = match y.checked_add_signed(dy) {
            Some(y_sum) if y_sum < adjacent_rolls_cnt_map.height => y_sum,
            _ => continue,
        };

        for dx in -1..=1isize {
            if dy == 0 && dx == 0 {
                continue;
            }

            let x_pos = match x.checked_add_signed(dx) {
                Some(x_sum) if x_sum < adjacent_rolls_cnt_map.width => x_sum,
                _ => continue,
            };
            adjacent_rolls_cnt_map.dec_by_one_if_positive(y_pos, x_pos);
        }
    }
}

fn remove_all_possible_rolls(
    grid: &mut Grid,
    adjacent_rolls_cnt_map: &mut Matrix,
    max_allowed_adjacent_rolls: u8
) -> u32 {
    let mut removed_rolls_count: u32 = 0;
    let mut done = false;

    while !done {
        done = true;
        for y in 0..adjacent_rolls_cnt_map.height {
            for x in 0..adjacent_rolls_cnt_map.width {
                match grid.0[y].0[x] {
                    Cell::Roll if adjacent_rolls_cnt_map.get(y, x) < max_allowed_adjacent_rolls => {
                        grid.0[y].0[x] = Cell::Empty;
                        remove_roll(adjacent_rolls_cnt_map, y, x);
                        removed_rolls_count += 1;
                        done = false;
                    },
                    _ => continue,
                }
            }
        }
    }

    removed_rolls_count
}

fn prob2(input: &mut Grid, max_allowed_adjacent_rolls: u8) -> u32 {
    let height = input.0.len();
    let width = input.0[0].0.len();
    let mut adjacent_rolls_count = Matrix::new(height, width);

    for y in 0..height {
        for x in 0..width {
            adjacent_rolls_count.set(y, x, count_adjacent_rolls(input, y, x));
        }
    }

    let removed_cnt = remove_all_possible_rolls(input, &mut adjacent_rolls_count, max_allowed_adjacent_rolls);

    println!("Prob 2 final grid:\n{}", input);
    println!("Prob 2 adjacent rolls count:\n{}", adjacent_rolls_count);

    removed_cnt
}

fn main() {
    let data = handle_args_load_puzzle_input();
    let mut parsed_input = parse_input(data);

    let prob1_res = prob1(&parsed_input, 4);
    let prob2_res = prob2(&mut parsed_input, 4);

    println!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 1411u32);
    println!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 8557u32);
}
