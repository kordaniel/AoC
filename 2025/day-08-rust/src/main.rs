use std::{
    cmp,
    collections::{
        BinaryHeap,
        HashSet,
    },
    fmt,
    process,
};

use day_08_rust::io::utils::handle_args_load_puzzle_input;

struct IdGenerator {
    next: usize,
}

impl IdGenerator {
    fn new() -> Self {
        Self { next: 0 }
    }

    fn next_id(&mut self) -> usize {
        let id = self.next;
        self.next += 1;
        id
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Point3D {
    id: usize,
    x: i64,
    y: i64,
    z: i64,
}

impl fmt::Display for Point3D {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "x={}, y={}, z={}", self.x, self.y, self.z)?;
        Ok(())
    }
}

impl Point3D {
    fn new(id: usize, coords: &mut dyn Iterator<Item = i64>) -> Self {
        Self {
            id,
            x: coords.next().expect("Invalid input: missing 'x' coord"),
            y: coords.next().expect("Invalid input: missing 'y' coord"),
            z: coords.next().expect("Invalid input: missing 'z' coord"),
        }
    }

    fn distance_to(&self, other: &Self) -> f64 {
        let x_res = (self.x - other.x).pow(2) as f64;
        let y_res = (self.y - other.y).pow(2) as f64;
        let z_res = (self.z - other.z).pow(2) as f64;
        (x_res + y_res + z_res).sqrt()
    }
}

#[derive(Clone, Debug)]
struct Edge {
    points: [Point3D; 2],
    distance: f64,
}

impl Edge {
    fn new(point_a: Point3D, point_b: Point3D, distance: f64) -> Self {
        Self {
            points: [point_a, point_b],
            distance
        }
    }
}

impl PartialEq for Edge {
    fn eq(&self, other: &Self) -> bool {
        (self.distance - other.distance).abs() < f64::EPSILON // FLOATS: Lazy implementation that suffices the needs for this task at hand
    }
}

impl Eq for Edge {}

impl Ord for Edge {
    fn cmp(&self, other: &Self) -> cmp::Ordering {
        // Rust BinaryHeap is a max heap => Inverse "natural" ordering
        match other.distance.partial_cmp(&self.distance) {
            Some(ord) => ord,
            None => panic!("Error in Edge Ord"),
        }
    }
}

impl PartialOrd for Edge {
    fn partial_cmp(&self, other: &Self) -> Option<cmp::Ordering> {
        Some(self.cmp(other))
    }
}

struct InputData {
    edges_dist_heap: BinaryHeap<Edge>, // Edge implements reversed ordering => MinHeap
}

fn parse_input(input_data: &Vec<String>) -> InputData {
    let mut id_generator = IdGenerator::new();

    let rows_iter = input_data.iter()
        .map(|row| row
            .split(',')
            .map(|coord| coord.trim())
            .map(|c| c.parse::<i64>().expect("Invalid input: integer coord"))
        );

    let points = rows_iter
        .map(|mut coords_iter| Point3D::new(
            id_generator.next_id(),
            &mut coords_iter
        ))
        .collect::<Vec<_>>();

    let mut edges_dist_heap: BinaryHeap<Edge> = BinaryHeap::new();
    for i in 0..(points.len()-1) {
        for j in (i+1)..points.len() {
            let pnt_a = points[i];
            let pnt_b = points[j];
            let dist = pnt_a.distance_to(&pnt_b);
            edges_dist_heap.push(Edge::new(pnt_a, pnt_b, dist));
        }
    }

    InputData { edges_dist_heap }
}

