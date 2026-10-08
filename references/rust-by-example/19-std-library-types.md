<a id="section-std"></a>

<a id="section-std--std-library-types"></a>

# Std library types

[Chapter index](SUMMARY.md)

**In this chapter**

- [Box, stack and heap](#section-std-box)
- [Vectors](#section-std-vec)
- [Strings](#section-std-str)
- [`Option`](#section-std-option)
- [`Result`](#section-std-result)
  - [`?`](#section-std-result-question_mark)
- [`panic!`](#section-std-panic)
- [HashMap](#section-std-hash)
  - [Alternate/custom key types](#section-std-hash-alt_key_types)
  - [HashSet](#section-std-hash-hashset)
- [`Rc`](#section-std-rc)
- [`Arc`](#section-std-arc)


The `std` library provides many custom types which expands drastically on
the `primitives`. Some of these include:

* growable `String`s like: `"hello world"`
* growable vectors: `[1, 2, 3]`
* optional types: `Option<i32>`
* error handling types: `Result<i32, i32>`
* heap allocated pointers: `Box<i32>`

<a id="section-std--see-also"></a>

### See also:

[primitives][section-std-ref-1] and [the std library][section-std-ref-2]

[section-std-ref-1]: 02-primitives.md
[section-std-ref-2]: https://doc.rust-lang.org/std/

<a id="section-std-box"></a>

<a id="section-std-box--box-stack-and-heap"></a>

## Box, stack and heap

All values in Rust are stack allocated by default. Values can be *boxed*
(allocated on the heap) by creating a `Box<T>`. A box is a smart pointer to a
heap allocated value of type `T`. When a box goes out of scope, its destructor
is called, the inner object is destroyed, and the memory on the heap is freed.

Boxed values can be dereferenced using the `*` operator; this removes one layer
of indirection.

```rust
use std::mem;

#[allow(dead_code)]
#[derive(Debug, Clone, Copy)]
struct Point {
    x: f64,
    y: f64,
}

// A Rectangle can be specified by where its top left and bottom right
// corners are in space
#[allow(dead_code)]
struct Rectangle {
    top_left: Point,
    bottom_right: Point,
}

fn origin() -> Point {
    Point { x: 0.0, y: 0.0 }
}

fn boxed_origin() -> Box<Point> {
    // Allocate this point on the heap, and return a pointer to it
    Box::new(Point { x: 0.0, y: 0.0 })
}

fn main() {
    // (all the type annotations are superfluous)
    // Stack allocated variables
    let point: Point = origin();
    let rectangle: Rectangle = Rectangle {
        top_left: origin(),
        bottom_right: Point { x: 3.0, y: -4.0 }
    };

    // Heap allocated rectangle
    let boxed_rectangle: Box<Rectangle> = Box::new(Rectangle {
        top_left: origin(),
        bottom_right: Point { x: 3.0, y: -4.0 },
    });

    // The output of functions can be boxed
    let boxed_point: Box<Point> = Box::new(origin());

    // Double indirection
    let box_in_a_box: Box<Box<Point>> = Box::new(boxed_origin());

    println!("Point occupies {} bytes on the stack",
             mem::size_of_val(&point));
    println!("Rectangle occupies {} bytes on the stack",
             mem::size_of_val(&rectangle));

    // box size == pointer size
    println!("Boxed point occupies {} bytes on the stack",
             mem::size_of_val(&boxed_point));
    println!("Boxed rectangle occupies {} bytes on the stack",
             mem::size_of_val(&boxed_rectangle));
    println!("Boxed box occupies {} bytes on the stack",
             mem::size_of_val(&box_in_a_box));

    // Copy the data contained in `boxed_point` into `unboxed_point`
    let unboxed_point: Point = *boxed_point;
    println!("Unboxed point occupies {} bytes on the stack",
             mem::size_of_val(&unboxed_point));
}
```

<a id="section-std-vec"></a>

<a id="section-std-vec--vectors"></a>

## Vectors

Vectors are re-sizable arrays. Like slices, their size is not known at compile
time, but they can grow or shrink at any time. A vector is represented using
3 parameters:

- pointer to the data
- length
- capacity

The capacity indicates how much memory is reserved for the vector. The vector
can grow as long as the length is smaller than the capacity. When this threshold
needs to be surpassed, the vector is reallocated with a larger capacity.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    // Iterators can be collected into vectors
    let collected_iterator: Vec<i32> = (0..10).collect();
    println!("Collected (0..10) into: {:?}", collected_iterator);

    // The `vec!` macro can be used to initialize a vector
    let mut xs = vec![1i32, 2, 3];
    println!("Initial vector: {:?}", xs);

    // Insert new element at the end of the vector
    println!("Push 4 into the vector");
    xs.push(4);
    println!("Vector: {:?}", xs);

    // Error! Immutable vectors can't grow
    collected_iterator.push(0);
    // FIXME ^ Comment out this line

    // The `len` method yields the number of elements currently stored in a vector
    println!("Vector length: {}", xs.len());

    // Indexing is done using the square brackets (indexing starts at 0)
    println!("Second element: {}", xs[1]);

    // `pop` removes the last element from the vector and returns it
    println!("Pop last element: {:?}", xs.pop());

    // Out of bounds indexing yields a panic
    println!("Fourth element: {}", xs[3]);
    // FIXME ^ Comment out this line

    // `Vector`s can be easily iterated over
    println!("Contents of xs:");
    for x in xs.iter() {
        println!("> {}", x);
    }

    // A `Vector` can also be iterated over while the iteration
    // count is enumerated in a separate variable (`i`)
    for (i, x) in xs.iter().enumerate() {
        println!("In position {} we have value {}", i, x);
    }

    // Thanks to `iter_mut`, mutable `Vector`s can also be iterated
    // over in a way that allows modifying each value
    for x in xs.iter_mut() {
        *x *= 3;
    }
    println!("Updated vector: {:?}", xs);
}
```

More `Vec` methods can be found under the
[std::vec][section-std-vec-ref-1] module

[section-std-vec-ref-1]: https://doc.rust-lang.org/std/vec/

<a id="section-std-str"></a>

<a id="section-std-str--strings"></a>

## Strings

The two most used string types in Rust are `String` and `&str`.

A `String` is stored as a vector of bytes (`Vec<u8>`), but guaranteed to
always be a valid UTF-8 sequence. `String` is heap allocated, growable and not
null terminated.

`&str` is a slice (`&[u8]`) that always points to a valid UTF-8 sequence, and
can be used to view into a `String`, just like `&[T]` is a view into `Vec<T>`.

```rust
fn main() {
    // (all the type annotations are superfluous)
    // A reference to a string allocated in read only memory
    let pangram: &'static str = "the quick brown fox jumps over the lazy dog";
    println!("Pangram: {}", pangram);

    // Iterate over words in reverse, no new string is allocated
    println!("Words in reverse");
    for word in pangram.split_whitespace().rev() {
        println!("> {}", word);
    }

    // Copy chars into a vector, sort and remove duplicates
    let mut chars: Vec<char> = pangram.chars().collect();
    chars.sort();
    chars.dedup();

    // Create an empty and growable `String`
    let mut string = String::new();
    for c in chars {
        // Insert a char at the end of string
        string.push(c);
        // Insert a string at the end of string
        string.push_str(", ");
    }

    // The trimmed string is a slice to the original string, hence no new
    // allocation is performed
    let chars_to_trim: &[char] = &[' ', ','];
    let trimmed_str: &str = string.trim_matches(chars_to_trim);
    println!("Used characters: {}", trimmed_str);

    // Heap allocate a string
    let alice = String::from("I like dogs");
    // Allocate new memory and store the modified string there
    let bob: String = alice.replace("dog", "cat");

    println!("Alice says: {}", alice);
    println!("Bob says: {}", bob);
}
```

More `str`/`String` methods can be found under the
[std::str][section-std-str-ref-1] and
[std::string][section-std-str-ref-2]
modules

<a id="section-std-str--literals-and-escapes"></a>

### Literals and escapes

There are multiple ways to write string literals with special characters in them.
All result in a similar `&str` so it's best to use the form that is the most
convenient to write. Similarly there are multiple ways to write byte string literals,
which all result in `&[u8; N]`.

Generally special characters are escaped with a backslash character: `\`.
This way you can add any character to your string, even unprintable ones
and ones that you don't know how to type. If you want a literal backslash,
escape it with another one: `\\`

String or character literal delimiters occurring within a literal must be escaped: `"\""`, `'\''`.

```rust
fn main() {
    // You can use escapes to write bytes by their hexadecimal values...
    let byte_escape = "I'm writing \x52\x75\x73\x74!";
    println!("What are you doing\x3F (\\x3F means ?) {}", byte_escape);

    // ...or Unicode code points.
    let unicode_codepoint = "\u{211D}";
    let character_name = "\"DOUBLE-STRUCK CAPITAL R\"";

    println!("Unicode character {} (U+211D) is called {}",
                unicode_codepoint, character_name );


    let long_string = "String literals
                        can span multiple lines.
                        The linebreak and indentation here ->\
                        <- can be escaped too!";
    println!("{}", long_string);
}
```

Sometimes there are just too many characters that need to be escaped or it's just
much more convenient to write a string out as-is. This is where raw string literals come into play.

```rust
fn main() {
    let raw_str = r"Escapes don't work here: \x3F \u{211D}";
    println!("{}", raw_str);

    // If you need quotes in a raw string, add a pair of #s
    let quotes = r#"And then I said: "There is no escape!""#;
    println!("{}", quotes);

    // If you need "# in your string, just use more #s in the delimiter.
    // You can use up to 255 #s.
    let longer_delimiter = r###"A string with "# in it. And even "##!"###;
    println!("{}", longer_delimiter);
}
```

Want a string that's not UTF-8? (Remember, `str` and `String` must be valid UTF-8).
Or maybe you want an array of bytes that's mostly text? Byte strings to the rescue!

```rust
use std::str;

fn main() {
    // Note that this is not actually a `&str`
    let bytestring: &[u8; 21] = b"this is a byte string";

    // Byte arrays don't have the `Display` trait, so printing them is a bit limited
    println!("A byte string: {:?}", bytestring);

    // Byte strings can have byte escapes...
    let escaped = b"\x52\x75\x73\x74 as bytes";
    // ...but no unicode escapes
    // let escaped = b"\u{211D} is not allowed";
    println!("Some escaped bytes: {:?}", escaped);


    // Raw byte strings work just like raw strings
    let raw_bytestring = br"\u{211D} is not escaped here";
    println!("{:?}", raw_bytestring);

    // Converting a byte array to `str` can fail
    if let Ok(my_str) = str::from_utf8(raw_bytestring) {
        println!("And the same as text: '{}'", my_str);
    }

    let _quotes = br#"You can also use "fancier" formatting, \
                    like with normal raw strings"#;

    // Byte strings don't have to be UTF-8
    let shift_jis = b"\x82\xe6\x82\xa8\x82\xb1\x82\xbb"; // "ようこそ" in SHIFT-JIS

    // But then they can't always be converted to `str`
    match str::from_utf8(shift_jis) {
        Ok(my_str) => println!("Conversion successful: '{}'", my_str),
        Err(e) => println!("Conversion failed: {:?}", e),
    };
}
```

For conversions between character encodings check out the [encoding][section-std-str-ref-4] crate.

A more detailed listing of the ways to write string literals and escape characters
is given in the ['Tokens' chapter][section-std-str-ref-3] of the Rust Reference.

[section-std-str-ref-1]: https://doc.rust-lang.org/std/str/
[section-std-str-ref-2]: https://doc.rust-lang.org/std/string/
[section-std-str-ref-3]: https://doc.rust-lang.org/reference/tokens.html
[section-std-str-ref-4]: https://crates.io/crates/encoding

<a id="section-std-option"></a>

<a id="section-std-option--option"></a>

## `Option`

Sometimes it's desirable to catch the failure of some parts of a program
instead of calling `panic!`; this can be accomplished using the `Option` enum.

The `Option<T>` enum has two variants:

* `None`, to indicate failure or lack of value, and
* `Some(value)`, a tuple struct that wraps a `value` with type `T`.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// An integer division that doesn't `panic!`
fn checked_division(dividend: i32, divisor: i32) -> Option<i32> {
    if divisor == 0 {
        // Failure is represented as the `None` variant
        None
    } else {
        // Result is wrapped in a `Some` variant
        Some(dividend / divisor)
    }
}

// This function handles a division that may not succeed
fn try_division(dividend: i32, divisor: i32) {
    // `Option` values can be pattern matched, just like other enums
    match checked_division(dividend, divisor) {
        None => println!("{} / {} failed!", dividend, divisor),
        Some(quotient) => {
            println!("{} / {} = {}", dividend, divisor, quotient)
        },
    }
}

fn main() {
    try_division(4, 2);
    try_division(1, 0);

    // Binding `None` to a variable needs to be type annotated
    let none: Option<i32> = None;
    let _equivalent_none = None::<i32>;

    let optional_float = Some(0f32);

    // Unwrapping a `Some` variant will extract the value wrapped.
    println!("{:?} unwraps to {:?}", optional_float, optional_float.unwrap());

    // Unwrapping a `None` variant will `panic!`
    println!("{:?} unwraps to {:?}", none, none.unwrap());
}
```

<a id="section-std-result"></a>

<a id="section-std-result--result"></a>

## `Result`

We've seen that the `Option` enum can be used as a return value from functions
that may fail, where `None` can be returned to indicate failure. However,
sometimes it is important to express *why* an operation failed. To do this we
have the `Result` enum.

The `Result<T, E>` enum has two variants:

* `Ok(value)` which indicates that the operation succeeded, and wraps the
  `value` returned by the operation. (`value` has type `T`)
* `Err(why)`, which indicates that the operation failed, and wraps `why`,
  which (hopefully) explains the cause of the failure. (`why` has type `E`)

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
mod checked {
    // Mathematical "errors" we want to catch
    #[derive(Debug)]
    pub enum MathError {
        DivisionByZero,
        NonPositiveLogarithm,
        NegativeSquareRoot,
    }

    pub type MathResult = Result<f64, MathError>;

    pub fn div(x: f64, y: f64) -> MathResult {
        if y == 0.0 {
            // This operation would `fail`, instead let's return the reason of
            // the failure wrapped in `Err`
            Err(MathError::DivisionByZero)
        } else {
            // This operation is valid, return the result wrapped in `Ok`
            Ok(x / y)
        }
    }

    pub fn sqrt(x: f64) -> MathResult {
        if x < 0.0 {
            Err(MathError::NegativeSquareRoot)
        } else {
            Ok(x.sqrt())
        }
    }

    pub fn ln(x: f64) -> MathResult {
        if x <= 0.0 {
            Err(MathError::NonPositiveLogarithm)
        } else {
            Ok(x.ln())
        }
    }
}

// `op(x, y)` === `sqrt(ln(x / y))`
fn op(x: f64, y: f64) -> f64 {
    // This is a three level match pyramid!
    match checked::div(x, y) {
        Err(why) => panic!("{:?}", why),
        Ok(ratio) => match checked::ln(ratio) {
            Err(why) => panic!("{:?}", why),
            Ok(ln) => match checked::sqrt(ln) {
                Err(why) => panic!("{:?}", why),
                Ok(sqrt) => sqrt,
            },
        },
    }
}

fn main() {
    // Will this fail?
    println!("{}", op(1.0, 10.0));
}
```

<a id="section-std-result-question_mark"></a>

<a id="section-std-result-question_mark--"></a>

### `?`

Chaining results using match can get pretty untidy; luckily, the `?` operator
can be used to make things pretty again. `?` is used at the end of an expression
returning a `Result`, and is equivalent to a match expression, where the
`Err(err)` branch expands to an early `return Err(From::from(err))`, and the `Ok(ok)`
branch expands to an `ok` expression.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
mod checked {
    #[derive(Debug)]
    enum MathError {
        DivisionByZero,
        NonPositiveLogarithm,
        NegativeSquareRoot,
    }

    type MathResult = Result<f64, MathError>;

    fn div(x: f64, y: f64) -> MathResult {
        if y == 0.0 {
            Err(MathError::DivisionByZero)
        } else {
            Ok(x / y)
        }
    }

    fn sqrt(x: f64) -> MathResult {
        if x < 0.0 {
            Err(MathError::NegativeSquareRoot)
        } else {
            Ok(x.sqrt())
        }
    }

    fn ln(x: f64) -> MathResult {
        if x <= 0.0 {
            Err(MathError::NonPositiveLogarithm)
        } else {
            Ok(x.ln())
        }
    }

    // Intermediate function
    fn op_(x: f64, y: f64) -> MathResult {
        // if `div` "fails", then `DivisionByZero` will be `return`ed
        let ratio = div(x, y)?;

        // if `ln` "fails", then `NonPositiveLogarithm` will be `return`ed
        let ln = ln(ratio)?;

        sqrt(ln)
    }

    pub fn op(x: f64, y: f64) {
        match op_(x, y) {
            Err(why) => panic!("{}", match why {
                MathError::NonPositiveLogarithm
                    => "logarithm of non-positive number",
                MathError::DivisionByZero
                    => "division by zero",
                MathError::NegativeSquareRoot
                    => "square root of negative number",
            }),
            Ok(value) => println!("{}", value),
        }
    }
}

fn main() {
    checked::op(1.0, 10.0);
}
```

Be sure to check the [documentation][section-std-result-question_mark-ref-1],
as there are many methods to map/compose `Result`.

[section-std-result-question_mark-ref-1]: https://doc.rust-lang.org/std/result/index.html

<a id="section-std-panic"></a>

<a id="section-std-panic--panic"></a>

## `panic!`

The `panic!` macro can be used to generate a panic and start unwinding
its stack. While unwinding, the runtime will take care of freeing all the
resources *owned* by the thread by calling the destructor of all its objects.

Since we are dealing with programs with only one thread, `panic!` will cause the
program to report the panic message and exit.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Re-implementation of integer division (/)
fn division(dividend: i32, divisor: i32) -> i32 {
    if divisor == 0 {
        // Division by zero triggers a panic
        panic!("division by zero");
    } else {
        dividend / divisor
    }
}

// The `main` task
fn main() {
    // Heap allocated integer
    let _x = Box::new(0i32);

    // This operation will trigger a task failure
    division(3, 0);

    println!("This point won't be reached!");

    // `_x` should get destroyed at this point
}
```

Let's check that `panic!` doesn't leak memory.

<!-- REUSE-IgnoreStart -->
<!-- Prevent REUSE from parsing the copyright statement in the sample code -->
```shell
$ rustc panic.rs && valgrind ./panic
==4401== Memcheck, a memory error detector
==4401== Copyright (C) 2002-2013, and GNU GPL'd, by Julian Seward et al.
==4401== Using Valgrind-3.10.0.SVN and LibVEX; rerun with -h for copyright info
==4401== Command: ./panic
==4401==
thread '<main>' panicked at 'division by zero', panic.rs:5
==4401==
==4401== HEAP SUMMARY:
==4401==     in use at exit: 0 bytes in 0 blocks
==4401==   total heap usage: 18 allocs, 18 frees, 1,648 bytes allocated
==4401==
==4401== All heap blocks were freed -- no leaks are possible
==4401==
==4401== For counts of detected and suppressed errors, rerun with: -v
==4401== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
<!-- REUSE-IgnoreEnd -->

<a id="section-std-hash"></a>

<a id="section-std-hash--hashmap"></a>

## HashMap

Where vectors store values by an integer index, `HashMap`s store values by key.
`HashMap` keys can be booleans, integers, strings,
or any other type that implements the `Eq` and `Hash` traits.
More on this in the next section.

Like vectors, `HashMap`s are growable, but HashMaps can also shrink themselves
when they have excess space.
You can create a HashMap with a certain starting capacity using
`HashMap::with_capacity(uint)`, or use `HashMap::new()` to get a HashMap
with a default initial capacity (recommended).

```rust
use std::collections::HashMap;

fn call(number: &str) -> &str {
    match number {
        "798-1364" => "We're sorry, the call cannot be completed as dialed.
            Please hang up and try again.",
        "645-7689" => "Hello, this is Mr. Awesome's Pizza. My name is Fred.
            What can I get for you today?",
        _ => "Hi! Who is this again?"
    }
}

fn main() {
    let mut contacts = HashMap::new();

    contacts.insert("Daniel", "798-1364");
    contacts.insert("Ashley", "645-7689");
    contacts.insert("Katie", "435-8291");
    contacts.insert("Robert", "956-1745");

    // Takes a reference and returns Option<&V>
    match contacts.get(&"Daniel") {
        Some(&number) => println!("Calling Daniel: {}", call(number)),
        _ => println!("Don't have Daniel's number."),
    }

    // `HashMap::insert()` returns `None`
    // if the inserted value is new, `Some(value)` otherwise
    contacts.insert("Daniel", "164-6743");

    match contacts.get(&"Ashley") {
        Some(&number) => println!("Calling Ashley: {}", call(number)),
        _ => println!("Don't have Ashley's number."),
    }

    contacts.remove(&"Ashley");

    // `HashMap::iter()` returns an iterator that yields
    // (&'a key, &'a value) pairs in arbitrary order.
    for (contact, &number) in contacts.iter() {
        println!("Calling {}: {}", contact, call(number));
    }
}
```

For more information on how hashing and hash maps
(sometimes called hash tables) work, have a look at
[Hash Table Wikipedia][section-std-hash-ref-1]

[section-std-hash-ref-1]: https://en.wikipedia.org/wiki/Hash_table

<a id="section-std-hash-alt_key_types"></a>

<a id="section-std-hash-alt_key_types--alternatecustom-key-types"></a>

### Alternate/custom key types

Any type that implements the `Eq` and `Hash` traits can be a key in `HashMap`.
This includes:

* `bool` (though not very useful since there are only two possible keys)
* `int`, `uint`, and all variations thereof
* `String` and `&str` (protip: you can have a `HashMap` keyed by `String`
and call `.get()` with an `&str`)

Note that `f32` and `f64` do *not* implement `Hash`,
likely because [floating-point precision errors][section-std-hash-alt_key_types-ref-2]
would make using them as hashmap keys horribly error-prone.

All collection classes implement `Eq` and `Hash`
if their contained type also respectively implements `Eq` and `Hash`.
For example, `Vec<T>` will implement `Hash` if `T` implements `Hash`.

You can easily implement `Eq` and `Hash` for a custom type with just one line:
`#[derive(PartialEq, Eq, Hash)]`

The compiler will do the rest. If you want more control over the details,
you can implement `Eq` and/or `Hash` yourself.
This guide will not cover the specifics of implementing `Hash`.

To play around with using a `struct` in `HashMap`,
let's try making a very simple user logon system:

```rust
use std::collections::HashMap;

// Eq requires that you derive PartialEq on the type.
#[derive(PartialEq, Eq, Hash)]
struct Account<'a>{
    username: &'a str,
    password: &'a str,
}

struct AccountInfo<'a>{
    name: &'a str,
    email: &'a str,
}

type Accounts<'a> = HashMap<Account<'a>, AccountInfo<'a>>;

fn try_logon<'a>(accounts: &Accounts<'a>,
        username: &'a str, password: &'a str){
    println!("Username: {}", username);
    println!("Password: {}", password);
    println!("Attempting logon...");

    let logon = Account {
        username,
        password,
    };

    match accounts.get(&logon) {
        Some(account_info) => {
            println!("Successful logon!");
            println!("Name: {}", account_info.name);
            println!("Email: {}", account_info.email);
        },
        _ => println!("Login failed!"),
    }
}

fn main(){
    let mut accounts: Accounts = HashMap::new();

    let account = Account {
        username: "j.everyman",
        password: "password123",
    };

    let account_info = AccountInfo {
        name: "John Everyman",
        email: "j.everyman@email.com",
    };

    accounts.insert(account, account_info);

    try_logon(&accounts, "j.everyman", "psasword123");

    try_logon(&accounts, "j.everyman", "password123");
}
```

[section-std-hash-alt_key_types-ref-1]: https://en.wikipedia.org/wiki/Hash_function
[section-std-hash-alt_key_types-ref-2]: https://en.wikipedia.org/wiki/Floating_point#Accuracy_problems

<a id="section-std-hash-hashset"></a>

<a id="section-std-hash-hashset--hashset"></a>

### HashSet

Consider a `HashSet` as a `HashMap` where we just care about the keys (
`HashSet<T>` is, in actuality, just a wrapper around `HashMap<T, ()>`).

"What's the point of that?" you ask. "I could just store the keys in a `Vec`."

A `HashSet`'s unique feature is that
it is guaranteed to not have duplicate elements.
That's the contract that any set collection fulfills.
`HashSet` is just one implementation. (see also: [`BTreeSet`][section-std-hash-hashset-ref-1])

If you insert a value that is already present in the `HashSet`,
(i.e. the new value is equal to the existing and they both have the same hash),
then the new value will replace the old.

This is great for when you never want more than one of something,
or when you want to know if you've already got something.

But sets can do more than that.

Sets have 4 primary operations (all of the following calls return an iterator):

* `union`: get all the unique elements in both sets.

* `difference`: get all the elements that are in the first set but not the second.

* `intersection`: get all the elements that are only in *both* sets.

* `symmetric_difference`:
get all the elements that are in one set or the other, but *not* both.

Try all of these in the following example:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
use std::collections::HashSet;

fn main() {
    let mut a: HashSet<i32> = vec![1i32, 2, 3].into_iter().collect();
    let mut b: HashSet<i32> = vec![2i32, 3, 4].into_iter().collect();

    assert!(a.insert(4));
    assert!(a.contains(&4));

    // `HashSet::insert()` returns false if
    // there was a value already present.
    assert!(b.insert(4), "Value 4 is already in set B!");
    // FIXME ^ Comment out this line

    b.insert(5);

    // If a collection's element type implements `Debug`,
    // then the collection implements `Debug`.
    // It usually prints its elements in the format `[elem1, elem2, ...]`
    println!("A: {:?}", a);
    println!("B: {:?}", b);

    // Print [1, 2, 3, 4, 5] in arbitrary order
    println!("Union: {:?}", a.union(&b).collect::<Vec<&i32>>());

    // This should print [1]
    println!("Difference: {:?}", a.difference(&b).collect::<Vec<&i32>>());

    // Print [2, 3, 4] in arbitrary order.
    println!("Intersection: {:?}", a.intersection(&b).collect::<Vec<&i32>>());

    // Print [1, 5]
    println!("Symmetric Difference: {:?}",
             a.symmetric_difference(&b).collect::<Vec<&i32>>());
}
```

(Examples are adapted from the [documentation.][section-std-hash-hashset-ref-2])

[section-std-hash-hashset-ref-1]: https://doc.rust-lang.org/std/collections/struct.BTreeSet.html
[section-std-hash-hashset-ref-2]: https://doc.rust-lang.org/std/collections/struct.HashSet.html#method.difference

<a id="section-std-rc"></a>

<a id="section-std-rc--rc"></a>

## `Rc`

When multiple ownership is needed, `Rc`(Reference Counting) can be used. `Rc`
keeps track of the number of the references which means the number of owners of
the value wrapped inside an `Rc`.

Reference count of an `Rc` increases by 1 whenever an `Rc` is cloned, and
decreases by 1 whenever one cloned `Rc` is dropped out of the scope. When an
`Rc`'s reference count becomes zero (which means there are no remaining owners),
both the `Rc` and the value are all dropped.

Cloning an `Rc` never performs a deep copy. Cloning creates just another pointer
to the wrapped value, and increments the count.

```rust
use std::rc::Rc;

fn main() {
    let rc_examples = "Rc examples".to_string();
    {
        println!("--- rc_a is created ---");

        let rc_a: Rc<String> = Rc::new(rc_examples);
        println!("Reference Count of rc_a: {}", Rc::strong_count(&rc_a));

        {
            println!("--- rc_a is cloned to rc_b ---");

            let rc_b: Rc<String> = Rc::clone(&rc_a);
            println!("Reference Count of rc_b: {}", Rc::strong_count(&rc_b));
            println!("Reference Count of rc_a: {}", Rc::strong_count(&rc_a));

            // Two `Rc`s are equal if their inner values are equal
            println!("rc_a and rc_b are equal: {}", rc_a.eq(&rc_b));

            // We can use methods of a value directly
            println!("Length of the value inside rc_a: {}", rc_a.len());
            println!("Value of rc_b: {}", rc_b);

            println!("--- rc_b is dropped out of scope ---");
        }

        println!("Reference Count of rc_a: {}", Rc::strong_count(&rc_a));

        println!("--- rc_a is dropped out of scope ---");
    }

    // Error! `rc_examples` already moved into `rc_a`
    // And when `rc_a` is dropped, `rc_examples` is dropped together
    // println!("rc_examples: {}", rc_examples);
    // TODO ^ Try uncommenting this line
}
```

<a id="section-std-rc--see-also"></a>

#### See also:

[std::rc][section-std-rc-ref-1] and [std::sync::arc][section-std-rc-ref-2].

[section-std-rc-ref-1]: https://doc.rust-lang.org/std/rc/index.html
[section-std-rc-ref-2]: https://doc.rust-lang.org/std/sync/struct.Arc.html

<a id="section-std-arc"></a>

<a id="section-std-arc--arc"></a>

## Arc

When shared ownership between threads is needed, `Arc`(Atomically Reference
Counted) can be used. This struct, via the `Clone` implementation can create
a reference pointer for the location of a value in the memory heap while
increasing the reference counter. As it shares ownership between threads, when
the last reference pointer to a value is out of scope, the variable is dropped.

```rust
use std::time::Duration;
use std::sync::Arc;
use std::thread;

fn main() {
    // This variable declaration is where its value is specified.
    let apple = Arc::new("the same apple");

    for _ in 0..10 {
        // Here there is no value specification as it is a pointer to a
        // reference in the memory heap.
        let apple = Arc::clone(&apple);

        thread::spawn(move || {
            // As Arc was used, threads can be spawned using the value allocated
            // in the Arc variable pointer's location.
            println!("{:?}", apple);
        });
    }

    // Make sure all Arc instances are printed from spawned threads.
    thread::sleep(Duration::from_secs(1));
}
```
