<a id="section-error"></a>

<a id="section-error--error-handling"></a>

# Error handling

[Chapter index](SUMMARY.md)

**In this chapter**

- [`panic`](#section-error-panic)
- [`abort` & `unwind`](#section-error-abort_unwind)
- [`Option` & `unwrap`](#section-error-option_unwrap)
  - [Unpacking options with `?`](#section-error-option_unwrap-question_mark)
  - [Combinators: `map`](#section-error-option_unwrap-map)
  - [Combinators: `and_then`](#section-error-option_unwrap-and_then)
  - [Defaults: `or`, `or_else`, `get_or_insert`, `get_or_insert_with`](#section-error-option_unwrap-defaults)
- [`Result`](#section-error-result)
  - [`map` for `Result`](#section-error-result-result_map)
  - [aliases for `Result`](#section-error-result-result_alias)
  - [Early returns](#section-error-result-early_returns)
  - [Introducing `?`](#section-error-result-enter_question_mark)
- [Multiple error types](#section-error-multiple_error_types)
  - [Pulling `Result`s out of `Option`s](#section-error-multiple_error_types-option_result)
  - [Defining an error type](#section-error-multiple_error_types-define_error_type)
  - [`Box`ing errors](#section-error-multiple_error_types-boxing_errors)
  - [Other uses of `?`](#section-error-multiple_error_types-reenter_question_mark)
  - [Wrapping errors](#section-error-multiple_error_types-wrap_error)
- [Iterating over `Result`s](#section-error-iter_result)


Error handling is the process of handling the possibility of failure. For
example, failing to read a file and then continuing to use that *bad* input
would clearly be problematic. Noticing and explicitly managing those errors
saves the rest of the program from various pitfalls.

There are various ways to deal with errors in Rust, which are described in the
following subchapters. They all have more or less subtle differences and different
use cases. As a rule of thumb:

An explicit `panic` is mainly useful for tests and dealing with unrecoverable errors.
For prototyping it can be useful, for example when dealing with functions that
haven't been implemented yet, but in those cases the more descriptive `unimplemented`
is better. In tests `panic` is a reasonable way to explicitly fail.

The `Option` type is for when a value is optional or when the lack of a value is
not an error condition. For example the parent of a directory - `/` and `C:` don't
have one. When dealing with `Option`s, `unwrap` is fine for prototyping and cases
where it's absolutely certain that there is guaranteed to be a value. However `expect`
is more useful since it lets you specify an error message in case something goes
wrong anyway.

When there is a chance that things do go wrong and the caller has to deal with the
problem, use `Result`. You can `unwrap` and `expect` them as well (please don't
do that unless it's a test or quick prototype).

For a more rigorous discussion of error handling, refer to the error
handling section in the [official book][section-error-ref-1].

[section-error-ref-1]: https://doc.rust-lang.org/book/ch09-00-error-handling.html

<a id="section-error-panic"></a>

<a id="section-error-panic--panic"></a>

## `panic`

The simplest error handling mechanism we will see is `panic`. It prints an
error message, starts unwinding the stack, and usually exits the program.
Here, we explicitly call `panic` on our error condition:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn drink(beverage: &str) {
    // You shouldn't drink too many sugary beverages.
    if beverage == "lemonade" { panic!("AAAaaaaa!!!!"); }

    println!("Some refreshing {} is all I need.", beverage);
}

fn main() {
    drink("water");
    drink("lemonade");
    drink("still water");
}
```

The first call to `drink` works. The second panics and thus the third is never called.

<a id="section-error-abort_unwind"></a>

<a id="section-error-abort_unwind--abort-and-unwind"></a>

## `abort` and `unwind`

The previous section illustrates the error handling mechanism `panic`.  Different code paths can be conditionally compiled based on the panic setting. The current values available are `unwind` and `abort`.

Building on the prior lemonade example, we explicitly use the panic strategy to exercise different lines of code.

```rust
fn drink(beverage: &str) {
    // You shouldn't drink too much sugary beverages.
    if beverage == "lemonade" {
        if cfg!(panic = "abort") {
            println!("This is not your party. Run!!!!");
        } else {
            println!("Spit it out!!!!");
        }
    } else {
        println!("Some refreshing {} is all I need.", beverage);
    }
}

fn main() {
    drink("water");
    drink("lemonade");
}
```

Here is another example focusing on rewriting `drink()` and explicitly use the `unwind` keyword.

```rust
#[cfg(panic = "unwind")]
fn ah() {
    println!("Spit it out!!!!");
}

#[cfg(not(panic = "unwind"))]
fn ah() {
    println!("This is not your party. Run!!!!");
}

fn drink(beverage: &str) {
    if beverage == "lemonade" {
        ah();
    } else {
        println!("Some refreshing {} is all I need.", beverage);
    }
}

fn main() {
    drink("water");
    drink("lemonade");
}
```

The panic strategy can be set from the command line by using `abort` or `unwind`.

```console
rustc  lemonade.rs -C panic=abort
```

<a id="section-error-option_unwrap"></a>

<a id="section-error-option_unwrap--option--unwrap"></a>

## `Option` & `unwrap`

In the last example, we showed that we can induce program failure at will.
We told our program to `panic` if we drink a sugary lemonade.
But what if we expect _some_ drink but don't receive one?
That case would be just as bad, so it needs to be handled!

We _could_ test this against the null string (`""`) as we do with a lemonade.
Since we're using Rust, let's instead have the compiler point out cases
where there's no drink.

An `enum` called `Option<T>` in the `std` library is used when absence is a
possibility. It manifests itself as one of two "options":

* `Some(T)`: An element of type `T` was found
* `None`: No element was found

These cases can either be explicitly handled via `match` or implicitly with
`unwrap`. Implicit handling will either return the inner element or `panic`.

Note that it's possible to manually customize `panic` with [expect][section-error-option_unwrap-ref-1],
but `unwrap` otherwise leaves us with a less meaningful output than explicit
handling. In the following example, explicit handling yields a more
controlled result while retaining the option to `panic` if desired.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// The adult has seen it all, and can handle any drink well.
// All drinks are handled explicitly using `match`.
fn give_adult(drink: Option<&str>) {
    // Specify a course of action for each case.
    match drink {
        Some("lemonade") => println!("Yuck! Too sugary."),
        Some(inner)   => println!("{}? How nice.", inner),
        None          => println!("No drink? Oh well."),
    }
}

// Others will `panic` before drinking sugary drinks.
// All drinks are handled implicitly using `unwrap`.
fn drink(drink: Option<&str>) {
    // `unwrap` returns a `panic` when it receives a `None`.
    let inside = drink.unwrap();
    if inside == "lemonade" { panic!("AAAaaaaa!!!!"); }

    println!("I love {}s!!!!!", inside);
}

fn main() {
    let water  = Some("water");
    let lemonade = Some("lemonade");
    let void  = None;

    give_adult(water);
    give_adult(lemonade);
    give_adult(void);

    let coffee = Some("coffee");
    let nothing = None;

    drink(coffee);
    drink(nothing);
}
```

[section-error-option_unwrap-ref-1]: https://doc.rust-lang.org/std/option/enum.Option.html#method.expect

<a id="section-error-option_unwrap-question_mark"></a>

<a id="section-error-option_unwrap-question_mark--unpacking-options-with-"></a>

### Unpacking options with `?`

You can unpack `Option`s by using `match` statements, but it's often easier to
use the `?` operator. If `x` is an `Option`, then evaluating `x?` will return
the underlying value if `x` is `Some`, otherwise it will terminate whatever
function is being executed and return `None`.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn next_birthday(current_age: Option<u8>) -> Option<String> {
    // If `current_age` is `None`, this returns `None`.
    // If `current_age` is `Some`, the inner `u8` value + 1
    // gets assigned to `next_age`
    let next_age: u8 = current_age? + 1;
    Some(format!("Next year I will be {}", next_age))
}
```

You can chain many `?`s together to make your code much more readable.

```rust
struct Person {
    job: Option<Job>,
}

#[derive(Clone, Copy)]
struct Job {
    phone_number: Option<PhoneNumber>,
}

#[derive(Clone, Copy)]
#[allow(dead_code)]
struct PhoneNumber {
    area_code: Option<u8>,
    number: u32,
}

impl Person {

    // Gets the area code of the phone number of the person's job, if it exists.
    fn work_phone_area_code(&self) -> Option<u8> {
        // This would need many nested `match` statements without the `?` operator.
        // It would take a lot more code - try writing it yourself and see which
        // is easier.
        self.job?.phone_number?.area_code
    }
}

fn main() {
    let p = Person {
        job: Some(Job {
            phone_number: Some(PhoneNumber {
                area_code: Some(61),
                number: 439222222,
            }),
        }),
    };

    assert_eq!(p.work_phone_area_code(), Some(61));
}
```

<a id="section-error-option_unwrap-map"></a>

<a id="section-error-option_unwrap-map--combinators-map"></a>

### Combinators: `map`

`match` is a valid method for handling `Option`s. However, you may
eventually find heavy usage tedious, especially with operations only valid
with an input. In these cases, [combinators][section-error-option_unwrap-map-ref-1] can be used to
manage control flow in a modular fashion.

`Option` has a built in method called `map()`, a combinator for the simple
mapping of `Some -> Some` and `None -> None`. Multiple `map()` calls can be
chained together for even more flexibility.

In the following example, `process()` replaces all functions previous
to it while staying compact.

```rust
#![allow(dead_code)]

#[derive(Debug)] enum Food { Apple, Carrot, Potato }

#[derive(Debug)] struct Peeled(Food);
#[derive(Debug)] struct Chopped(Food);
#[derive(Debug)] struct Cooked(Food);

// Peeling food. If there isn't any, then return `None`.
// Otherwise, return the peeled food.
fn peel(food: Option<Food>) -> Option<Peeled> {
    match food {
        Some(food) => Some(Peeled(food)),
        None       => None,
    }
}

// Chopping food. If there isn't any, then return `None`.
// Otherwise, return the chopped food.
fn chop(peeled: Option<Peeled>) -> Option<Chopped> {
    match peeled {
        Some(Peeled(food)) => Some(Chopped(food)),
        None               => None,
    }
}

// Cooking food. Here, we showcase `map()` instead of `match` for case handling.
fn cook(chopped: Option<Chopped>) -> Option<Cooked> {
    chopped.map(|Chopped(food)| Cooked(food))
}

// A function to peel, chop, and cook food all in sequence.
// We chain multiple uses of `map()` to simplify the code.
fn process(food: Option<Food>) -> Option<Cooked> {
    food.map(|f| Peeled(f))
        .map(|Peeled(f)| Chopped(f))
        .map(|Chopped(f)| Cooked(f))
}

// Check whether there's food or not before trying to eat it!
fn eat(food: Option<Cooked>) {
    match food {
        Some(food) => println!("Mmm. I love {:?}", food),
        None       => println!("Oh no! It wasn't edible."),
    }
}

fn main() {
    let apple = Some(Food::Apple);
    let carrot = Some(Food::Carrot);
    let potato = None;

    let cooked_apple = cook(chop(peel(apple)));
    let cooked_carrot = cook(chop(peel(carrot)));
    // Let's try the simpler looking `process()` now.
    let cooked_potato = process(potato);

    eat(cooked_apple);
    eat(cooked_carrot);
    eat(cooked_potato);
}
```

<a id="section-error-option_unwrap-map--see-also"></a>

##### See also:

[closures][section-error-option_unwrap-map-ref-2], [`Option`][section-error-option_unwrap-map-ref-3], [`Option::map()`][section-error-option_unwrap-map-ref-4]

[section-error-option_unwrap-map-ref-1]: https://doc.rust-lang.org/reference/glossary.html#combinator
[section-error-option_unwrap-map-ref-2]: 09-functions.md#section-fn-closures
[section-error-option_unwrap-map-ref-3]: https://doc.rust-lang.org/std/option/enum.Option.html
[section-error-option_unwrap-map-ref-4]: https://doc.rust-lang.org/std/option/enum.Option.html#method.map

<a id="section-error-option_unwrap-and_then"></a>

<a id="section-error-option_unwrap-and_then--combinators-and_then"></a>

### Combinators: `and_then`

`map()` was described as a chainable way to simplify `match` statements.
However, using `map()` on a function that returns an `Option<T>` results
in the nested `Option<Option<T>>`. Chaining multiple calls together can
then become confusing. That's where another combinator called `and_then()`,
known in some languages as flatmap, comes in.

`and_then()` calls its function input with the wrapped value and returns the result. If the `Option` is `None`, then it returns `None` instead.

In the following example, `cookable_v3()` results in an `Option<Food>`.
Using `map()` instead of `and_then()` would have given an
`Option<Option<Food>>`, which is an invalid type for `eat()`.

```rust
#![allow(dead_code)]

#[derive(Debug)] enum Food { CordonBleu, Steak, Sushi }
#[derive(Debug)] enum Day { Monday, Tuesday, Wednesday }

// We don't have the ingredients to make Sushi.
fn have_ingredients(food: Food) -> Option<Food> {
    match food {
        Food::Sushi => None,
        _           => Some(food),
    }
}

// We have the recipe for everything except Cordon Bleu.
fn have_recipe(food: Food) -> Option<Food> {
    match food {
        Food::CordonBleu => None,
        _                => Some(food),
    }
}

// To make a dish, we need both the recipe and the ingredients.
// We can represent the logic with a chain of `match`es:
fn cookable_v1(food: Food) -> Option<Food> {
    match have_recipe(food) {
        None       => None,
        Some(food) => have_ingredients(food),
    }
}

// This can conveniently be rewritten more compactly with `and_then()`:
fn cookable_v3(food: Food) -> Option<Food> {
    have_recipe(food).and_then(have_ingredients)
}

// Otherwise we'd need to `flatten()` an `Option<Option<Food>>`
// to get an `Option<Food>`:
fn cookable_v2(food: Food) -> Option<Food> {
    have_recipe(food).map(have_ingredients).flatten()
}

fn eat(food: Food, day: Day) {
    match cookable_v3(food) {
        Some(food) => println!("Yay! On {:?} we get to eat {:?}.", day, food),
        None       => println!("Oh no. We don't get to eat on {:?}?", day),
    }
}

fn main() {
    let (cordon_bleu, steak, sushi) = (Food::CordonBleu, Food::Steak, Food::Sushi);

    eat(cordon_bleu, Day::Monday);
    eat(steak, Day::Tuesday);
    eat(sushi, Day::Wednesday);
}
```

<a id="section-error-option_unwrap-and_then--see-also"></a>

##### See also:

[closures][section-error-option_unwrap-and_then-ref-1], [`Option`][section-error-option_unwrap-and_then-ref-2], [`Option::and_then()`][section-error-option_unwrap-and_then-ref-3], and [`Option::flatten()`][section-error-option_unwrap-and_then-ref-4]

[section-error-option_unwrap-and_then-ref-1]: 09-functions.md#section-fn-closures
[section-error-option_unwrap-and_then-ref-2]: https://doc.rust-lang.org/std/option/enum.Option.html
[section-error-option_unwrap-and_then-ref-3]: https://doc.rust-lang.org/std/option/enum.Option.html#method.and_then
[section-error-option_unwrap-and_then-ref-4]: https://doc.rust-lang.org/std/option/enum.Option.html#method.flatten

<a id="section-error-option_unwrap-defaults"></a>

<a id="section-error-option_unwrap-defaults--unpacking-options-and-defaults"></a>

### Unpacking options and defaults

There is more than one way to unpack an `Option` and fall back on a default if it is `None`. To choose the one that meets our needs, we need to consider the following:

* do we need eager or lazy evaluation?
* do we need to keep the original empty value intact, or modify it in place?

<a id="section-error-option_unwrap-defaults--or-is-chainable-evaluates-eagerly-keeps-empty-value-intact"></a>

#### `or()` is chainable, evaluates eagerly, keeps empty value intact

`or()`is chainable and eagerly evaluates its argument, as is shown in the following example. Note that because `or`'s arguments are evaluated eagerly, the variable passed to `or` is moved.

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let apple = Some(Fruit::Apple);
    let orange = Some(Fruit::Orange);
    let no_fruit: Option<Fruit> = None;

    let first_available_fruit = no_fruit.or(orange).or(apple);
    println!("first_available_fruit: {:?}", first_available_fruit);
    // first_available_fruit: Some(Orange)

    // `or` moves its argument.
    // In the example above, `or(orange)` returned a `Some`, so `or(apple)` was not invoked.
    // But the variable named `apple` has been moved regardless, and cannot be used anymore.
    // println!("Variable apple was moved, so this line won't compile: {:?}", apple);
    // TODO: uncomment the line above to see the compiler error
}
```

<a id="section-error-option_unwrap-defaults--or_else-is-chainable-evaluates-lazily-keeps-empty-value-intact"></a>

#### `or_else()` is chainable, evaluates lazily, keeps empty value intact

Another alternative is to use `or_else`, which is also chainable, and evaluates lazily, as is shown in the following example:

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let no_fruit: Option<Fruit> = None;
    let get_kiwi_as_fallback = || {
        println!("Providing kiwi as fallback");
        Some(Fruit::Kiwi)
    };
    let get_lemon_as_fallback = || {
        println!("Providing lemon as fallback");
        Some(Fruit::Lemon)
    };

    let first_available_fruit = no_fruit
        .or_else(get_kiwi_as_fallback)
        .or_else(get_lemon_as_fallback);
    println!("first_available_fruit: {:?}", first_available_fruit);
    // Providing kiwi as fallback
    // first_available_fruit: Some(Kiwi)
}
```

<a id="section-error-option_unwrap-defaults--get_or_insert-evaluates-eagerly-modifies-empty-value-in-place"></a>

#### `get_or_insert()` evaluates eagerly, modifies empty value in place

To make sure that an `Option` contains a value, we can use `get_or_insert` to modify it in place with a fallback value, as is shown in the following example. Note that `get_or_insert` eagerly evaluates its parameter, so variable `apple` is moved:

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let mut my_fruit: Option<Fruit> = None;
    let apple = Fruit::Apple;
    let first_available_fruit = my_fruit.get_or_insert(apple);
    println!("first_available_fruit is: {:?}", first_available_fruit);
    println!("my_fruit is: {:?}", my_fruit);
    // first_available_fruit is: Apple
    // my_fruit is: Some(Apple)
    //println!("Variable named `apple` is moved: {:?}", apple);
    // TODO: uncomment the line above to see the compiler error
}
```

<a id="section-error-option_unwrap-defaults--get_or_insert_with-evaluates-lazily-modifies-empty-value-in-place"></a>

#### `get_or_insert_with()` evaluates lazily, modifies empty value in place

Instead of explicitly providing a value to fall back on, we can pass a closure to `get_or_insert_with`, as follows:

```rust
#[derive(Debug)]
enum Fruit { Apple, Orange, Banana, Kiwi, Lemon }

fn main() {
    let mut my_fruit: Option<Fruit> = None;
    let get_lemon_as_fallback = || {
        println!("Providing lemon as fallback");
        Fruit::Lemon
    };
    let first_available_fruit = my_fruit
        .get_or_insert_with(get_lemon_as_fallback);
    println!("first_available_fruit is: {:?}", first_available_fruit);
    println!("my_fruit is: {:?}", my_fruit);
    // Providing lemon as fallback
    // first_available_fruit is: Lemon
    // my_fruit is: Some(Lemon)

    // If the Option has a value, it is left unchanged, and the closure is not invoked
    let mut my_apple = Some(Fruit::Apple);
    let should_be_apple = my_apple.get_or_insert_with(get_lemon_as_fallback);
    println!("should_be_apple is: {:?}", should_be_apple);
    println!("my_apple is unchanged: {:?}", my_apple);
    // The output is a follows. Note that the closure `get_lemon_as_fallback` is not invoked
    // should_be_apple is: Apple
    // my_apple is unchanged: Some(Apple)
}
```

<a id="section-error-option_unwrap-defaults--see-also"></a>

##### See also:

[`closures`][section-error-option_unwrap-defaults-ref-1], [`get_or_insert`][section-error-option_unwrap-defaults-ref-2], [`get_or_insert_with`][section-error-option_unwrap-defaults-ref-3], [`moved variables`][section-error-option_unwrap-defaults-ref-4], [`or`][section-error-option_unwrap-defaults-ref-5], [`or_else`][section-error-option_unwrap-defaults-ref-6]

[section-error-option_unwrap-defaults-ref-1]: https://doc.rust-lang.org/book/ch13-01-closures.html
[section-error-option_unwrap-defaults-ref-2]: https://doc.rust-lang.org/core/option/enum.Option.html#method.get_or_insert
[section-error-option_unwrap-defaults-ref-3]: https://doc.rust-lang.org/core/option/enum.Option.html#method.get_or_insert_with
[section-error-option_unwrap-defaults-ref-4]: https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html
[section-error-option_unwrap-defaults-ref-5]: https://doc.rust-lang.org/core/option/enum.Option.html#method.or
[section-error-option_unwrap-defaults-ref-6]: https://doc.rust-lang.org/core/option/enum.Option.html#method.or_else

<a id="section-error-result"></a>

<a id="section-error-result--result"></a>

## `Result`

[`Result`][section-error-result-ref-2] is a richer version of the [`Option`][section-error-result-ref-1] type that
describes possible *error* instead of possible *absence*.

That is, `Result<T, E>` could have one of two outcomes:

* `Ok(T)`: An element `T` was found
* `Err(E)`: An error was found with element `E`

By convention, the expected outcome is `Ok` while the unexpected outcome is `Err`.

Like `Option`, `Result` has many methods associated with it. `unwrap()`, for
example, either yields the element `T` or `panic`s. For case handling,
there are many combinators between `Result` and `Option` that overlap.

In working with Rust, you will likely encounter methods that return the
`Result` type, such as the [`parse()`][section-error-result-ref-3] method. It might not always
be possible to parse a string into the other type, so `parse()` returns a
`Result` indicating possible failure.

Let's see what happens when we successfully and unsuccessfully `parse()` a string:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn multiply(first_number_str: &str, second_number_str: &str) -> i32 {
    // Let's try using `unwrap()` to get the number out. Will it bite us?
    let first_number = first_number_str.parse::<i32>().unwrap();
    let second_number = second_number_str.parse::<i32>().unwrap();
    first_number * second_number
}

fn main() {
    let twenty = multiply("10", "2");
    println!("double is {}", twenty);

    let tt = multiply("t", "2");
    println!("double is {}", tt);
}
```

In the unsuccessful case, `parse()` leaves us with an error for `unwrap()`
to `panic` on. Additionally, the `panic` exits our program and provides an
unpleasant error message.

To improve the quality of our error message, we should be more specific
about the return type and consider explicitly handling the error.

<a id="section-error-result--using-result-in-main"></a>

### Using `Result` in `main`

The `Result` type can also be the return type of the `main` function if
specified explicitly. Typically the `main` function will be of the form:

```rust
fn main() {
    println!("Hello World!");
}
```

However `main` is also able to have a return type of `Result`. If an error
occurs within the `main` function it will return an error code and print a debug
representation of the error (using the [`Debug`][section-error-result-ref-4] trait). The following example
shows such a scenario and touches on aspects covered in [the following section][section-error-result-ref-5].

```rust
use std::num::ParseIntError;

fn main() -> Result<(), ParseIntError> {
    let number_str = "10";
    let number = match number_str.parse::<i32>() {
        Ok(number)  => number,
        Err(e) => return Err(e),
    };
    println!("{}", number);
    Ok(())
}
```

[section-error-result-ref-1]: https://doc.rust-lang.org/std/option/enum.Option.html
[section-error-result-ref-2]: https://doc.rust-lang.org/std/result/enum.Result.html
[section-error-result-ref-3]: https://doc.rust-lang.org/std/primitive.str.html#method.parse
[section-error-result-ref-4]: https://doc.rust-lang.org/std/fmt/trait.Debug.html
[section-error-result-ref-5]: #section-error-result-early_returns

<a id="section-error-result-result_map"></a>

<a id="section-error-result-result_map--map-for-result"></a>

### `map` for `Result`

Panicking in the previous example's `multiply` does not make for robust code.
Generally, we want to return the error to the caller so it can decide what is
the right way to respond to errors.

We first need to know what kind of error type we are dealing with. To determine
the `Err` type, we look to [`parse()`][section-error-result-result_map-ref-1], which is implemented with the
[`FromStr`][section-error-result-result_map-ref-2] trait for [`i32`][section-error-result-result_map-ref-3]. As a result, the `Err` type is
specified as [`ParseIntError`][section-error-result-result_map-ref-4].

In the example below, the straightforward `match` statement leads to code
that is overall more cumbersome.

```rust
use std::num::ParseIntError;

// With the return type rewritten, we use pattern matching without `unwrap()`.
fn multiply(first_number_str: &str, second_number_str: &str) -> Result<i32, ParseIntError> {
    match first_number_str.parse::<i32>() {
        Ok(first_number)  => {
            match second_number_str.parse::<i32>() {
                Ok(second_number)  => {
                    Ok(first_number * second_number)
                },
                Err(e) => Err(e),
            }
        },
        Err(e) => Err(e),
    }
}

fn print(result: Result<i32, ParseIntError>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    // This still presents a reasonable answer.
    let twenty = multiply("10", "2");
    print(twenty);

    // The following now provides a much more helpful error message.
    let tt = multiply("t", "2");
    print(tt);
}
```

Luckily, `Option`'s `map`, `and_then`, and many other combinators are also
implemented for `Result`. [`Result`][section-error-result-result_map-ref-5] contains a complete listing.

```rust
use std::num::ParseIntError;

// As with `Option`, we can use combinators such as `map()`.
// This function is otherwise identical to the one above and reads:
// Multiply if both values can be parsed from str, otherwise pass on the error.
fn multiply(first_number_str: &str, second_number_str: &str) -> Result<i32, ParseIntError> {
    first_number_str.parse::<i32>().and_then(|first_number| {
        second_number_str.parse::<i32>().map(|second_number| first_number * second_number)
    })
}

fn print(result: Result<i32, ParseIntError>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    // This still presents a reasonable answer.
    let twenty = multiply("10", "2");
    print(twenty);

    // The following now provides a much more helpful error message.
    let tt = multiply("t", "2");
    print(tt);
}
```

[section-error-result-result_map-ref-1]: https://doc.rust-lang.org/std/primitive.str.html#method.parse
[section-error-result-result_map-ref-2]: https://doc.rust-lang.org/std/str/trait.FromStr.html
[section-error-result-result_map-ref-3]: https://doc.rust-lang.org/std/primitive.i32.html
[section-error-result-result_map-ref-4]: https://doc.rust-lang.org/std/num/struct.ParseIntError.html
[section-error-result-result_map-ref-5]: https://doc.rust-lang.org/std/result/enum.Result.html

<a id="section-error-result-result_alias"></a>

<a id="section-error-result-result_alias--aliases-for-result"></a>

### aliases for `Result`

How about when we want to reuse a specific `Result` type many times?
Recall that Rust allows us to create [aliases][section-error-result-result_alias-ref-1]. Conveniently,
we can define one for the specific `Result` in question.

At a module level, creating aliases can be particularly helpful. Errors
found in a specific module often have the same `Err` type, so a single alias
can succinctly define *all* associated `Results`. This is so useful that the
`std` library even supplies one: [`io::Result`][section-error-result-result_alias-ref-2]!

Here's a quick example to show off the syntax:

```rust
use std::num::ParseIntError;

// Define a generic alias for a `Result` with the error type `ParseIntError`.
type AliasedResult<T> = Result<T, ParseIntError>;

// Use the above alias to refer to our specific `Result` type.
fn multiply(first_number_str: &str, second_number_str: &str) -> AliasedResult<i32> {
    first_number_str.parse::<i32>().and_then(|first_number| {
        second_number_str.parse::<i32>().map(|second_number| first_number * second_number)
    })
}

// Here, the alias again allows us to save some space.
fn print(result: AliasedResult<i32>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    print(multiply("10", "2"));
    print(multiply("t", "2"));
}
```

<a id="section-error-result-result_alias--see-also"></a>

##### See also:

[`io::Result`][section-error-result-result_alias-ref-2]

[section-error-result-result_alias-ref-1]: 05-types.md#section-types-alias
[section-error-result-result_alias-ref-2]: https://doc.rust-lang.org/std/io/type.Result.html

<a id="section-error-result-early_returns"></a>

<a id="section-error-result-early_returns--early-returns"></a>

### Early returns

In the previous example, we explicitly handled the errors using combinators.
Another way to deal with this case analysis is to use a combination of
`match` statements and *early returns*.

That is, we can simply stop executing the function and return the error if
one occurs. For some, this form of code can be easier to both read and
write. Consider this version of the previous example, rewritten using early returns:

```rust
use std::num::ParseIntError;

fn multiply(first_number_str: &str, second_number_str: &str) -> Result<i32, ParseIntError> {
    let first_number = match first_number_str.parse::<i32>() {
        Ok(first_number)  => first_number,
        Err(e) => return Err(e),
    };

    let second_number = match second_number_str.parse::<i32>() {
        Ok(second_number)  => second_number,
        Err(e) => return Err(e),
    };

    Ok(first_number * second_number)
}

fn print(result: Result<i32, ParseIntError>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    print(multiply("10", "2"));
    print(multiply("t", "2"));
}
```

At this point, we've learned to explicitly handle errors using combinators
and early returns. While we generally want to avoid panicking, explicitly
handling all of our errors is cumbersome.

In the next section, we'll introduce `?` for the cases where we simply
need to `unwrap` without possibly inducing `panic`.

<a id="section-error-result-enter_question_mark"></a>

<a id="section-error-result-enter_question_mark--introducing-"></a>

### Introducing `?`

Sometimes we just want the simplicity of `unwrap` without the possibility of
a `panic`. Until now, `unwrap` has forced us to nest deeper and deeper when
what we really wanted was to get the variable *out*. This is exactly the purpose of `?`.

Upon finding an `Err`, there are two valid actions to take:

1. `panic!` which we already decided to try to avoid if possible
2. `return` because an `Err` means it cannot be handled

`?` is *almost*[^section-error-result-enter_question_mark-†] exactly equivalent to an `unwrap` which `return`s
instead of `panic`king on `Err`s. Let's see how we can simplify the earlier
example that used combinators:

```rust
use std::num::ParseIntError;

fn multiply(first_number_str: &str, second_number_str: &str) -> Result<i32, ParseIntError> {
    let first_number = first_number_str.parse::<i32>()?;
    let second_number = second_number_str.parse::<i32>()?;

    Ok(first_number * second_number)
}

fn print(result: Result<i32, ParseIntError>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    print(multiply("10", "2"));
    print(multiply("t", "2"));
}
```

<a id="section-error-result-enter_question_mark--the-try-macro"></a>

#### The `try!` macro

Before there was `?`, the same functionality was achieved with the `try!` macro.
The `?` operator is now recommended, but you may still find `try!` when looking
at older code. The same `multiply` function from the previous example
would look like this using `try!`:

> **Example note:** This example uses Rust edition 2015.

```rust
// To compile and run this example without errors, while using Cargo, change the value
// of the `edition` field, in the `[package]` section of the `Cargo.toml` file, to "2015".

use std::num::ParseIntError;

fn multiply(first_number_str: &str, second_number_str: &str) -> Result<i32, ParseIntError> {
    let first_number = try!(first_number_str.parse::<i32>());
    let second_number = try!(second_number_str.parse::<i32>());

    Ok(first_number * second_number)
}

fn print(result: Result<i32, ParseIntError>) {
    match result {
        Ok(n)  => println!("n is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    print(multiply("10", "2"));
    print(multiply("t", "2"));
}
```

[^section-error-result-enter_question_mark-†]: See [re-enter ?][section-error-result-enter_question_mark-ref-1] for more details.

[section-error-result-enter_question_mark-ref-1]: #section-error-multiple_error_types-reenter_question_mark

<a id="section-error-multiple_error_types"></a>

<a id="section-error-multiple_error_types--multiple-error-types"></a>

## Multiple error types

The previous examples have always been very convenient; `Result`s interact
with other `Result`s and `Option`s interact with other `Option`s.

Sometimes an `Option` needs to interact with a `Result`, or a
`Result<T, Error1>` needs to interact with a `Result<T, Error2>`. In those
cases, we want to manage our different error types in a way that makes them
composable and easy to interact with.

In the following code, two instances of `unwrap` generate different error
types. `Vec::first` returns an `Option`, while `parse::<i32>` returns a
`Result<i32, ParseIntError>`:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn double_first(vec: Vec<&str>) -> i32 {
    let first = vec.first().unwrap(); // Generate error 1
    2 * first.parse::<i32>().unwrap() // Generate error 2
}

fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    println!("The first doubled is {}", double_first(numbers));

    println!("The first doubled is {}", double_first(empty));
    // Error 1: the input vector is empty

    println!("The first doubled is {}", double_first(strings));
    // Error 2: the element doesn't parse to a number
}
```

Over the next sections, we'll see several strategies for handling these kind of problems.

<a id="section-error-multiple_error_types-option_result"></a>

<a id="section-error-multiple_error_types-option_result--pulling-results-out-of-options"></a>

### Pulling `Result`s out of `Option`s

The most basic way of handling mixed error types is to just embed them in each
other.

```rust
use std::num::ParseIntError;

fn double_first(vec: Vec<&str>) -> Option<Result<i32, ParseIntError>> {
    vec.first().map(|first| {
        first.parse::<i32>().map(|n| 2 * n)
    })
}

fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    println!("The first doubled is {:?}", double_first(numbers));

    println!("The first doubled is {:?}", double_first(empty));
    // Error 1: the input vector is empty

    println!("The first doubled is {:?}", double_first(strings));
    // Error 2: the element doesn't parse to a number
}
```

There are times when we'll want to stop processing on errors (like with
[`?`][section-error-multiple_error_types-option_result-ref-1]) but keep going when the `Option` is `None`. The `transpose` function comes in handy to swap the `Result` and `Option`.

```rust
use std::num::ParseIntError;

fn double_first(vec: Vec<&str>) -> Result<Option<i32>, ParseIntError> {
    let opt = vec.first().map(|first| {
        first.parse::<i32>().map(|n| 2 * n)
    });

    opt.transpose()
}

fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    println!("The first doubled is {:?}", double_first(numbers));
    println!("The first doubled is {:?}", double_first(empty));
    println!("The first doubled is {:?}", double_first(strings));
}
```

[section-error-multiple_error_types-option_result-ref-1]: #section-error-result-enter_question_mark

<a id="section-error-multiple_error_types-define_error_type"></a>

<a id="section-error-multiple_error_types-define_error_type--defining-an-error-type"></a>

### Defining an error type

Sometimes it simplifies the code to mask all of the different errors with a
single type of error.  We'll show this with a custom error.

Rust allows us to define our own error types. In general, a "good" error type:

* Represents different errors with the same type
* Presents nice error messages to the user
* Is easy to compare with other types
  * Good: `Err(EmptyVec)`
  * Bad: `Err("Please use a vector with at least one element".to_owned())`
* Can hold information about the error
  * Good: `Err(BadChar(c, position))`
  * Bad: `Err("+ cannot be used here".to_owned())`
* Composes well with other errors

```rust
use std::fmt;

type Result<T> = std::result::Result<T, DoubleError>;

// Define our error types. These may be customized for our error handling cases.
// Now we will be able to write our own errors, defer to an underlying error
// implementation, or do something in between.
#[derive(Debug, Clone)]
struct DoubleError;

// Generation of an error is completely separate from how it is displayed.
// There's no need to be concerned about cluttering complex logic with the display style.
//
// Note that we don't store any extra info about the errors. This means we can't state
// which string failed to parse without modifying our types to carry that information.
impl fmt::Display for DoubleError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid first item to double")
    }
}

fn double_first(vec: Vec<&str>) -> Result<i32> {
    vec.first()
        // Change the error to our new type.
        .ok_or(DoubleError)
        .and_then(|s| {
            s.parse::<i32>()
                // Update to the new error type here also.
                .map_err(|_| DoubleError)
                .map(|i| 2 * i)
        })
}

fn print(result: Result<i32>) {
    match result {
        Ok(n) => println!("The first doubled is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    print(double_first(numbers));
    print(double_first(empty));
    print(double_first(strings));
}
```

<a id="section-error-multiple_error_types-boxing_errors"></a>

<a id="section-error-multiple_error_types-boxing_errors--boxing-errors"></a>

### `Box`ing errors

A way to write simple code while preserving the original errors is to [`Box`][section-error-multiple_error_types-boxing_errors-ref-1]
them.  The drawback is that the underlying error type is only known at runtime and not
[statically determined][section-error-multiple_error_types-boxing_errors-ref-2].

The stdlib helps in boxing our errors by having `Box` implement conversion from
any type that implements the `Error` trait into the trait object `Box<Error>`,
via [`From`][section-error-multiple_error_types-boxing_errors-ref-4].

```rust
use std::error;
use std::fmt;

// Change the alias to use `Box<dyn error::Error>`.
type Result<T> = std::result::Result<T, Box<dyn error::Error>>;

#[derive(Debug, Clone)]
struct EmptyVec;

impl fmt::Display for EmptyVec {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid first item to double")
    }
}

impl error::Error for EmptyVec {}

fn double_first(vec: Vec<&str>) -> Result<i32> {
    vec.first()
        .ok_or_else(|| EmptyVec.into()) // Converts to Box using Into trait.
        .and_then(|s| {
            s.parse::<i32>()
                .map_err(From::from) // Converts to Box using From::from fn pointer.
                .map(|i| 2 * i)
        })
}

fn print(result: Result<i32>) {
    match result {
        Ok(n) => println!("The first doubled is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    print(double_first(numbers));
    print(double_first(empty));
    print(double_first(strings));
}
```

<a id="section-error-multiple_error_types-boxing_errors--see-also"></a>

##### See also:

[Dynamic dispatch][section-error-multiple_error_types-boxing_errors-ref-2] and [`Error` trait][section-error-multiple_error_types-boxing_errors-ref-3]

[section-error-multiple_error_types-boxing_errors-ref-1]: https://doc.rust-lang.org/std/boxed/struct.Box.html
[section-error-multiple_error_types-boxing_errors-ref-2]: https://doc.rust-lang.org/book/ch17-02-trait-objects.html#trait-objects-perform-dynamic-dispatch
[section-error-multiple_error_types-boxing_errors-ref-3]: https://doc.rust-lang.org/std/error/trait.Error.html
[section-error-multiple_error_types-boxing_errors-ref-4]: https://doc.rust-lang.org/std/convert/trait.From.html

<a id="section-error-multiple_error_types-reenter_question_mark"></a>

<a id="section-error-multiple_error_types-reenter_question_mark--other-uses-of-"></a>

### Other uses of `?`

Notice in the previous example that our immediate reaction to calling
`parse` is to `map` the error from a library error into a boxed
error:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
.and_then(|s| s.parse::<i32>())
    .map_err(|e| e.into())
```

Since this is a simple and common operation, it would be convenient if it
could be elided. Alas, because `and_then` is not sufficiently flexible, it
cannot. However, we can instead use `?`.

`?` was previously explained as either `unwrap` or `return Err(err)`.
This is only mostly true. It actually means `unwrap` or
`return Err(From::from(err))`. Since `From::from` is a conversion utility
between different types, this means that if you `?` where the error is
convertible to the return type, it will convert automatically.

Here, we rewrite the previous example using `?`. As a result, the
`map_err` will go away when `From::from` is implemented for our error type:

```rust
use std::error;
use std::fmt;

// Change the alias to use `Box<dyn error::Error>`.
type Result<T> = std::result::Result<T, Box<dyn error::Error>>;

#[derive(Debug)]
struct EmptyVec;

impl fmt::Display for EmptyVec {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "invalid first item to double")
    }
}

impl error::Error for EmptyVec {}

// The same structure as before but rather than chain all `Results`
// and `Options` along, we `?` to get the inner value out immediately.
fn double_first(vec: Vec<&str>) -> Result<i32> {
    let first = vec.first().ok_or(EmptyVec)?;
    let parsed = first.parse::<i32>()?;
    Ok(2 * parsed)
}

fn print(result: Result<i32>) {
    match result {
        Ok(n)  => println!("The first doubled is {}", n),
        Err(e) => println!("Error: {}", e),
    }
}

fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    print(double_first(numbers));
    print(double_first(empty));
    print(double_first(strings));
}
```

This is actually fairly clean now. Compared with the original `panic`, it
is very similar to replacing the `unwrap` calls with `?` except that the
return types are `Result`. As a result, they must be destructured at the
top level.

<a id="section-error-multiple_error_types-reenter_question_mark--see-also"></a>

##### See also:

[`From::from`][section-error-multiple_error_types-reenter_question_mark-ref-1] and [`?`][section-error-multiple_error_types-reenter_question_mark-ref-2]

[section-error-multiple_error_types-reenter_question_mark-ref-1]: https://doc.rust-lang.org/std/convert/trait.From.html
[section-error-multiple_error_types-reenter_question_mark-ref-2]: https://doc.rust-lang.org/reference/expressions/operator-expr.html#the-question-mark-operator

<a id="section-error-multiple_error_types-wrap_error"></a>

<a id="section-error-multiple_error_types-wrap_error--wrapping-errors"></a>

### Wrapping errors

An alternative to boxing errors is to wrap them in your own error type.

```rust
use std::error;
use std::error::Error;
use std::num::ParseIntError;
use std::fmt;

type Result<T> = std::result::Result<T, DoubleError>;

#[derive(Debug)]
enum DoubleError {
    EmptyVec,
    // We will defer to the parse error implementation for their error.
    // Supplying extra info requires adding more data to the type.
    Parse(ParseIntError),
}

impl fmt::Display for DoubleError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            DoubleError::EmptyVec =>
                write!(f, "please use a vector with at least one element"),
            // The wrapped error contains additional information and is available
            // via the source() method.
            DoubleError::Parse(..) =>
                write!(f, "the provided string could not be parsed as int"),
        }
    }
}

impl error::Error for DoubleError {
    fn source(&self) -> Option<&(dyn error::Error + 'static)> {
        match *self {
            DoubleError::EmptyVec => None,
            // The cause is the underlying implementation error type. Is implicitly
            // cast to the trait object `&error::Error`. This works because the
            // underlying type already implements the `Error` trait.
            DoubleError::Parse(ref e) => Some(e),
        }
    }
}

// Implement the conversion from `ParseIntError` to `DoubleError`.
// This will be automatically called by `?` if a `ParseIntError`
// needs to be converted into a `DoubleError`.
impl From<ParseIntError> for DoubleError {
    fn from(err: ParseIntError) -> DoubleError {
        DoubleError::Parse(err)
    }
}

fn double_first(vec: Vec<&str>) -> Result<i32> {
    let first = vec.first().ok_or(DoubleError::EmptyVec)?;
    // Here we implicitly use the `ParseIntError` implementation of `From` (which
    // we defined above) in order to create a `DoubleError`.
    let parsed = first.parse::<i32>()?;

    Ok(2 * parsed)
}

fn print(result: Result<i32>) {
    match result {
        Ok(n)  => println!("The first doubled is {}", n),
        Err(e) => {
            println!("Error: {}", e);
            if let Some(source) = e.source() {
                println!("  Caused by: {}", source);
            }
        },
    }
}

fn main() {
    let numbers = vec!["42", "93", "18"];
    let empty = vec![];
    let strings = vec!["tofu", "93", "18"];

    print(double_first(numbers));
    print(double_first(empty));
    print(double_first(strings));
}
```

This adds a bit more boilerplate for handling errors and might not be needed in
all applications. There are some libraries that can take care of the boilerplate
for you.

<a id="section-error-multiple_error_types-wrap_error--see-also"></a>

##### See also:

[`From::from`][section-error-multiple_error_types-wrap_error-ref-1] and [`Enums`][section-error-multiple_error_types-wrap_error-ref-2]

[`Crates for handling errors`][section-error-multiple_error_types-wrap_error-ref-3]

[section-error-multiple_error_types-wrap_error-ref-1]: https://doc.rust-lang.org/std/convert/trait.From.html
[section-error-multiple_error_types-wrap_error-ref-2]: 03-custom-types.md#section-custom_types-enum
[section-error-multiple_error_types-wrap_error-ref-3]: https://crates.io/keywords/error-handling

<a id="section-error-iter_result"></a>

<a id="section-error-iter_result--iterating-over-results"></a>

## Iterating over `Result`s

An `Iter::map` operation might fail, for example:

```rust
fn main() {
    let strings = vec!["tofu", "93", "18"];
    let numbers: Vec<_> = strings
        .into_iter()
        .map(|s| s.parse::<i32>())
        .collect();
    println!("Results: {:?}", numbers);
}
```

Let's step through strategies for handling this.

<a id="section-error-iter_result--ignore-the-failed-items-with-filter_map"></a>

### Ignore the failed items with `filter_map()`

`filter_map` calls a function and filters out the results that are `None`.

```rust
fn main() {
    let strings = vec!["tofu", "93", "18"];
    let numbers: Vec<_> = strings
        .into_iter()
        .filter_map(|s| s.parse::<i32>().ok())
        .collect();
    println!("Results: {:?}", numbers);
}
```

<a id="section-error-iter_result--collect-the-failed-items-with-map_err-and-filter_map"></a>

### Collect the failed items with `map_err()` and `filter_map()`

`map_err` calls a function with the error, so by adding that to the previous
`filter_map` solution we can save them off to the side while iterating.

```rust
fn main() {
    let strings = vec!["42", "tofu", "93", "999", "18"];
    let mut errors = vec![];
    let numbers: Vec<_> = strings
        .into_iter()
        .map(|s| s.parse::<u8>())
        .filter_map(|r| r.map_err(|e| errors.push(e)).ok())
        .collect();
    println!("Numbers: {:?}", numbers);
    println!("Errors: {:?}", errors);
}
```

<a id="section-error-iter_result--fail-the-entire-operation-with-collect"></a>

### Fail the entire operation with `collect()`

`Result` implements `FromIterator` so that a vector of results (`Vec<Result<T, E>>`)
can be turned into a result with a vector (`Result<Vec<T>, E>`). Once an
`Result::Err` is found, the iteration will terminate.

```rust
fn main() {
    let strings = vec!["tofu", "93", "18"];
    let numbers: Result<Vec<_>, _> = strings
        .into_iter()
        .map(|s| s.parse::<i32>())
        .collect();
    println!("Results: {:?}", numbers);
}
```

This same technique can be used with `Option`.

<a id="section-error-iter_result--collect-all-valid-values-and-failures-with-partition"></a>

### Collect all valid values and failures with `partition()`

```rust
fn main() {
    let strings = vec!["tofu", "93", "18"];
    let (numbers, errors): (Vec<_>, Vec<_>) = strings
        .into_iter()
        .map(|s| s.parse::<i32>())
        .partition(Result::is_ok);
    println!("Numbers: {:?}", numbers);
    println!("Errors: {:?}", errors);
}
```

When you look at the results, you'll note that everything is still wrapped in
`Result`.  A little more boilerplate is needed for this.

```rust
fn main() {
    let strings = vec!["tofu", "93", "18"];
    let (numbers, errors): (Vec<_>, Vec<_>) = strings
        .into_iter()
        .map(|s| s.parse::<i32>())
        .partition(Result::is_ok);
    let numbers: Vec<_> = numbers.into_iter().map(Result::unwrap).collect();
    let errors: Vec<_> = errors.into_iter().map(Result::unwrap_err).collect();
    println!("Numbers: {:?}", numbers);
    println!("Errors: {:?}", errors);
}
```