fn prob1(mut edges_dist_heap: BinaryHeap<Edge>, connections_cnt: usize) -> usize {
    let mut added_cnt = 0usize;
    let mut circuits: Vec<HashSet<usize>> = Vec::new();

    while added_cnt < connections_cnt {
        let edge = edges_dist_heap.pop().expect("Logic error: Cannot pop from empty heap");
        let a = edge.points[0].id;
        let b = edge.points[1].id;

        added_cnt += 1;
        let mut was_in_same_circuit = false;
        let mut circuit_i: (Option<usize>, Option<usize>) = (None, None);

        for (i, circuit) in circuits.iter().enumerate() {
            if circuit.contains(&a) {
                if circuit.contains(&b) {
                    was_in_same_circuit = true;
                    break;
                }
                if circuit_i.0 == None {
                    circuit_i.0 = Some(i);
                } else {
                    circuit_i.1 = Some(i);
                }
            } else if circuit.contains(&b) {
                if circuit_i.0 == None {
                    circuit_i.0 = Some(i);
                } else {
                    circuit_i.1 = Some(i);
                }
            }

            if circuit_i.0.is_some() && circuit_i.1.is_some() {
                break;
            }
        }

        if was_in_same_circuit {
            continue;
        }

        match circuit_i {
            (None, None) => circuits.push(HashSet::from([a, b])),
            (Some(i), None) => circuits[i].extend([a, b]),
            (Some(i), Some(j)) => {
                let min_i = cmp::min(i, j);
                let max_i = cmp::max(i, j);
                let (left, right) = circuits.split_at_mut(max_i);

                left[min_i].insert(a);
                left[min_i].insert(b);
                left[min_i].extend(right[0].iter());
                circuits.remove(max_i); // O(n)
            },
            _ => panic!("Logic error"),
        }
    }

    let mut circuits_sizes = circuits.iter()
        .map(|circuit| circuit.len())
        .collect::<Vec<_>>();
    circuits_sizes.sort_by(|a, b| b.cmp(a));

    circuits_sizes.iter().take(3).product::<usize>()
}

fn prob2(mut edges_dist_heap: BinaryHeap<Edge>) -> i64 {
    let mut last_added_pair: Option<(Point3D, Point3D)> = None;
    let mut circuits: Vec<HashSet<usize>> = Vec::new();

    while let Some(edge) = edges_dist_heap.pop() {
        let a = edge.points[0].id;
        let b = edge.points[1].id;
        let mut was_in_same_circuit = false;
        let mut circuit_i: (Option<usize>, Option<usize>) = (None, None);

        for (i, circuit) in circuits.iter().enumerate() {
            if circuit.contains(&a) {
                if circuit.contains(&b) {
                    was_in_same_circuit = true;
                    break;
                }
                if circuit_i.0 == None {
                    circuit_i.0 = Some(i);
                } else {
                    circuit_i.1 = Some(i);
                }
            } else if circuit.contains(&b) {
                if circuit_i.0 == None {
                    circuit_i.0 = Some(i);
                } else {
                    circuit_i.1 = Some(i);
                }
            }

            if circuit_i.0.is_some() && circuit_i.1.is_some() {
                break;
            }
        }

        if was_in_same_circuit {
            continue;
        }

        last_added_pair = Some((edge.points[0], edge.points[1]));

        match circuit_i {
            (None, None) => circuits.push(HashSet::from([a, b])),
            (Some(i), None) => circuits[i].extend([a, b]),
            (Some(i), Some(j)) => {
                let min_i = cmp::min(i, j);
                let max_i = cmp::max(i, j);
                let (left, right) = circuits.split_at_mut(max_i);

                left[min_i].extend([a, b]);
                left[min_i].extend(right[0].iter());
                right[0].clear(); // Leave empty sets in the Vec
            },
            _ => panic!("Logic error"),
        }
    }

    match last_added_pair {
        Some(pair) => pair.0.x * pair.1.x,
        None => 0,
    }
}

fn main() {
    // Lazy implementation that performs O(n) operations on Vec's instead of using smarter
    // bookkeeping of the states of the circuits. Runtime <0.5 seconds with the given input.
    let data = match handle_args_load_puzzle_input() {
        Some(input_data) => input_data,
        None => process::exit(0),
    };

    let parsed_input = parse_input(&data.0);

    let prob1_res = prob1(parsed_input.edges_dist_heap.clone(), if data.1 { 1000 } else { 10 });
    let prob2_res = prob2(parsed_input.edges_dist_heap);

    println!("Prob 1: {}. Correct? {}", prob1_res, prob1_res == 40usize || prob1_res == 164475usize);
    println!("Prob 2: {}. Correct? {}", prob2_res, prob2_res == 25272i64 || prob2_res == 169521198i64);
}
