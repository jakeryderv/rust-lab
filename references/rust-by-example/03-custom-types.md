<a id="section-custom_types"></a>

<a id="section-custom_types--custom-types"></a>

# Custom Types

[Chapter index](SUMMARY.md)

**In this chapter**

- [Structures](#section-custom_types-structs)
- [Enums](#section-custom_types-enum)
  - [use](#section-custom_types-enum-enum_use)
  - [C-like](#section-custom_types-enum-c_like)
  - [Testcase: linked-list](#section-custom_types-enum-testcase_linked_list)
- [constants](#section-custom_types-constants)


Rust custom data types are formed mainly through the two keywords:

* `struct`: define a structure
* `enum`: define an enumeration

Constants can also be created via the `const` and `static` keywords.

<a id="section-custom_types-structs"></a>

<a id="section-custom_types-structs--structures"></a>

## Structures

There are three types of structures ("structs") that can be created using the
`struct` keyword:

* Tuple structs, which are, basically, named tuples.
* The classic [C structs][section-custom_types-structs-ref-2]
* Unit structs, which are field-less, are useful for generics.

```rust
// An attribute to hide warnings for unused code.
#![allow(dead_code)]

#[derive(Debug)]
struct Person {
    name: String,
    age: u8,
}

// A unit struct
struct Unit;

// A tuple struct
struct Pair(i32, f32);

// A struct with two fields
struct Point {
    x: f32,
    y: f32,
}

// Structs can be reused as fields of another struct
struct Rectangle {
    // A rectangle can be specified by where the top left and bottom right
    // corners are in space.
    top_left: Point,
    bottom_right: Point,
}

fn main() {
    // Create struct with field init shorthand
    let name = String::from("Peter");
    let age = 27;
    let peter = Person { name, age };

    // Print debug struct
    println!("{:?}", peter);

    // Instantiate a `Point`
    let point: Point = Point { x: 5.2, y: 0.4 };
    let another_point: Point = Point { x: 10.3, y: 0.2 };

    // Access the fields of the point
    println!("point coordinates: ({}, {})", point.x, point.y);

    // Make a new point by using struct update syntax to use the fields of our
    // other one
    let bottom_right = Point { x: 10.3, ..another_point };

    // `bottom_right.y` will be the same as `another_point.y` because we used that field
    // from `another_point`
    println!("second point: ({}, {})", bottom_right.x, bottom_right.y);

    // Destructure the point using a `let` binding
    let Point { x: left_edge, y: top_edge } = point;

    let _rectangle = Rectangle {
        // struct instantiation is an expression too
        top_left: Point { x: left_edge, y: top_edge },
        bottom_right: bottom_right,
    };

    // Instantiate a unit struct
    let _unit = Unit;

    // Instantiate a tuple struct
    let pair = Pair(1, 0.1);

    // Access the fields of a tuple struct
    println!("pair contains {:?} and {:?}", pair.0, pair.1);

    // Destructure a tuple struct
    let Pair(integer, decimal) = pair;

    println!("pair contains {:?} and {:?}", integer, decimal);
}
```

<a id="section-custom_types-structs--activity"></a>

#### Activity

1. Add a function `rect_area` which calculates the area of a `Rectangle` (try
   using nested destructuring).
2. Add a function `square` which takes a `Point` and a `f32` as arguments, and
   returns a `Rectangle` with its top left corner on the point, and a width and
   height corresponding to the `f32`.

<a id="section-custom_types-structs--see-also"></a>

#### See also

[`attributes`][section-custom_types-structs-ref-1], [raw identifiers][section-custom_types-structs-ref-4] and [destructuring][section-custom_types-structs-ref-3]

[section-custom_types-structs-ref-1]: 13-attributes.md
[section-custom_types-structs-ref-2]: https://en.wikipedia.org/wiki/Struct_(C_programming_language)
[section-custom_types-structs-ref-3]: 08-flow-of-control.md#section-flow_control-match-destructuring
[section-custom_types-structs-ref-4]: 23-compatibility.md#section-compatibility-raw_identifiers

<a id="section-custom_types-enum"></a>

<a id="section-custom_types-enum--enums"></a>

## Enums

The `enum` keyword allows the creation of a type which may be one of a few
different variants. Any variant which is valid as a `struct` is also valid in
an `enum`.

```rust
// Create an `enum` to classify a web event. Note how both
// names and type information together specify the variant:
// `PageLoad != PageUnload` and `KeyPress(char) != Paste(String)`.
// Each is different and independent.
enum WebEvent {
    // An `enum` variant may either be `unit-like`,
    PageLoad,
    PageUnload,
    // like tuple structs,
    KeyPress(char),
    Paste(String),
    // or c-like structures.
    Click { x: i64, y: i64 },
}

// A function which takes a `WebEvent` enum as an argument and
// returns nothing.
fn inspect(event: WebEvent) {
    match event {
        WebEvent::PageLoad => println!("page loaded"),
        WebEvent::PageUnload => println!("page unloaded"),
        // Destructure `c` from inside the `enum` variant.
        WebEvent::KeyPress(c) => println!("pressed '{}'.", c),
        WebEvent::Paste(s) => println!("pasted \"{}\".", s),
        // Destructure `Click` into `x` and `y`.
        WebEvent::Click { x, y } => {
            println!("clicked at x={}, y={}.", x, y);
        },
    }
}

fn main() {
    let pressed = WebEvent::KeyPress('x');
    // `to_owned()` creates an owned `String` from a string slice.
    let pasted  = WebEvent::Paste("my text".to_owned());
    let click   = WebEvent::Click { x: 20, y: 80 };
    let load    = WebEvent::PageLoad;
    let unload  = WebEvent::PageUnload;

    inspect(pressed);
    inspect(pasted);
    inspect(click);
    inspect(load);
    inspect(unload);
}

```

<a id="section-custom_types-enum--type-aliases"></a>

### Type aliases

If you use a type alias, you can refer to each enum variant via its alias.
This might be useful if the enum's name is too long or too generic, and you
want to rename it.

```rust
enum VeryVerboseEnumOfThingsToDoWithNumbers {
    Add,
    Subtract,
}

// Creates a type alias
type Operations = VeryVerboseEnumOfThingsToDoWithNumbers;

fn main() {
    // We can refer to each variant via its alias, not its long and inconvenient
    // name.
    let x = Operations::Add;
}
```

The most common place you'll see this is in `impl` blocks using the `Self` alias.

```rust
enum VeryVerboseEnumOfThingsToDoWithNumbers {
    Add,
    Subtract,
}

impl VeryVerboseEnumOfThingsToDoWithNumbers {
    fn run(&self, x: i32, y: i32) -> i32 {
        match self {
            Self::Add => x + y,
            Self::Subtract => x - y,
        }
    }
}
```

To learn more about enums and type aliases, you can read the
[stabilization report][section-custom_types-enum-ref-5] from when this feature was stabilized into
Rust.

<a id="section-custom_types-enum--see-also"></a>

#### See also:

[`match`][section-custom_types-enum-ref-2], [`fn`][section-custom_types-enum-ref-3], and [`String`][section-custom_types-enum-ref-4], ["Type alias enum variants" RFC][section-custom_types-enum-ref-6]

[section-custom_types-enum-ref-1]: https://en.wikipedia.org/wiki/Struct_(C_programming_language)
[section-custom_types-enum-ref-2]: 08-flow-of-control.md#section-flow_control-match
[section-custom_types-enum-ref-3]: 09-functions.md
[section-custom_types-enum-ref-4]: 19-std-library-types.md#section-std-str
[section-custom_types-enum-ref-5]: https://github.com/rust-lang/rust/pull/61682/#issuecomment-502472847
[section-custom_types-enum-ref-6]: https://rust-lang.github.io/rfcs/2338-type-alias-enum-variants.html

<a id="section-custom_types-enum-enum_use"></a>

<a id="section-custom_types-enum-enum_use--use"></a>

### use

The `use` declaration can be used to avoid typing the full module path to access a name:

```rust
// An attribute to hide warnings for unused code.
#![allow(dead_code)]

enum Stage {
    Beginner,
    Advanced,
}

enum Role {
    Student,
    Teacher,
}

fn main() {
    // Explicitly `use` each name so they are available without
    // manual scoping.
    use Stage::{Beginner, Advanced};
    // Automatically `use` each name inside `Role`.
    use Role::*;

    // Equivalent to `Stage::Beginner`.
    let stage = Beginner;
    // Equivalent to `Role::Student`.
    let role = Student;

    match stage {
        // Note the lack of scoping because of the explicit `use` above.
        Beginner => println!("Beginners are starting their learning journey!"),
        Advanced => println!("Advanced learners are mastering their subjects..."),
    }

    match role {
        // Note again the lack of scoping.
        Student => println!("Students are acquiring knowledge!"),
        Teacher => println!("Teachers are spreading knowledge!"),
    }
}
```

<a id="section-custom_types-enum-enum_use--see-also"></a>

##### See also:

[`match`][section-custom_types-enum-enum_use-ref-2] and [`use`][section-custom_types-enum-enum_use-ref-1]

[section-custom_types-enum-enum_use-ref-1]: 10-modules.md#section-mod-use
[section-custom_types-enum-enum_use-ref-2]: 08-flow-of-control.md#section-flow_control-match

<a id="section-custom_types-enum-c_like"></a>

<a id="section-custom_types-enum-c_like--c-like"></a>

### C-like

`enum` can also be used as C-like enums.

```rust
// An attribute to hide warnings for unused code.
#![allow(dead_code)]

// enum with implicit discriminator (starts at 0)
enum Number {
    Zero,
    One,
    Two,
}

// enum with explicit discriminator
enum Color {
    Red = 0xff0000,
    Green = 0x00ff00,
    Blue = 0x0000ff,
}

fn main() {
    // `enums` can be cast as integers.
    println!("zero is {}", Number::Zero as i32);
    println!("one is {}", Number::One as i32);

    println!("roses are #{:06x}", Color::Red as u32);
    println!("violets are #{:06x}", Color::Blue as u32);
}
```

<a id="section-custom_types-enum-c_like--see-also"></a>

##### See also:

[casting][section-custom_types-enum-c_like-ref-1]

[section-custom_types-enum-c_like-ref-1]: 05-types.md#section-types-cast

<a id="section-custom_types-enum-testcase_linked_list"></a>

<a id="section-custom_types-enum-testcase_linked_list--testcase-linked-list"></a>

### Testcase: linked-list

A possible way to implement a linked list of `u32` elements is via enums:

```rust
enum LinkedList {
    // Next: Tuple struct that wraps an element and a boxed link to the next node
    Next(u32, Box<LinkedList>),
    // End: A node that signifies the end of the linked list
    End,
}

// `use` brings the enum variants into scope, so they can be used without the `LinkedList::` prefix
use LinkedList::*;

// Methods can be attached to an enum
impl LinkedList {
    // Create an empty linked list
    fn new() -> LinkedList {
        // `End` has type `LinkedList`
        End
    }

    // Take ownership of a linked list, and return a new one with a new element at its front
    fn prepend(self, elem: u32) -> LinkedList {
        // `Next` also has type `LinkedList`, since it is a variant of the `LinkedList` enum
        Next(elem, Box::new(self))
    }

    // Return the length of the linked list
    fn len(&self) -> u32 {
        // `len` depends on which enum variant we have, so we pattern-match on `self`
        // Since this method only borrows `self`, the `tail` binding is also a borrow
        // Note: In Rust 2018+, match infers the needed references automatically
        match self {
            // Count this node and recursively count the rest of the linked list
            // Note: this is not tail-recursive and could overflow for very long linked lists
            Next(_, tail) => 1 + tail.len(),
            // Base case: the empty linked list has length 0.
            End => 0,
        }
    }
}

// Implement `Display` for `LinkedList` so it can be printed to the console using `println!`
impl std::fmt::Display for LinkedList {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Next(head, tail) => write!(f, "({}, {})", head, tail),
            End => write!(f, "End"),
        }
    }
}

fn main() {
    // Create an empty linked list
    let mut list = LinkedList::new();

    // Prepend some elements
    list = list.prepend(1);
    list = list.prepend(2);
    list = list.prepend(3);

    // Show the final state of the list
    println!("linked list has length: {}", list.len());
    println!("{}", list);
}
```

<a id="section-custom_types-enum-testcase_linked_list--see-also"></a>

##### See also:

[`Box`][section-custom_types-enum-testcase_linked_list-ref-1] and [methods][section-custom_types-enum-testcase_linked_list-ref-2]

[section-custom_types-enum-testcase_linked_list-ref-1]: 19-std-library-types.md#section-std-box
[section-custom_types-enum-testcase_linked_list-ref-2]: 09-functions.md#section-fn-methods

<a id="section-custom_types-constants"></a>

<a id="section-custom_types-constants--constants"></a>

## constants

Rust has two different types of constants which can be declared in any scope
including global. Both require explicit type annotation:

* `const`: An unchangeable value (the common case).
* `static`: A possibly mutable variable with [`'static`][section-custom_types-constants-ref-1] lifetime.
  The static lifetime is inferred and does not have to be specified.
  Accessing or modifying a mutable static variable is [`unsafe`][section-custom_types-constants-ref-2].

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Globals are declared outside all other scopes.
static LANGUAGE: &str = "Rust";
const THRESHOLD: i32 = 10;

fn is_big(n: i32) -> bool {
    // Access constant in some function
    n > THRESHOLD
}

fn main() {
    let n = 16;

    // Access constant in the main thread
    println!("This is {}", LANGUAGE);
    println!("The threshold is {}", THRESHOLD);
    println!("{} is {}", n, if is_big(n) { "big" } else { "small" });

    // Error! Cannot modify a `const`.
    THRESHOLD = 5;
    // FIXME ^ Comment out this line
}
```

<a id="section-custom_types-constants--see-also"></a>

#### See also:

[The `const`/`static` RFC](
https://github.com/rust-lang/rfcs/blob/master/text/0246-const-vs-static.md),
[`'static` lifetime][section-custom_types-constants-ref-1]

[section-custom_types-constants-ref-1]: 15-scoping-rules.md#section-scope-lifetime-static_lifetime
[section-custom_types-constants-ref-2]: 22-unsafe-operations.md
