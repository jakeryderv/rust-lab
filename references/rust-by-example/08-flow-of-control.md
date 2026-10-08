<a id="section-flow_control"></a>

<a id="section-flow_control--flow-of-control"></a>

# Flow of Control

[Chapter index](SUMMARY.md)

**In this chapter**

- [if/else](#section-flow_control-if_else)
- [loop](#section-flow_control-loop)
  - [Nesting and labels](#section-flow_control-loop-nested)
  - [Returning from loops](#section-flow_control-loop-return)
- [while](#section-flow_control-while)
- [for and range](#section-flow_control-for)
- [match](#section-flow_control-match)
  - [Destructuring](#section-flow_control-match-destructuring)
    - [tuples](#section-flow_control-match-destructuring-destructure_tuple)
    - [arrays/slices](#section-flow_control-match-destructuring-destructure_slice)
    - [enums](#section-flow_control-match-destructuring-destructure_enum)
    - [pointers/ref](#section-flow_control-match-destructuring-destructure_pointers)
    - [structs](#section-flow_control-match-destructuring-destructure_structures)
  - [Guards](#section-flow_control-match-guard)
  - [Binding](#section-flow_control-match-binding)
- [if let](#section-flow_control-if_let)
- [let-else](#section-flow_control-let_else)
- [while let](#section-flow_control-while_let)


An integral part of any programming language are ways to modify control flow:
`if`/`else`, `for`, and others. Let's talk about them in Rust.

<a id="section-flow_control-if_else"></a>

<a id="section-flow_control-if_else--ifelse"></a>

## if/else

Branching with `if`-`else` is similar to other languages. Unlike many of them,
the boolean condition doesn't need to be surrounded by parentheses, and each
condition is followed by a block. `if`-`else` conditionals are expressions,
and, all branches must return the same type.

```rust
fn main() {
    let n = 5;

    if n < 0 {
        print!("{} is negative", n);
    } else if n > 0 {
        print!("{} is positive", n);
    } else {
        print!("{} is zero", n);
    }

    let big_n =
        if n < 10 && n > -10 {
            println!(", and is a small number, increase ten-fold");

            // This expression returns an `i32`.
            10 * n
        } else {
            println!(", and is a big number, halve the number");

            // This expression must return an `i32` as well.
            n / 2
            // TODO ^ Try suppressing this expression with a semicolon.
        };
    //   ^ Don't forget to put a semicolon here! All `let` bindings need it.

    println!("{} -> {}", n, big_n);
}
```

<a id="section-flow_control-loop"></a>

<a id="section-flow_control-loop--loop"></a>

## loop

Rust provides a `loop` keyword to indicate an infinite loop.

The `break` statement can be used to exit a loop at anytime, whereas the
`continue` statement can be used to skip the rest of the iteration and start a
new one.

```rust
fn main() {
    let mut count = 0u32;

    println!("Let's count until infinity!");

    // Infinite loop
    loop {
        count += 1;

        if count == 3 {
            println!("three");

            // Skip the rest of this iteration
            continue;
        }

        println!("{}", count);

        if count == 5 {
            println!("OK, that's enough");

            // Exit this loop
            break;
        }
    }
}
```

<a id="section-flow_control-loop-nested"></a>

<a id="section-flow_control-loop-nested--nesting-and-labels"></a>

### Nesting and labels

It's possible to `break` or `continue` outer loops when dealing with nested
loops. In these cases, the loops must be annotated with some `'label`, and the
label must be passed to the `break`/`continue` statement.

```rust
#![allow(unreachable_code, unused_labels)]

fn main() {
    'outer: loop {
        println!("Entered the outer loop");

        'inner: loop {
            println!("Entered the inner loop");

            // This would break only the inner loop
            //break;

            // This breaks the outer loop
            break 'outer;
        }

        println!("This point will never be reached");
    }

    println!("Exited the outer loop");
}
```

<a id="section-flow_control-loop-return"></a>

<a id="section-flow_control-loop-return--returning-from-loops"></a>

### Returning from loops

One of the uses of a `loop` is to retry an operation until it succeeds. If the
operation returns a value though, you might need to pass it to the rest of the
code: put it after the `break`, and it will be returned by the `loop`
expression.

```rust
fn main() {
    let mut counter = 0;

    let result = loop {
        counter += 1;

        if counter == 10 {
            break counter * 2;
        }
    };

    assert_eq!(result, 20);
}
```

<a id="section-flow_control-while"></a>

<a id="section-flow_control-while--while"></a>

## while

The `while` keyword can be used to run a loop while a condition is true.

Let's write the infamous [FizzBuzz][section-flow_control-while-ref-1] using a `while` loop.

```rust
fn main() {
    // A counter variable
    let mut n = 1;

    // Loop while `n` is less than 101
    while n < 101 {
        if n % 15 == 0 {
            println!("fizzbuzz");
        } else if n % 3 == 0 {
            println!("fizz");
        } else if n % 5 == 0 {
            println!("buzz");
        } else {
            println!("{}", n);
        }

        // Increment counter
        n += 1;
    }
}
```

[section-flow_control-while-ref-1]: https://en.wikipedia.org/wiki/Fizz_buzz

<a id="section-flow_control-for"></a>

<a id="section-flow_control-for--for-loops"></a>

## for loops

<a id="section-flow_control-for--for-and-range"></a>

### for and range

The `for in` construct can be used to iterate through an `Iterator`.
One of the easiest ways to create an iterator is to use the range
notation `a..b`. This yields values from `a` (inclusive) to `b`
(exclusive) in steps of one.

Let's write FizzBuzz using `for` instead of `while`.

```rust
fn main() {
    // `n` will take the values: 1, 2, ..., 100 in each iteration
    for n in 1..101 {
        if n % 15 == 0 {
            println!("fizzbuzz");
        } else if n % 3 == 0 {
            println!("fizz");
        } else if n % 5 == 0 {
            println!("buzz");
        } else {
            println!("{}", n);
        }
    }
}
```

Alternatively, `a..=b` can be used for a range that is inclusive on both ends.
The above can be written as:

```rust
fn main() {
    // `n` will take the values: 1, 2, ..., 100 in each iteration
    for n in 1..=100 {
        if n % 15 == 0 {
            println!("fizzbuzz");
        } else if n % 3 == 0 {
            println!("fizz");
        } else if n % 5 == 0 {
            println!("buzz");
        } else {
            println!("{}", n);
        }
    }
}
```

Just remember that even though you can compile the code when `a>b`, the loop
gets never executed.

```rust
for i in 10..1 {
    println!("fizzbuzz");
}
```

If you want to count down, you need to use .rev() instead

```rust
for i in (1..10).rev() {
    println!("fizzbuzz");
}
```

<a id="section-flow_control-for--for-and-iterators"></a>

### for and iterators

The `for in` construct is able to interact with an `Iterator` in several ways.
As discussed in the section on the [Iterator][section-flow_control-for-ref-1] trait, by default the `for`
loop will apply the `into_iter` function to the collection. However, this is
not the only means of converting collections into iterators.

`into_iter`, `iter` and `iter_mut` all handle the conversion of a collection
into an iterator in different ways, by providing different views on the data
within.

* `iter` - This borrows each element of the collection through each iteration.
  Thus leaving the collection untouched and available for reuse after the loop.

```rust
fn main() {
    let names = vec!["Bob", "Frank", "Ferris"];

    for name in names.iter() {
        match name {
            &"Ferris" => println!("There is a rustacean among us!"),
            // TODO ^ Try deleting the & and matching just "Ferris"
            _ => println!("Hello {}", name),
        }
    }

    println!("names: {:?}", names);
}
```

* `into_iter` - This consumes the collection so that on each iteration the exact
  data is provided. Once the collection has been consumed it is no longer
  available for reuse as it has been 'moved' within the loop.

```rust
fn main() {
    let names = vec!["Bob", "Frank", "Ferris"];

    for name in names.into_iter() {
        match name {
            "Ferris" => println!("There is a rustacean among us!"),
            _ => println!("Hello {}", name),
        }
    }

    // `names` has been 'moved' and can no longer be used.
    // Try uncommenting the line below to see the compiler error:
    // println!("names: {:?}", names);
}
```

* `iter_mut` - This mutably borrows each element of the collection, allowing for
  the collection to be modified in place.

```rust
fn main() {
    let mut names = vec!["Bob", "Frank", "Ferris"];

    for name in names.iter_mut() {
        *name = match name {
            &mut "Ferris" => "There is a rustacean among us!",
            _ => "Hello",
        }
    }

    println!("names: {:?}", names);
}
```

In the above snippets note the type of `match` branch, that is the key
difference in the types of iteration. The difference in type then of course
implies differing actions that are able to be performed.

<a id="section-flow_control-for--see-also"></a>

#### See also:

[Iterator][section-flow_control-for-ref-1]

[section-flow_control-for-ref-1]: 16-traits.md#section-trait-iter

<a id="section-flow_control-match"></a>

<a id="section-flow_control-match--match"></a>

## match

Rust provides pattern matching via the `match` keyword, which can be used like
a C `switch`. The first matching arm is evaluated and all possible values must be
covered.

```rust
fn main() {
    let number = 13;
    // TODO ^ Try different values for `number`

    println!("Tell me about {}", number);
    match number {
        // Match a single value
        1 => println!("One!"),
        // Match several values
        2 | 3 | 5 | 7 | 11 => println!("This is a prime"),
        // TODO ^ Try adding 13 to the list of prime values
        // Match an inclusive range
        13..=19 => println!("A teen"),
        // Handle the rest of cases
        _ => println!("Ain't special"),
        // TODO ^ Try commenting out this catch-all arm
    }

    let boolean = true;
    // Match is an expression too
    let binary = match boolean {
        // The arms of a match must cover all the possible values
        false => 0,
        true => 1,
        // TODO ^ Try commenting out one of these arms
    };

    println!("{} -> {}", boolean, binary);
}
```

<a id="section-flow_control-match-destructuring"></a>

<a id="section-flow_control-match-destructuring--destructuring"></a>

### Destructuring

A `match` block can destructure items in a variety of ways.

* [Destructuring Tuples][section-flow_control-match-destructuring-ref-4]
* [Destructuring Arrays and Slices][section-flow_control-match-destructuring-ref-5]
* [Destructuring Enums][section-flow_control-match-destructuring-ref-1]
* [Destructuring Pointers][section-flow_control-match-destructuring-ref-2]
* [Destructuring Structures][section-flow_control-match-destructuring-ref-3]

[section-flow_control-match-destructuring-ref-1]: #section-flow_control-match-destructuring-destructure_enum
[section-flow_control-match-destructuring-ref-2]: #section-flow_control-match-destructuring-destructure_pointers
[section-flow_control-match-destructuring-ref-3]: #section-flow_control-match-destructuring-destructure_structures
[section-flow_control-match-destructuring-ref-4]: #section-flow_control-match-destructuring-destructure_tuple
[section-flow_control-match-destructuring-ref-5]: #section-flow_control-match-destructuring-destructure_slice

<a id="section-flow_control-match-destructuring--see-also"></a>

##### See also:

[The Rust Reference for Destructuring](https://doc.rust-lang.org/reference/patterns.html#r-patterns.destructure)

<a id="section-flow_control-match-destructuring-destructure_tuple"></a>

<a id="section-flow_control-match-destructuring-destructure_tuple--tuples"></a>

#### tuples

Tuples can be destructured in a `match` as follows:

```rust
fn main() {
    let triple = (0, -2, 3);
    // TODO ^ Try different values for `triple`

    println!("Tell me about {:?}", triple);
    // Match can be used to destructure a tuple
    match triple {
        // Destructure the second and third elements
        (0, y, z) => println!("First is `0`, `y` is {:?}, and `z` is {:?}", y, z),
        (1, ..)  => println!("First is `1` and the rest doesn't matter"),
        (.., 2)  => println!("last is `2` and the rest doesn't matter"),
        (3, .., 4)  => println!("First is `3`, last is `4`, and the rest doesn't matter"),
        // `..` can be used to ignore the rest of the tuple
        _      => println!("It doesn't matter what they are"),
        // `_` means don't bind the value to a variable
    }
}
```

<a id="section-flow_control-match-destructuring-destructure_tuple--see-also"></a>

###### See also:

[Tuples](02-primitives.md#section-primitives-tuples)

<a id="section-flow_control-match-destructuring-destructure_slice"></a>

<a id="section-flow_control-match-destructuring-destructure_slice--arraysslices"></a>

#### arrays/slices

Like tuples, arrays and slices can be destructured this way:

```rust
fn main() {
    // Try changing the values in the array, or make it a slice!
    let array = [1, -2, 6];

    match array {
        // Binds the second and the third elements to the respective variables
        [0, second, third] =>
            println!("array[0] = 0, array[1] = {}, array[2] = {}", second, third),

        // Single values can be ignored with _
        [1, _, third] => println!(
            "array[0] = 1, array[2] = {} and array[1] was ignored",
            third
        ),

        // You can also bind some and ignore the rest
        [-1, second, ..] => println!(
            "array[0] = -1, array[1] = {} and all the other ones were ignored",
            second
        ),
        // The code below would not compile
        // [-1, second] => ...

        // Or store them in another array/slice (the type depends on
        // that of the value that is being matched against)
        [3, second, tail @ ..] => println!(
            "array[0] = 3, array[1] = {} and the other elements were {:?}",
            second, tail
        ),

        // Combining these patterns, we can, for example, bind the first and
        // last values, and store the rest of them in a single array
        [first, middle @ .., last] => println!(
            "array[0] = {}, middle = {:?}, array[2] = {}",
            first, middle, last
        ),
    }
}
```

<a id="section-flow_control-match-destructuring-destructure_slice--see-also"></a>

###### See also:

[Arrays and Slices](02-primitives.md#section-primitives-array) and [Binding](#section-flow_control-match-binding) for `@` sigil

<a id="section-flow_control-match-destructuring-destructure_enum"></a>

<a id="section-flow_control-match-destructuring-destructure_enum--enums"></a>

#### enums

An `enum` is destructured similarly:

```rust
// `allow` required to silence warnings because only
// one variant is used.
#[allow(dead_code)]
enum Color {
    // These 3 are specified solely by their name.
    Red,
    Blue,
    Green,
    // These likewise tie `u32` tuples to different names: color models.
    RGB(u32, u32, u32),
    HSV(u32, u32, u32),
    HSL(u32, u32, u32),
    CMY(u32, u32, u32),
    CMYK(u32, u32, u32, u32),
}

fn main() {
    let color = Color::RGB(122, 17, 40);
    // TODO ^ Try different variants for `color`

    println!("What color is it?");
    // An `enum` can be destructured using a `match`.
    match color {
        Color::Red   => println!("The color is Red!"),
        Color::Blue  => println!("The color is Blue!"),
        Color::Green => println!("The color is Green!"),
        Color::RGB(r, g, b) =>
            println!("Red: {}, green: {}, and blue: {}!", r, g, b),
        Color::HSV(h, s, v) =>
            println!("Hue: {}, saturation: {}, value: {}!", h, s, v),
        Color::HSL(h, s, l) =>
            println!("Hue: {}, saturation: {}, lightness: {}!", h, s, l),
        Color::CMY(c, m, y) =>
            println!("Cyan: {}, magenta: {}, yellow: {}!", c, m, y),
        Color::CMYK(c, m, y, k) =>
            println!("Cyan: {}, magenta: {}, yellow: {}, key (black): {}!",
                c, m, y, k),
        // Don't need another arm because all variants have been examined
    }
}
```

<a id="section-flow_control-match-destructuring-destructure_enum--see-also"></a>

###### See also:

[`#[allow(...)]`][section-flow_control-match-destructuring-destructure_enum-ref-1], [color models][section-flow_control-match-destructuring-destructure_enum-ref-2] and [`enum`][section-flow_control-match-destructuring-destructure_enum-ref-3]

[section-flow_control-match-destructuring-destructure_enum-ref-1]: 13-attributes.md#section-attribute-unused
[section-flow_control-match-destructuring-destructure_enum-ref-2]: https://en.wikipedia.org/wiki/Color_model
[section-flow_control-match-destructuring-destructure_enum-ref-3]: 03-custom-types.md#section-custom_types-enum

<a id="section-flow_control-match-destructuring-destructure_pointers"></a>

<a id="section-flow_control-match-destructuring-destructure_pointers--pointersref"></a>

#### pointers/ref

For pointers, a distinction needs to be made between destructuring
and dereferencing as they are different concepts which are used
differently from languages like C/C++.

* Dereferencing uses `*`
* Destructuring uses `&`, `ref`, and `ref mut`

```rust
fn main() {
    // Assign a reference of type `i32`. The `&` signifies there
    // is a reference being assigned.
    let reference = &4;

    match reference {
        // If `reference` is pattern matched against `&val`, it results
        // in a comparison like:
        // `&i32`
        // `&val`
        // ^ We see that if the matching `&`s are dropped, then the `i32`
        // should be assigned to `val`.
        &val => println!("Got a value via destructuring: {:?}", val),
    }

    // To avoid the `&`, you dereference before matching.
    match *reference {
        val => println!("Got a value via dereferencing: {:?}", val),
    }

    // What if you don't start with a reference? `reference` was a `&`
    // because the right side was already a reference. This is not
    // a reference because the right side is not one.
    let _not_a_reference = 3;

    // Rust provides `ref` for exactly this purpose. It modifies the
    // assignment so that a reference is created for the element; this
    // reference is assigned.
    let ref _is_a_reference = 3;

    // Accordingly, by defining 2 values without references, references
    // can be retrieved via `ref` and `ref mut`.
    let value = 5;
    let mut mut_value = 6;

    // Use `ref` keyword to create a reference.
    match value {
        ref r => println!("Got a reference to a value: {:?}", r),
    }

    // Use `ref mut` similarly.
    match mut_value {
        ref mut m => {
            // Got a reference. Gotta dereference it before we can
            // add anything to it.
            *m += 10;
            println!("We added 10. `mut_value`: {:?}", m);
        },
    }
}
```

<a id="section-flow_control-match-destructuring-destructure_pointers--see-also"></a>

###### See also:

[The ref pattern](15-scoping-rules.md#section-scope-borrow-ref)

<a id="section-flow_control-match-destructuring-destructure_structures"></a>

<a id="section-flow_control-match-destructuring-destructure_structures--structs"></a>

#### structs

Similarly, a `struct` can be destructured as shown:

```rust
fn main() {
    struct Foo {
        x: (u32, u32),
        y: u32,
    }

    // Try changing the values in the struct to see what happens
    let foo = Foo { x: (1, 2), y: 3 };

    match foo {
        Foo { x: (1, b), y } => println!("First of x is 1, b = {},  y = {} ", b, y),

        // you can destructure structs and rename the variables,
        // the order is not important
        Foo { y: 2, x: i } => println!("y is 2, i = {:?}", i),

        // and you can also ignore some variables:
        Foo { y, .. } => println!("y = {}, we don't care about x", y),
        // this will give an error: pattern does not mention field `x`
        //Foo { y } => println!("y = {}", y),
    }

    let faa = Foo { x: (1, 2), y: 3 };

    // You do not need a match block to destructure structs:
    let Foo { x : x0, y: y0 } = faa;
    println!("Outside: x0 = {x0:?}, y0 = {y0}");

    // Destructuring works with nested structs as well:
    struct Bar {
        foo: Foo,
    }

    let bar = Bar { foo: faa };
    let Bar { foo: Foo { x: nested_x, y: nested_y } } = bar;
    println!("Nested: nested_x = {nested_x:?}, nested_y = {nested_y:?}");
}
```

<a id="section-flow_control-match-destructuring-destructure_structures--see-also"></a>

###### See also:

[Structs](03-custom-types.md#section-custom_types-structs)

<a id="section-flow_control-match-guard"></a>

<a id="section-flow_control-match-guard--guards"></a>

### Guards

A `match` *guard* can be added to filter the arm.

```rust
#[allow(dead_code)]
enum Temperature {
    Celsius(i32),
    Fahrenheit(i32),
}

fn main() {
    let temperature = Temperature::Celsius(35);
    // ^ TODO try different values for `temperature`

    match temperature {
        Temperature::Celsius(t) if t > 30 => println!("{}C is above 30 Celsius", t),
        // The `if condition` part ^ is a guard
        Temperature::Celsius(t) => println!("{}C is equal to or below 30 Celsius", t),

        Temperature::Fahrenheit(t) if t > 86 => println!("{}F is above 86 Fahrenheit", t),
        Temperature::Fahrenheit(t) => println!("{}F is equal to or below 86 Fahrenheit", t),
    }
}
```

Note that the compiler won't take guard conditions into account when checking
if all patterns are covered by the match expression.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    let number: u8 = 4;

    match number {
        i if i == 0 => println!("Zero"),
        i if i > 0 => println!("Greater than zero"),
        // _ => unreachable!("Should never happen."),
        // TODO ^ uncomment to fix compilation
    }
}
```

<a id="section-flow_control-match-guard--see-also"></a>

##### See also:

[Tuples](02-primitives.md#section-primitives-tuples)
[Enums](03-custom-types.md#section-custom_types-enum)

<a id="section-flow_control-match-binding"></a>

<a id="section-flow_control-match-binding--binding"></a>

### Binding

Indirectly accessing a variable makes it impossible to branch and use that
variable without re-binding. `match` provides the `@` sigil for binding values to
names:

```rust
// A function `age` which returns a `u32`.
fn age() -> u32 {
    15
}

fn main() {
    println!("Tell me what type of person you are");

    match age() {
        0             => println!("I haven't celebrated my first birthday yet"),
        // Could `match` 1 ..= 12 directly but then what age
        // would the child be?
        // Could `match` n and use an `if` guard, but would
        // not contribute to exhaustiveness checks.
        // (Although in this case that would not matter since
        // a "catch-all" pattern is present at the bottom)
        // Instead, bind to `n` for the sequence of 1 ..= 12.
        // Now the age can be reported.
        n @ 1  ..= 12 => println!("I'm a child of age {:?}", n),
        n @ 13 ..= 19 => println!("I'm a teen of age {:?}", n),
        // A similar binding can be done when matching several values.
        n @ (1 | 7 | 15 | 13) => println!("I'm a teen of age {:?}", n),
        // Nothing bound. Return the result.
        n             => println!("I'm an old person of age {:?}", n),
    }
}
```

You can also use binding to "destructure" `enum` variants, such as `Option`:

```rust
fn some_number() -> Option<u32> {
    Some(42)
}

fn main() {
    match some_number() {
        // Got `Some` variant, match if its value, bound to `n`,
        // is equal to 42.
        // Could also use `Some(42)` and print `"The Answer: 42!"`
        // but that would require changing `42` in 2 spots should
        // you ever wish to change it.
        // Could also use `Some(n) if n == 42` and print `"The Answer: {n}!"`
        // but that would not contribute to exhaustiveness checks.
        // (Although in this case that would not matter since
        // the next arm is a "catch-all" pattern)
        Some(n @ 42) => println!("The Answer: {}!", n),
        // Match any other number.
        Some(n)      => println!("Not interesting... {}", n),
        // Match anything else (`None` variant).
        _            => (),
    }
}
```

<a id="section-flow_control-match-binding--see-also"></a>

##### See also:

[`functions`][section-flow_control-match-binding-ref-1], [`enums`][section-flow_control-match-binding-ref-2] and [`Option`][section-flow_control-match-binding-ref-3]

[section-flow_control-match-binding-ref-1]: 09-functions.md
[section-flow_control-match-binding-ref-2]: 03-custom-types.md#section-custom_types-enum
[section-flow_control-match-binding-ref-3]: 19-std-library-types.md#section-std-option

<a id="section-flow_control-if_let"></a>

<a id="section-flow_control-if_let--if-let"></a>

## if let

For some use cases, when matching enums, `match` is awkward. For example:

```rust
// Make `optional` of type `Option<i32>`
let optional = Some(7);

match optional {
    Some(i) => println!("This is a really long string and `{:?}`", i),
    _ => {},
    // ^ Required because `match` is exhaustive. Doesn't it seem
    // like wasted space?
};

```

`if let` is cleaner for this use case and in addition allows various
failure options to be specified:

```rust
fn main() {
    // All have type `Option<i32>`
    let number = Some(7);
    let letter: Option<i32> = None;
    let emoticon: Option<i32> = None;

    // The `if let` construct reads: "if `let` destructures `number` into
    // `Some(i)`, evaluate the block (`{}`).
    if let Some(i) = number {
        println!("Matched {:?}!", i);
    }

    // If you need to specify a failure, use an else:
    if let Some(i) = letter {
        println!("Matched {:?}!", i);
    } else {
        // Destructure failed. Change to the failure case.
        println!("Didn't match a number. Let's go with a letter!");
    }

    // Provide an altered failing condition.
    let i_like_letters = false;

    if let Some(i) = emoticon {
        println!("Matched {:?}!", i);
    // Destructure failed. Evaluate an `else if` condition to see if the
    // alternate failure branch should be taken:
    } else if i_like_letters {
        println!("Didn't match a number. Let's go with a letter!");
    } else {
        // The condition evaluated false. This branch is the default:
        println!("I don't like letters. Let's go with an emoticon :)!");
    }
}
```

In the same way, `if let` can be used to match any enum value:

```rust
// Our example enum
enum Foo {
    Bar,
    Baz,
    Qux(u32)
}

fn main() {
    // Create example variables
    let a = Foo::Bar;
    let b = Foo::Baz;
    let c = Foo::Qux(100);

    // Variable a matches Foo::Bar
    if let Foo::Bar = a {
        println!("a is foobar");
    }

    // Variable b does not match Foo::Bar
    // So this will print nothing
    if let Foo::Bar = b {
        println!("b is foobar");
    }

    // Variable c matches Foo::Qux which has a value
    // Similar to Some() in the previous example
    if let Foo::Qux(value) = c {
        println!("c is {}", value);
    }

    // Binding also works with `if let`
    if let Foo::Qux(value @ 100) = c {
        println!("c is one hundred");
    }
}
```

Another benefit is that `if let` allows us to match non-parameterized enum variants. This is true even in cases where the enum doesn't implement or derive `PartialEq`. In such cases `if Foo::Bar == a` would fail to compile, because instances of the enum cannot be equated, however `if let` will continue to work.

Would you like a challenge? Fix the following example to use `if let`:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// This enum purposely neither implements nor derives PartialEq.
// That is why comparing Foo::Bar == a fails below.
enum Foo {Bar}

fn main() {
    let a = Foo::Bar;

    // Variable a matches Foo::Bar
    if Foo::Bar == a {
    // ^-- this causes a compile-time error. Use `if let` instead.
        println!("a is foobar");
    }
}
```

<a id="section-flow_control-if_let--see-also"></a>

#### See also:

[`enum`][section-flow_control-if_let-ref-1], [`Option`][section-flow_control-if_let-ref-3], and the [RFC][section-flow_control-if_let-ref-2]

[section-flow_control-if_let-ref-1]: 03-custom-types.md#section-custom_types-enum
[section-flow_control-if_let-ref-2]: https://github.com/rust-lang/rfcs/pull/160
[section-flow_control-if_let-ref-3]: 19-std-library-types.md#section-std-option

<a id="section-flow_control-let_else"></a>

<a id="section-flow_control-let_else--let-else"></a>

## let-else

> 🛈 stable since: rust 1.65
>
> 🛈 you can target specific edition by compiling like this
> `rustc --edition=2021 main.rs`

With `let`-`else`, a refutable pattern can match and bind variables
in the surrounding scope like a normal `let`, or else diverge (e.g. `break`,
`return`, `panic!`) when the pattern doesn't match.

```rust
use std::str::FromStr;

fn get_count_item(s: &str) -> (u64, &str) {
    let mut it = s.split(' ');
    let (Some(count_str), Some(item)) = (it.next(), it.next()) else {
        panic!("Can't segment count item pair: '{s}'");
    };
    let Ok(count) = u64::from_str(count_str) else {
        panic!("Can't parse integer: '{count_str}'");
    };
    (count, item)
}

fn main() {
    assert_eq!(get_count_item("3 chairs"), (3, "chairs"));
}
```

The scope of name bindings is the main thing that makes this different from
`match` or `if let`-`else` expressions. You could previously approximate these
patterns with an unfortunate bit of repetition and an outer `let`:

```rust
use std::str::FromStr;

fn get_count_item(s: &str) -> (u64, &str) {
    let mut it = s.split(' ');
    let (count_str, item) = match (it.next(), it.next()) {
        (Some(count_str), Some(item)) => (count_str, item),
        _ => panic!("Can't segment count item pair: '{s}'"),
    };
    let count = if let Ok(count) = u64::from_str(count_str) {
        count
    } else {
        panic!("Can't parse integer: '{count_str}'");
    };
    (count, item)
}

assert_eq!(get_count_item("3 chairs"), (3, "chairs"));
```

<a id="section-flow_control-let_else--see-also"></a>

#### See also:

[option][section-flow_control-let_else-ref-4], [match][section-flow_control-let_else-ref-1], [if let][section-flow_control-let_else-ref-2] and the [let-else RFC][section-flow_control-let_else-ref-3].

[section-flow_control-let_else-ref-1]: #section-flow_control-match
[section-flow_control-let_else-ref-2]: #section-flow_control-if_let
[section-flow_control-let_else-ref-3]: https://rust-lang.github.io/rfcs/3137-let-else.html
[section-flow_control-let_else-ref-4]: 19-std-library-types.md#section-std-option

<a id="section-flow_control-while_let"></a>

<a id="section-flow_control-while_let--while-let"></a>

## while let

Similar to `if let`, `while let` can make awkward `match` sequences
more tolerable. Consider the following sequence that increments `i`:

```rust
// Make `optional` of type `Option<i32>`
let mut optional = Some(0);

// Repeatedly try this test.
loop {
    match optional {
        // If `optional` destructures, evaluate the block.
        Some(i) => {
            if i > 9 {
                println!("Greater than 9, quit!");
                optional = None;
            } else {
                println!("`i` is `{:?}`. Try again.", i);
                optional = Some(i + 1);
            }
            // ^ Requires 3 indentations!
        },
        // Quit the loop when the destructure fails:
        _ => { break; }
        // ^ Why should this be required? There must be a better way!
    }
}
```

Using `while let` makes this sequence much nicer:

```rust
fn main() {
    // Make `optional` of type `Option<i32>`
    let mut optional = Some(0);

    // This reads: "while `let` destructures `optional` into
    // `Some(i)`, evaluate the block (`{}`). Else `break`.
    while let Some(i) = optional {
        if i > 9 {
            println!("Greater than 9, quit!");
            optional = None;
        } else {
            println!("`i` is `{:?}`. Try again.", i);
            optional = Some(i + 1);
        }
        // ^ Less rightward drift and doesn't require
        // explicitly handling the failing case.
    }
    // ^ `if let` had additional optional `else`/`else if`
    // clauses. `while let` does not have these.
}
```

<a id="section-flow_control-while_let--see-also"></a>

#### See also:

[`enum`][section-flow_control-while_let-ref-1], [`Option`][section-flow_control-while_let-ref-2], and the [RFC][section-flow_control-while_let-ref-3]

[section-flow_control-while_let-ref-1]: 03-custom-types.md#section-custom_types-enum
[section-flow_control-while_let-ref-2]: 19-std-library-types.md#section-std-option
[section-flow_control-while_let-ref-3]: https://github.com/rust-lang/rfcs/pull/214
