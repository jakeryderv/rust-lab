fn main() {
    let mut numbers = [1, 2, 3, 4, 5, 6];

    // 1. Create an immutable slice of the first 3 elements
    // Print the slice
    let first_half = &numbers[..3];
    println!("First half: {first_half:?}");

    // 2. Create a mutable slice of the last 3 elements
    // Double each element using a loop
    let second_half = &mut numbers[3..];

    for num in second_half.iter_mut() {
        *num *= 2;
    }

    // 3. Print the entire modified array
    println!("After doubling: {numbers:?}");

    // 4. Split the array into two mutable slices
    // Add 10 to every element in the left slice
    // Subtract 10 from every element in the right slice
    let (left, right) = numbers.split_at_mut(3);

    for num in left.iter_mut() {
        *num += 10;
    }

    for num in right.iter_mut() {
        *num -= 10;
    }

    // 5. Print the final array
    println!("Final: {numbers:?}");
}
