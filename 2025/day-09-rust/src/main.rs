use std::{
    cmp,
    collections::HashSet,
    io,
    process,
};

use crossterm::{
    event,
    execute,
    terminal::{
        EnterAlternateScreen,
        LeaveAlternateScreen,
        disable_raw_mode,
        enable_raw_mode,
    }
};
use ratatui::{
    Frame,
    Terminal,
    backend::{
        CrosstermBackend,
        TestBackend,
    },
    layout::{
        Constraint,
        Layout,
    },
    style::Color,
    widgets::{
        Block,
        Borders,
        canvas::{
            Canvas,
            Points,
            Rectangle,
        },
    },
};

use day_09_rust::io::utils::handle_args_load_puzzle_input;

#[derive(Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Point2D {
    y: usize,
    x: usize,
}

impl Point2D {
    fn new(x: usize, y: usize) -> Self {
        Self { y, x }
    }

    fn from(mut coords: impl Iterator<Item = usize>) -> Self {
        let x = coords.next().unwrap();
        let y = coords.next().unwrap();
        debug_assert_eq!(coords.next(), None);
        Self { y, x }
    }

    fn rectangle_size(&self, other: &Self) -> usize {
        (self.x.abs_diff(other.x) + 1) * (self.y.abs_diff(other.y) + 1)
    }

    fn rectangle_is_inside_polygon(&self, other: &Self, polygon_bounds: &HashSet<Self>) -> bool {
        let x_min = cmp::min(self.x, other.x);
        let x_max = cmp::max(self.x, other.x);
        let y_min = cmp::min(self.y, other.y);
        let y_max = cmp::max(self.y, other.y);

        for green_pnt in polygon_bounds {
            if x_min < green_pnt.x && green_pnt.x < x_max && y_min < green_pnt.y && green_pnt.y < y_max {
                return false;
            }
        }

        [
            Point2D::new(x_min, y_min),
            Point2D::new(x_min, y_max),
            Point2D::new(x_max, y_min),
            Point2D::new(x_max, y_max)
        ].map(|corner| polygon_bounds.contains(&corner))
            .into_iter()
            .filter(|on_bounds| *on_bounds)
            .count() != 4
    }
}

struct RectangleData {
    x: f64,
    y: f64,
    w: f64,
    h: f64,
}

fn parse_input(input_data: &Vec<String>) -> Vec<Point2D> {
    input_data.iter()
        .map(|row| row
            .trim()
            .split(',')
            .map(|coord| coord.parse::<usize>().expect("Invalid input: parsing red tile coords"))
        )
        .map(|coords| Point2D::from(coords))
        .collect::<Vec<_>>()
}

fn prob1(red_tiles: &Vec<Point2D>) -> usize {
    let mut rect_max_size = 0usize;
    let mut tiles_iter = red_tiles.iter();
    while let Some(tile) = tiles_iter.next() {
        let tiles_rest = tiles_iter.clone();
        for tile_pair in tiles_rest {
            rect_max_size = cmp::max(rect_max_size, tile.rectangle_size(tile_pair));
        }
    }
    rect_max_size
}

fn compute_polygon_boundaries_coords(red_tiles: &Vec<Point2D>) -> HashSet<Point2D> {
    let mut boundary_coords = HashSet::new();
    let mut pnt_a = red_tiles.iter().last().expect("Error: no red tiles in input");

    for pnt_b in red_tiles.iter() {
        if pnt_a.x == pnt_b.x {
            for y in cmp::min(pnt_a.y, pnt_b.y)..=cmp::max(pnt_a.y, pnt_b.y) {
                boundary_coords.insert(Point2D::new(pnt_a.x, y));
            }
        } else if pnt_a.y == pnt_b.y {
            for x in cmp::min(pnt_a.x, pnt_b.x)..=cmp::max(pnt_a.x, pnt_b.x) {
                boundary_coords.insert(Point2D::new(x, pnt_a.y));
            }
        } else {
            panic!("Invalid input");
        }
        pnt_a = pnt_b;
    }

    boundary_coords
}

fn prob2(red_tiles: &Vec<Point2D>) -> (usize, RectangleData) {
    let mut rect_max_size = 0usize;
    let mut corners: Option<(&Point2D, &Point2D)> = None;
    let green_tiles: HashSet<Point2D> = compute_polygon_boundaries_coords(red_tiles);
    let mut tiles_iter = red_tiles.iter();

    while let Some(pnt_a) = tiles_iter.next() {
        let tiles_rest = tiles_iter.clone();
        for pnt_b in tiles_rest {
            let rect_size = pnt_a.rectangle_size(pnt_b);
            if rect_size <= rect_max_size {
                continue;
            }
            if !pnt_a.rectangle_is_inside_polygon(pnt_b, &green_tiles) {
                continue;
            }
            rect_max_size = rect_size;
            corners = Some((pnt_a, pnt_b));
        }
    }

    if corners.is_none() {
        return (0, RectangleData { x: 0.0, y: 0.0, w: 0.0, h: 0.0 });
    }

    let (pnt_a, pnt_b) = corners.unwrap();
    let x = cmp::min(pnt_a.x, pnt_b.x);
    let y = cmp::min(pnt_a.y, pnt_b.y);
    let w = cmp::max(pnt_a.x, pnt_b.x) - x;
    let h = cmp::max(pnt_a.y, pnt_b.y) - y;
    (
        rect_max_size,
        RectangleData {
            x: x as f64,
            y: y as f64,
            w: w as f64,
            h: h as f64,
        }
    )
}

