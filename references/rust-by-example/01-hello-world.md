<a id="section-hello"></a>

<a id="section-hello--hello-world"></a>

# Hello World

[Chapter index](SUMMARY.md)

**In this chapter**

- [Comments](#section-hello-comment)
- [Formatted print](#section-hello-print)
  - [Debug](#section-hello-print-print_debug)
  - [Display](#section-hello-print-print_display)
    - [Testcase: List](#section-hello-print-print_display-testcase_list)
  - [Formatting](#section-hello-print-fmt)


This is the source code of the traditional Hello World program.

```rust
// This is a comment, and is ignored by the compiler.
// Save this code as hello.rs and run it with rustc, as shown below.

// This code is editable, feel free to hack it!
// Keep a copy of the original if you want to reset your experiment.

// This is the main function.
fn main() {
    // Statements here are executed when the compiled binary is called.

    // Print text to the console.
    println!("Hello World!");
}
```

`println!` is a [*macro*][section-hello-ref-1] that prints text to the
console.

A binary can be generated using the Rust compiler: `rustc`.

```bash
$ rustc hello.rs
```

`rustc` will produce a `hello` binary that can be executed.

```bash
$ ./hello
Hello World!
```

<a id="section-hello--activity"></a>

### Activity

Compile and run the program locally to see the expected output. Next, add a new
line with a second `println!` macro so that the output shows:

```text
Hello World!
I'm a Rustacean!
```

[section-hello-ref-1]: 17-macro_rules.md

<a id="section-hello-comment"></a>

<a id="section-hello-comment--comments"></a>

## Comments

Any program requires comments, and Rust supports
a few different varieties:

<a id="section-hello-comment--regular-comments"></a>

### Regular Comments

These are ignored by the compiler:

* **Line comments**: Start with `//` and continue to the end of the line
* **Block comments**: Enclosed in `/* ... */` and can span multiple lines

<a id="section-hello-comment--documentation-comments-doc-comments-which-are-parsed-into-html-library-documentationdocs"></a>

### Documentation Comments (Doc Comments) which are parsed into HTML library [documentation][section-hello-comment-ref-1]:

 - `///` - Generates docs for the item that follows it
- `//!` - Generates docs for the enclosing item (typically used at the top of a file or module)
```rust

fn main() {
    // Line comments start with two slashes.
    // Everything after the slashes is ignored by the compiler.

    // Example: This line won't execute
    // println!("Hello, world!");

    // Try removing the slashes above and running the code again.

    /*
      Block comments are useful for temporarily disabling code.
      They can also be nested: /* like this */ which makes it easy
      to comment out large sections quickly.
     */

    /*
     * Note: The asterisk column on the left is just for style - 
     * it's not required by the language.
     */

    // Block comments make it easy to toggle code on/off by adding
    // or removing just one slash:

    /* <- Add a '/' here to uncomment the entire block below

    println!("Now");
    println!("everything");
    println!("executes!");
    // Line comments inside remain unaffected

    // */

    // Block comments can also be used within expressions:
    let x = 5 + /* 90 + */ 5;
    println!("Is `x` 10 or 100? x = {}", x);
}
```

<a id="section-hello-comment--see-also"></a>

#### See also:

[Library documentation][section-hello-comment-ref-1]

[section-hello-comment-ref-1]: 24-meta.md#section-meta-doc

<a id="section-hello-print"></a>

<a id="section-hello-print--formatted-print"></a>

## Formatted print

Printing is handled by a series of [`macros`][section-hello-print-ref-2] defined in
[`std::fmt`][section-hello-print-ref-1] some of which are:

* `format!`: write formatted text to [`String`][section-hello-print-ref-3]
* `print!`: same as `format!` but the text is printed to the console
  (io::stdout).
* `println!`: same as `print!` but a newline is appended.
* `eprint!`: same as `print!` but the text is printed to the standard error
  (io::stderr).
* `eprintln!`: same as `eprint!` but a newline is appended.

All parse text in the same fashion. As a plus, Rust checks formatting
correctness at compile time.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    // In general, the `{}` will be automatically replaced with any
    // arguments. These will be stringified.
    println!("{} days", 31);

    // Positional arguments can be used. Specifying an integer inside `{}`
    // determines which additional argument will be replaced. Arguments start
    // at 0 immediately after the format string.
    println!("{0}, this is {1}. {1}, this is {0}", "Alice", "Bob");

    // As can named arguments.
    println!("{subject} {verb} {object}",
             object="the lazy dog",
             subject="the quick brown fox",
             verb="jumps over");

    // Different formatting can be invoked by specifying the format character
    // after a `:`.
    println!("Base 10:               {}",   69420); // 69420
    println!("Base 2 (binary):       {:b}", 69420); // 10000111100101100
    println!("Base 8 (octal):        {:o}", 69420); // 207454
    println!("Base 16 (hexadecimal): {:x}", 69420); // 10f2c

    // You can right-justify text with a specified width. This will
    // output "    1". (Four white spaces and a "1", for a total width of 5.)
    println!("{number:>5}", number=1);

    // You can pad numbers with extra zeroes,
    println!("{number:0>5}", number=1); // 00001
    // and left-adjust by flipping the sign. This will output "10000".
    println!("{number:0<5}", number=1); // 10000

    // You can use named arguments in the format specifier by appending a `$`.
    println!("{number:0>width$}", number=1, width=5);

    // Rust even checks to make sure the correct number of arguments are used.
    println!("My name is {0}, {1} {0}", "Bond");
    // FIXME ^ Add the missing argument: "James"

    // Only types that implement fmt::Display can be formatted with `{}`. User-
    // defined types do not implement fmt::Display by default.

    #[allow(dead_code)] // disable `dead_code` which warn against unused module
    struct Structure(i32);

    // This will not compile because `Structure` does not implement
    // fmt::Display.
    // println!("This struct `{}` won't print...", Structure(3));
    // TODO ^ Try uncommenting this line

    // For Rust 1.58 and above, you can directly capture the argument from a
    // surrounding variable. Just like the above, this will output
    // "    1", 4 white spaces and a "1".
    let number: f64 = 1.0;
    let width: usize = 5;
    println!("{number:>width$}");
}
```

[`std::fmt`][section-hello-print-ref-1] contains many [`traits`][section-hello-print-ref-5] which govern the display
of text. The base form of two important ones are listed below:

* `fmt::Debug`: Uses the `{:?}` marker. Format text for debugging purposes.
* `fmt::Display`: Uses the `{}` marker. Format text in a more elegant, user
  friendly fashion.

Here, we used `fmt::Display` because the std library provides implementations
for these types. To print text for custom types, more steps are required.

Implementing the `fmt::Display` trait automatically implements the
[`ToString`][section-hello-print-ref-6] trait which allows us to [convert][section-hello-print-ref-7] the type to [`String`][section-hello-print-ref-3].

In *line 43*, `#[allow(dead_code)]` is an [attribute][section-hello-print-ref-8] which only applies to the item after it.

<a id="section-hello-print--activities"></a>

#### Activities

* Fix the issue in the above code (see FIXME) so that it runs without
  error.
* Try uncommenting the line that attempts to format the `Structure` struct
  (see TODO)
* Add a `println!` macro call that prints: `Pi is roughly 3.142` by controlling
  the number of decimal places shown. For the purposes of this exercise, use
  `let pi = 3.141592` as an estimate for pi. (Hint: you may need to check the
  [`std::fmt`][section-hello-print-ref-1] documentation for setting the number of decimals to display)

<a id="section-hello-print--see-also"></a>

#### See also:

[`std::fmt`][section-hello-print-ref-1], [`macros`][section-hello-print-ref-2], [`struct`][section-hello-print-ref-4], [`traits`][section-hello-print-ref-5], and [`dead_code`][section-hello-print-ref-9]

[section-hello-print-ref-1]: https://doc.rust-lang.org/std/fmt/
[section-hello-print-ref-2]: 17-macro_rules.md
[section-hello-print-ref-3]: 19-std-library-types.md#section-std-str
[section-hello-print-ref-4]: 03-custom-types.md#section-custom_types-structs
[section-hello-print-ref-5]: https://doc.rust-lang.org/std/fmt/#formatting-traits
[section-hello-print-ref-6]: https://doc.rust-lang.org/std/string/trait.ToString.html
[section-hello-print-ref-7]: 06-conversion.md#section-conversion-string
[section-hello-print-ref-8]: 13-attributes.md
[section-hello-print-ref-9]: 13-attributes.md#section-attribute-unused

<a id="section-hello-print-print_debug"></a>

<a id="section-hello-print-print_debug--debug"></a>

### Debug

All types which want to use `std::fmt` formatting `traits` require an
implementation to be printable. Automatic implementations are only provided
for types such as in the `std` library. All others *must* be manually
implemented somehow.

The `fmt::Debug` `trait` makes this very straightforward. *All* types can
`derive` (automatically create) the `fmt::Debug` implementation. This is
not true for `fmt::Display` which must be manually implemented.

```rust
// This structure cannot be printed either with `fmt::Display` or
// with `fmt::Debug`.
struct UnPrintable(i32);

// The `derive` attribute automatically creates the implementation
// required to make this `struct` printable with `fmt::Debug`.
#[derive(Debug)]
struct DebugPrintable(i32);
```

All `std` library types are automatically printable with `{:?}` too:

```rust
// Derive the `fmt::Debug` implementation for `Structure`. `Structure`
// is a structure which contains a single `i32`.
#[derive(Debug)]
struct Structure(i32);

// Put a `Structure` inside of the structure `Deep`. Make it printable
// also.
#[derive(Debug)]
struct Deep(Structure);

fn main() {
    // Printing with `{:?}` is similar to with `{}`.
    println!("{:?} months in a year.", 12);
    println!("{1:?} {0:?} is the {actor:?} name.",
             "Slater",
             "Christian",
             actor="actor's");

    // `Structure` is printable!
    println!("Now {:?} will print!", Structure(3));

    // The problem with `derive` is there is no control over how
    // the results look. What if I want this to just show a `7`?
    println!("Now {:?} will print!", Deep(Structure(7)));
}
```

So `fmt::Debug` definitely makes this printable but sacrifices some elegance.
Rust also provides "pretty printing" with `{:#?}`.

```rust
#[derive(Debug)]
struct Person<'a> {
    name: &'a str,
    age: u8
}

fn main() {
    let name = "Peter";
    let age = 27;
    let peter = Person { name, age };

    // Pretty print
    println!("{:#?}", peter);
}
```

One can manually implement `fmt::Display` to control the display.

<a id="section-hello-print-print_debug--see-also"></a>

##### See also:

[`attributes`][section-hello-print-print_debug-ref-1], [`derive`][section-hello-print-print_debug-ref-2], [`std::fmt`][section-hello-print-print_debug-ref-3],
and [`struct`][section-hello-print-print_debug-ref-4]

[section-hello-print-print_debug-ref-1]: https://doc.rust-lang.org/reference/attributes.html
[section-hello-print-print_debug-ref-2]: 16-traits.md#section-trait-derive
[section-hello-print-print_debug-ref-3]: https://doc.rust-lang.org/std/fmt/
[section-hello-print-print_debug-ref-4]: 03-custom-types.md#section-custom_types-structs

<a id="section-hello-print-print_display"></a>

<a id="section-hello-print-print_display--display"></a>

### Display

`fmt::Debug` hardly looks compact and clean, so it is often advantageous to
customize the output appearance. This is done by manually implementing
[`fmt::Display`][section-hello-print-print_display-ref-3], which uses the `{}` print marker. Implementing it
looks like this:

```rust
// Import (via `use`) the `fmt` module to make it available.
use std::fmt;

// Define a structure for which `fmt::Display` will be implemented. This is
// a tuple struct named `Structure` that contains an `i32`.
struct Structure(i32);

// To use the `{}` marker, the trait `fmt::Display` must be implemented
// manually for the type.
impl fmt::Display for Structure {
    // This trait requires `fmt` with this exact signature.
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Write strictly the first element into the supplied output
        // stream: `f`. Returns `fmt::Result` which indicates whether the
        // operation succeeded or failed. Note that `write!` uses syntax which
        // is very similar to `println!`.
        write!(f, "{}", self.0)
    }
}
```

`fmt::Display` may be cleaner than `fmt::Debug` but this presents
a problem for the `std` library. How should ambiguous types be displayed?
For example, if the `std` library implemented a single style for all
`Vec<T>`, what style should it be? Would it be either of these two?

* `Vec<path>`: `/:/etc:/home/username:/bin` (split on `:`)
* `Vec<number>`: `1,2,3` (split on `,`)

No, because there is no ideal style for all types and the `std` library
doesn't presume to dictate one. `fmt::Display` is not implemented for `Vec<T>`
or for any other generic containers. `fmt::Debug` must then be used for these
generic cases.

This is not a problem though because for any new *container* type which is
*not* generic, `fmt::Display` can be implemented.

```rust
use std::fmt; // Import `fmt`

// A structure holding two numbers. `Debug` will be derived so the results can
// be contrasted with `Display`.
#[derive(Debug)]
struct MinMax(i64, i64);

// Implement `Display` for `MinMax`.
impl fmt::Display for MinMax {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Use `self.number` to refer to each positional data point.
        write!(f, "({}, {})", self.0, self.1)
    }
}

// Define a structure where the fields are nameable for comparison.
#[derive(Debug)]
struct Point2D {
    x: f64,
    y: f64,
}

// Similarly, implement `Display` for `Point2D`.
impl fmt::Display for Point2D {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Customize so only `x` and `y` are denoted.
        write!(f, "x: {}, y: {}", self.x, self.y)
    }
}

fn main() {
    let minmax = MinMax(0, 14);

    println!("Compare structures:");
    println!("Display: {}", minmax);
    println!("Debug: {:?}", minmax);

    let big_range =   MinMax(-300, 300);
    let small_range = MinMax(-3, 3);

    println!("The big range is {big} and the small is {small}",
             small = small_range,
             big = big_range);

    let point = Point2D { x: 3.3, y: 7.2 };

    println!("Compare points:");
    println!("Display: {}", point);
    println!("Debug: {:?}", point);

    // The following line would not compile: both `Debug` and `Display`
    // were implemented, but `{:b}` requires `fmt::Binary` to be
    // implemented, which it hasn't been for `Point2D`.
    // println!("What does Point2D look like in binary: {:b}?", point);
}
```

So, `fmt::Display` has been implemented but `fmt::Binary` has not, and therefore
cannot be used. `std::fmt` has many such [`traits`][section-hello-print-print_display-ref-8] and each requires
its own implementation. This is detailed further in [`std::fmt`][section-hello-print-print_display-ref-3].

<a id="section-hello-print-print_display--activity"></a>

##### Activity

After checking the output of the above example, use the `Point2D` struct as a
guide to add a `Complex` struct to the example. When printed in the same
way, the output should be:

```txt
Display: 3.3 +7.2i
Debug: Complex { real: 3.3, imag: 7.2 }

Display: 4.7 -2.3i
Debug: Complex { real: 4.7, imag: -2.3 }
```

Bonus: Add a space after the `+`/`-` signs.

Hints in case you get stuck:

- Check the documentation for [`Sign/#/0`][section-hello-print-print_display-ref-4] in `std::fmt`.
- Bonus: Check [`if`-`else`][section-hello-print-print_display-ref-5] branching and the [`abs`][section-hello-print-print_display-ref-2] function.

<a id="section-hello-print-print_display--see-also"></a>

##### See also:

[`derive`][section-hello-print-print_display-ref-1], [`std::fmt`][section-hello-print-print_display-ref-3], [`macros`][section-hello-print-print_display-ref-6], [`struct`][section-hello-print-print_display-ref-7],
[`trait`][section-hello-print-print_display-ref-8], and [`use`][section-hello-print-print_display-ref-9]

[section-hello-print-print_display-ref-1]: 16-traits.md#section-trait-derive
[section-hello-print-print_display-ref-2]: https://doc.rust-lang.org/std/primitive.f64.html#method.abs
[section-hello-print-print_display-ref-3]: https://doc.rust-lang.org/std/fmt/
[section-hello-print-print_display-ref-4]: https://doc.rust-lang.org/std/fmt/#sign0
[section-hello-print-print_display-ref-5]: 08-flow-of-control.md#section-flow_control-if_else
[section-hello-print-print_display-ref-6]: 17-macro_rules.md
[section-hello-print-print_display-ref-7]: 03-custom-types.md#section-custom_types-structs
[section-hello-print-print_display-ref-8]: https://doc.rust-lang.org/std/fmt/#formatting-traits
[section-hello-print-print_display-ref-9]: 10-modules.md#section-mod-use

<a id="section-hello-print-print_display-testcase_list"></a>

<a id="section-hello-print-print_display-testcase_list--testcase-list"></a>

#### Testcase: List

Implementing `fmt::Display` for a structure where the elements must each be
handled sequentially is tricky. The problem is that each `write!` generates a
`fmt::Result`. Proper handling of this requires dealing with *all* the
results. Rust provides the `?` operator for exactly this purpose.

Using `?` on `write!` looks like this:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Try `write!` to see if it errors. If it errors, return
// the error. Otherwise continue.
write!(f, "{}", value)?;
```

With `?` available, implementing `fmt::Display` for a `Vec` is
straightforward:

```rust
use std::fmt; // Import the `fmt` module.

// Define a structure named `List` containing a `Vec`.
struct List(Vec<i32>);

impl fmt::Display for List {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Create a reference to the Vec<i32> stored in the List struct.
        let vec = &self.0;

        write!(f, "[")?;

        // Iterate over `v` in `vec` while enumerating the iteration
        // index in `index`.
        for (index, v) in vec.iter().enumerate() {
            // For every element except the first, add a comma.
            // Use the ? operator to return on errors.
            if index != 0 { write!(f, ", ")?; }
            write!(f, "{}", v)?;
        }

        // Close the opened bracket and return a fmt::Result value.
        write!(f, "]")
    }
}

fn main() {
    let v = List(vec![1, 2, 3]);
    println!("{}", v);
}
```

<a id="section-hello-print-print_display-testcase_list--activity"></a>

###### Activity

Try changing the program so that the index of each element in the vector is also
printed. The new output should look like this:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
[0: 1, 1: 2, 2: 3]
```

<a id="section-hello-print-print_display-testcase_list--see-also"></a>

###### See also:

[`for`][section-hello-print-print_display-testcase_list-ref-1], [`ref`][section-hello-print-print_display-testcase_list-ref-3], [`Result`][section-hello-print-print_display-testcase_list-ref-2], [`struct`][section-hello-print-print_display-testcase_list-ref-4],
[`?`][section-hello-print-print_display-testcase_list-ref-5], and [`vec!`][section-hello-print-print_display-testcase_list-ref-6]

[section-hello-print-print_display-testcase_list-ref-1]: 08-flow-of-control.md#section-flow_control-for
[section-hello-print-print_display-testcase_list-ref-2]: 19-std-library-types.md#section-std-result
[section-hello-print-print_display-testcase_list-ref-3]: 15-scoping-rules.md#section-scope-borrow-ref
[section-hello-print-print_display-testcase_list-ref-4]: 03-custom-types.md#section-custom_types-structs
[section-hello-print-print_display-testcase_list-ref-5]: 19-std-library-types.md#section-std-result-question_mark
[section-hello-print-print_display-testcase_list-ref-6]: 19-std-library-types.md#section-std-vec

<a id="section-hello-print-fmt"></a>

<a id="section-hello-print-fmt--formatting"></a>

### Formatting

We've seen that formatting is specified via a *format string*:

* `format!("{}", foo)` -> `"3735928559"`
* `format!("0x{:X}", foo)` -> [`"0xDEADBEEF"`][section-hello-print-fmt-ref-3]
* `format!("0o{:o}", foo)` -> `"0o33653337357"`

The same variable (`foo`) can be formatted differently depending on which
*argument type* is used: `X` vs `o` vs *unspecified*.

This formatting functionality is implemented via traits, and there is one trait
for each argument type. The most common formatting trait is `Display`, which
handles cases where the argument type is left unspecified: `{}` for instance.

```rust
use std::fmt::{self, Formatter, Display};

struct City {
    name: &'static str,
    // Latitude
    lat: f32,
    // Longitude
    lon: f32,
}

impl Display for City {
    // `f` is a buffer, and this method must write the formatted string into it.
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        let lat_c = if self.lat >= 0.0 { 'N' } else { 'S' };
        let lon_c = if self.lon >= 0.0 { 'E' } else { 'W' };

        // `write!` is like `format!`, but it will write the formatted string
        // into a buffer (the first argument).
        write!(f, "{}: {:.3}°{} {:.3}°{}",
               self.name, self.lat.abs(), lat_c, self.lon.abs(), lon_c)
    }
}

#[derive(Debug)]
struct Color {
    red: u8,
    green: u8,
    blue: u8,
}

fn main() {
    for city in [
        City { name: "Dublin", lat: 53.347778, lon: -6.259722 },
        City { name: "Oslo", lat: 59.95, lon: 10.75 },
        City { name: "Vancouver", lat: 49.25, lon: -123.1 },
    ] {
        println!("{}", city);
    }
    for color in [
        Color { red: 128, green: 255, blue: 90 },
        Color { red: 0, green: 3, blue: 254 },
        Color { red: 0, green: 0, blue: 0 },
    ] {
        // Switch this to use {} once you've added an implementation
        // for fmt::Display.
        println!("{:?}", color);
    }
}
```

You can view a [full list of formatting traits][section-hello-print-fmt-ref-5] and their argument
types in the [`std::fmt`][section-hello-print-fmt-ref-4] documentation.

<a id="section-hello-print-fmt--activity"></a>

##### Activity

Add an implementation of the `fmt::Display` trait for the `Color` struct above
so that the output displays as:

```text
RGB (128, 255, 90) 0x80FF5A
RGB (0, 3, 254) 0x0003FE
RGB (0, 0, 0) 0x000000
```

Two hints if you get stuck:

* You [may need to list each color more than once][section-hello-print-fmt-ref-2].
* You can [pad with zeros to a width of 2][section-hello-print-fmt-ref-6] with `:0>2`.
For hexadecimals, you can use `:02X`.

Bonus:

* If you would like to experiment with [type casting][section-hello-print-fmt-ref-7] in advance,
the formula for [calculating a color in the RGB color space][section-hello-print-fmt-ref-1] is
`RGB = (R * 65_536) + (G * 256) + B`, where `R is RED, G is GREEN, and B is BLUE`.
An unsigned 8-bit integer (`u8`) can only hold numbers up to 255. To cast `u8` to `u32`, you can write `variable_name as u32`.

<a id="section-hello-print-fmt--see-also"></a>

##### See also:

[`std::fmt`][section-hello-print-fmt-ref-4]

[section-hello-print-fmt-ref-1]: https://www.rapidtables.com/web/color/RGB_Color.html#rgb-format
[section-hello-print-fmt-ref-2]: https://doc.rust-lang.org/std/fmt/#named-parameters
[section-hello-print-fmt-ref-3]: https://en.wikipedia.org/wiki/Deadbeef#Magic_debug_values
[section-hello-print-fmt-ref-4]: https://doc.rust-lang.org/std/fmt/
[section-hello-print-fmt-ref-5]: https://doc.rust-lang.org/std/fmt/#formatting-traits
[section-hello-print-fmt-ref-6]: https://doc.rust-lang.org/std/fmt/#width
[section-hello-print-fmt-ref-7]: 05-types.md#section-types-cast
