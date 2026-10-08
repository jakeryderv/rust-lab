<a id="section-macros"></a>

<a id="section-macros--macro_rules"></a>

# `macro_rules!`

[Chapter index](SUMMARY.md)

**In this chapter**

- [Syntax](#section-macros-syntax)
  - [Designators](#section-macros-designators)
  - [Overload](#section-macros-overload)
  - [Repeat](#section-macros-repeat)
- [DRY (Don't Repeat Yourself)](#section-macros-dry)
- [DSL (Domain Specific Languages)](#section-macros-dsl)
- [Variadics](#section-macros-variadics)


Rust provides a powerful macro system that allows metaprogramming. As you've
seen in previous chapters, macros look like functions, except that their name
ends with a bang `!`, but instead of generating a function call, macros are
expanded into source code that gets compiled with the rest of the program.
However, unlike macros in C and other languages, Rust macros are expanded into
abstract syntax trees, rather than string preprocessing, so you don't get
unexpected precedence bugs.

Macros can be created using the `macro_rules!` macro.

```rust
// This is a simple macro named `say_hello`.
macro_rules! say_hello {
    // `()` indicates that the macro takes no argument.
    () => {
        // The macro will expand into the contents of this block.
        println!("Hello!")
    };
}

fn main() {
    // This call will expand into `println!("Hello!")`
    say_hello!()
}
```

So why are macros useful?

1. Don't repeat yourself. There are many cases where you may need similar
   functionality in multiple places but with different types. Often, writing a
   macro is a useful way to avoid repeating code. (More on this later)

2. Domain-specific languages. Macros allow you to define special syntax for a
   specific purpose. (More on this later)

3. Variadic interfaces. Sometimes you want to define an interface that takes a
   variable number of arguments. An example is `println!` which could take any
   number of arguments, depending on the format string. (More on this later)

<a id="section-macros-syntax"></a>

<a id="section-macros-syntax--syntax"></a>

## Syntax

In following subsections, we will show how to define macros in Rust.
There are three basic ideas:

- [Patterns and Designators][section-macros-syntax-ref-1]
- [Overloading][section-macros-syntax-ref-2]
- [Repetition][section-macros-syntax-ref-3]

[section-macros-syntax-ref-1]: #section-macros-designators
[section-macros-syntax-ref-2]: #section-macros-overload
[section-macros-syntax-ref-3]: #section-macros-repeat

<a id="section-macros-designators"></a>

<a id="section-macros-designators--designators"></a>

### Designators

The arguments of a macro are prefixed by a dollar sign `$` and type annotated
with a *designator*:

```rust
macro_rules! create_function {
    // This macro takes an argument of designator `ident` and
    // creates a function named `$func_name`.
    // The `ident` designator is used for variable/function names.
    ($func_name:ident) => {
        fn $func_name() {
            // The `stringify!` macro converts an `ident` into a string.
            println!("You called {:?}()",
                     stringify!($func_name));
        }
    };
}

// Create functions named `foo` and `bar` with the above macro.
create_function!(foo);
create_function!(bar);

macro_rules! print_result {
    // This macro takes an expression of type `expr` and prints
    // it as a string along with its result.
    // The `expr` designator is used for expressions.
    ($expression:expr) => {
        // `stringify!` will convert the expression *as it is* into a string.
        println!("{:?} = {:?}",
                 stringify!($expression),
                 $expression);
    };
}

fn main() {
    foo();
    bar();

    print_result!(1u32 + 1);

    // Recall that blocks are expressions too!
    print_result!({
        let x = 1u32;

        x * x + 2 * x - 1
    });
}
```

These are some of the available designators:

* `block`
* `expr` is used for expressions
* `ident` is used for variable/function names
* `item`
* `literal` is used for literal constants
* `pat` (*pattern*)
* `path`
* `stmt` (*statement*)
* `tt` (*token tree*)
* `ty` (*type*)
* `vis` (*visibility qualifier*)

For a complete list, see the [Rust Reference][section-macros-designators-ref-1].

[section-macros-designators-ref-1]: https://doc.rust-lang.org/reference/macros-by-example.html

<a id="section-macros-overload"></a>

<a id="section-macros-overload--overload"></a>

### Overload

Macros can be overloaded to accept different combinations of arguments.
In that regard, `macro_rules!` can work similarly to a match block:

```rust
// `test!` will compare `$left` and `$right`
// in different ways depending on how you invoke it:
macro_rules! test {
    // Arguments don't need to be separated by a comma.
    // Any template can be used!
    ($left:expr; and $right:expr) => {
        println!("{:?} and {:?} is {:?}",
                 stringify!($left),
                 stringify!($right),
                 $left && $right)
    };
    // ^ each arm must end with a semicolon.
    ($left:expr; or $right:expr) => {
        println!("{:?} or {:?} is {:?}",
                 stringify!($left),
                 stringify!($right),
                 $left || $right)
    };
}

fn main() {
    test!(1i32 + 1 == 2i32; and 2i32 * 2 == 4i32);
    test!(true; or false);
}
```

<a id="section-macros-repeat"></a>

<a id="section-macros-repeat--repeat"></a>

### Repeat

Macros can use `+` in the argument list to indicate that an argument may
repeat at least once, or `*`, to indicate that the argument may repeat zero or
more times.

In the following example, surrounding the matcher with `$(...),+` will
match one or more expression, separated by commas.
Also note that the semicolon is optional on the last case.

```rust
// `find_min!` will calculate the minimum of any number of arguments.
macro_rules! find_min {
    // Base case:
    ($x:expr) => ($x);
    // `$x` followed by at least one `$y,`
    ($x:expr, $($y:expr),+) => (
        // Call `find_min!` on the tail `$y`
        std::cmp::min($x, find_min!($($y),+))
    )
}

fn main() {
    println!("{}", find_min!(1));
    println!("{}", find_min!(1 + 2, 2));
    println!("{}", find_min!(5, 2 * 3, 4));
}
```

<a id="section-macros-dry"></a>

<a id="section-macros-dry--dry-dont-repeat-yourself"></a>

## DRY (Don't Repeat Yourself)

Macros allow writing DRY code by factoring out the common parts of functions
and/or test suites. Here is an example that implements and tests the `+=`, `*=`
and `-=` operators on `Vec<T>`:

```rust
use std::ops::{Add, Mul, Sub};

macro_rules! assert_equal_len {
    // The `tt` (token tree) designator is used for
    // operators and tokens.
    ($a:expr, $b:expr, $func:ident, $op:tt) => {
        assert!($a.len() == $b.len(),
                "{:?}: dimension mismatch: {:?} {:?} {:?}",
                stringify!($func),
                ($a.len(),),
                stringify!($op),
                ($b.len(),));
    };
}

macro_rules! op {
    ($func:ident, $bound:ident, $op:tt, $method:ident) => {
        fn $func<T: $bound<T, Output=T> + Copy>(xs: &mut Vec<T>, ys: &Vec<T>) {
            assert_equal_len!(xs, ys, $func, $op);

            for (x, y) in xs.iter_mut().zip(ys.iter()) {
                *x = $bound::$method(*x, *y);
                // *x = x.$method(*y);
            }
        }
    };
}

// Implement `add_assign`, `mul_assign`, and `sub_assign` functions.
op!(add_assign, Add, +=, add);
op!(mul_assign, Mul, *=, mul);
op!(sub_assign, Sub, -=, sub);

mod test {
    use std::iter;
    macro_rules! test {
        ($func:ident, $x:expr, $y:expr, $z:expr) => {
            #[test]
            fn $func() {
                for size in 0usize..10 {
                    let mut x: Vec<_> = iter::repeat($x).take(size).collect();
                    let y: Vec<_> = iter::repeat($y).take(size).collect();
                    let z: Vec<_> = iter::repeat($z).take(size).collect();

                    super::$func(&mut x, &y);

                    assert_eq!(x, z);
                }
            }
        };
    }

    // Test `add_assign`, `mul_assign`, and `sub_assign`.
    test!(add_assign, 1u32, 2u32, 3u32);
    test!(mul_assign, 2u32, 3u32, 6u32);
    test!(sub_assign, 3u32, 2u32, 1u32);
}
```

```shell
$ rustc --test dry.rs && ./dry
running 3 tests
test test::mul_assign ... ok
test test::add_assign ... ok
test test::sub_assign ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured
```

<a id="section-macros-dsl"></a>

<a id="section-macros-dsl--domain-specific-languages-dsls"></a>

## Domain Specific Languages (DSLs)

A DSL is a mini "language" embedded in a Rust macro. It is completely valid
Rust because the macro system expands into normal Rust constructs, but it looks
like a small language. This allows you to define concise or intuitive syntax for
some special functionality (within bounds).

Suppose that I want to define a little calculator API. I would like to supply
an expression and have the output printed to console.

```rust
macro_rules! calculate {
    (eval $e:expr) => {
        {
            let val: usize = $e; // Force types to be unsigned integers
            println!("{} = {}", stringify!{$e}, val);
        }
    };
}

fn main() {
    calculate! {
        eval 1 + 2 // hehehe `eval` is _not_ a Rust keyword!
    }

    calculate! {
        eval (1 + 2) * (3 / 4)
    }
}
```

Output:

```txt
1 + 2 = 3
(1 + 2) * (3 / 4) = 0
```

This was a very simple example, but much more complex interfaces have been
developed, such as [`lazy_static`](https://crates.io/crates/lazy_static) or
[`clap`](https://crates.io/crates/clap).

Also, note the two pairs of braces in the macro. The outer ones are
part of the syntax of `macro_rules!`, in addition to `()` or `[]`.

<a id="section-macros-variadics"></a>

<a id="section-macros-variadics--variadic-interfaces"></a>

## Variadic Interfaces

A _variadic_ interface takes an arbitrary number of arguments. For example,
`println!` can take an arbitrary number of arguments, as determined by the
format string.

We can extend our `calculate!` macro from the previous section to be variadic:

```rust
macro_rules! calculate {
    // The pattern for a single `eval`
    (eval $e:expr) => {
        {
            let val: usize = $e; // Force types to be integers
            println!("{} = {}", stringify!{$e}, val);
        }
    };

    // Decompose multiple `eval`s recursively
    (eval $e:expr, $(eval $es:expr),+) => {{
        calculate! { eval $e }
        calculate! { $(eval $es),+ }
    }};
}

fn main() {
    calculate! { // Look ma! Variadic `calculate!`!
        eval 1 + 2,
        eval 3 + 4,
        eval (2 * 3) + 1
    }
}
```

Output:

```txt
1 + 2 = 3
3 + 4 = 7
(2 * 3) + 1 = 7
```
