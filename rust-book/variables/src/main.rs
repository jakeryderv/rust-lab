/*
*   "let" to declare variables
*       "let mut" for mutable variables
*       "let" on same variable to shadow it
*
*   "const" to declare constants
*       must be type annotated
*       any scope
*       only constant expressions
*/

// global const from const expression
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;

fn main() {
    println!("three hours in seconds: {THREE_HOURS_IN_SECONDS}");

    // mutable var
    let mut x = 5;
    println!("x = {x}");
    x += 1;
    println!("x = {x}");

    // immutable var
    let y = 10;
    println!("y = {y}");

    // shadow it in inner scope
    {
        let y = 20;
        println!("y = {y}");
    }

    // reverts to previous scope
    println!("y = {y}");

    // shadow it in same scope
    let y = 20;
    println!("y = {y}");

    // shadowing effectively creates a new variable when using "let" again
    // means we can change the type while using the same name
    let y = "jake";
    println!("y = {y}");
}
