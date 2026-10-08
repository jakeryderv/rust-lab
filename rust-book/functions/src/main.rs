fn main() {
    let x = plus_one(five() + five());
    println!("x = {x}");
}

fn plus_one(x: i32) -> i32 {
    x + 1
}

fn five() -> i32 {
    5
}
