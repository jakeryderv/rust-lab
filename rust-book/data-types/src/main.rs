/*
*   two data type subsets: scalar & compound
*
*   rust is statically typed
*   must know the types of all var's at compile time
*
*   compiler can usually infer
*
*   scalar: represents single value
*       integers
*       floats
*       booleans
*       chars
*
*   compound: multiple values into one type
*       tuples
*       arrays
*/

#[allow(unused_variables)]
fn main() {
    println!("Min: {}", i32::MIN);
    println!("Max: {}", i32::MAX);
    println!("Bits: {}", i32::BITS);

    println!("Min: {}", f64::MIN);
    println!("Max: {}", f64::MAX);
    println!("Epsilon: {}", f64::EPSILON);
    println!("Digits: {}", f64::DIGITS);

    // addition
    let sum = 5 + 10;

    // subtraction
    let difference = 95.5 - 4.3;

    // multiplication
    let product = 4 * 30;

    // division
    let quotient = 56.7 / 32.2;
    let truncated = -5 / 3; // Results in -1

    // remainder
    let remainder = 43 % 5;
}