fn draw_canvas(
    frame: &mut Frame,
    block_text: &str,
    grid_width: f64,
    grid_height: f64,
    points: &Vec<(f64, f64)>,
    rect: &RectangleData,
    prob1_text: &str,
    prob2_text: &str
) {
    use Constraint::{Length, Min};
    let prob1_p = ratatui::widgets::Paragraph::new(prob1_text);
    let prob2_p = ratatui::widgets::Paragraph::new(prob2_text);

    let vertical = Layout::vertical([Length(1), Length(1), Min(0)]);
    let [prob1_area, prob2_area, canvas_area] = vertical.areas(frame.area());

    let canvas = Canvas::default()
        .block(Block::default().title(block_text).borders(Borders::ALL))
        .x_bounds([0.0, grid_width])
        .y_bounds([0.0, grid_height])
        .paint(|ctx| {
            ctx.draw(&Points::new(&points, Color::Red));
            ctx.draw(&Rectangle {
                x: rect.x,
                y: rect.y,
                width: rect.w,
                height: rect.h,
                color: Color::Yellow,
            });
        });

    frame.render_widget(prob1_p, prob1_area);
    frame.render_widget(prob2_p, prob2_area);
    frame.render_widget(canvas, canvas_area);
}

fn dump_result(
    grid_width: f64,
    grid_height: f64,
    red_points: &Vec<(f64, f64)>,
    rect: &RectangleData,
    prob1_text: &str,
    prob2_text: &str
) -> Result<(), Box<dyn std::error::Error>> {
    let backend = TestBackend::new(120, 52);
    let mut terminal = Terminal::new(backend)?;

    terminal.draw(|frame| {
        draw_canvas(frame,
            " Prob2 visualization ",
            grid_width,
            grid_height,
            red_points,
            rect,
            prob1_text,
            prob2_text
        );
    })?;

    let buff = terminal.backend().buffer();
    for y in buff.area.top()..buff.area.bottom() {
        for x in buff.area.left()..buff.area.right() {
            let cell = buff.cell(ratatui::layout::Position::new(x, y)).expect("Error dumping terminal buffer");
            print!("{}", cell.symbol());
        }
        println!();
    }
    Ok(())
}

fn run_ui(
    grid_width: f64,
    grid_height: f64,
    red_points: &Vec<(f64, f64)>,
    rect: &RectangleData,
    prob1_text: &str,
    prob2_text: &str
) -> Result<(), Box<dyn std::error::Error>> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen)?;

    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    loop {
        terminal.draw(|frame| {
            draw_canvas(
                frame,
                " Prob2 visualization (press any key to exit) ",
                grid_width,
                grid_height,
                red_points,
                rect,
                prob1_text,
                prob2_text
            );
        })?;

        std::thread::sleep(std::time::Duration::from_secs(1));

        if event::read()?.is_key_press() {
            break;
        }
    }

    disable_raw_mode()?;
    execute!(terminal.backend_mut(), LeaveAlternateScreen)?;

    Ok(())
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (dump_ascii, input_data) = handle_args_load_puzzle_input();
    let data = match input_data {
        Some(input_data) => input_data,
        None => process::exit(0),
    };

    let parsed_input = parse_input(&data);

    let prob1_res = prob1(&parsed_input);
    let (prob2_res, prob2_rect) = prob2(&parsed_input);

    let prob1_text = format!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 50usize || prob1_res == 4748826374usize);
    let prob2_text = format!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 24usize || prob2_res == 1554370486usize);

    let points = parsed_input.iter()
        .map(|p| (p.x as f64, p.y as f64))
        .collect::<Vec<_>>();
    let width = points.iter().map(|p| p.0).fold(0./0., f64::max);
    let height = points.iter().map(|p| p.1).fold(0./0., f64::max);

    if dump_ascii {
        dump_result(width, height, &points, &prob2_rect, prob1_text.as_str(), prob2_text.as_str())?;
    } else {
        run_ui(width, height, &points, &prob2_rect, prob1_text.as_str(), prob2_text.as_str())?;
    }

    Ok(())
}
