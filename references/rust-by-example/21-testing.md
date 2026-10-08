<a id="section-testing"></a>

<a id="section-testing--testing"></a>

# Testing

[Chapter index](SUMMARY.md)

**In this chapter**

- [Unit testing](#section-testing-unit_testing)
- [Documentation testing](#section-testing-doc_testing)
- [Integration testing](#section-testing-integration_testing)
- [Dev-dependencies](#section-testing-dev_dependencies)


Rust is a programming language that cares a lot about correctness and it
includes support for writing software tests within the language itself.

Testing comes in three styles:

* [Unit][section-testing-ref-1] testing.
* [Doc][section-testing-ref-2] testing.
* [Integration][section-testing-ref-3] testing.

Also Rust has support for specifying additional dependencies for tests:

* [Dev-dependencies][section-testing-ref-4]

<a id="section-testing--see-also"></a>

## See Also

* [The Book][section-testing-ref-5] chapter on testing
* [API Guidelines][section-testing-ref-6] on doc-testing

[section-testing-ref-1]: #section-testing-unit_testing
[section-testing-ref-2]: #section-testing-doc_testing
[section-testing-ref-3]: #section-testing-integration_testing
[section-testing-ref-4]: #section-testing-dev_dependencies
[section-testing-ref-5]: https://doc.rust-lang.org/book/ch11-00-testing.html
[section-testing-ref-6]: https://rust-lang-nursery.github.io/api-guidelines/documentation.html

<a id="section-testing-unit_testing"></a>

<a id="section-testing-unit_testing--unit-testing"></a>

## Unit testing

Tests are Rust functions that verify that the non-test code is functioning in
the expected manner. The bodies of test functions typically perform some setup,
run the code we want to test, then assert whether the results are what we
expect.

Most unit tests go into a `tests` [mod][section-testing-unit_testing-ref-4] with the `#[cfg(test)]` [attribute][section-testing-unit_testing-ref-1].
Test functions are marked with the `#[test]` attribute.

Tests fail when something in the test function [panics][section-testing-unit_testing-ref-2]. There are some
helper [macros][section-testing-unit_testing-ref-3]:

* `assert!(expression)` - panics if expression evaluates to `false`.
* `assert_eq!(left, right)` and `assert_ne!(left, right)` - testing left and
  right expressions for equality and inequality respectively.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

// This is a really bad adding function, its purpose is to fail in this
// example.
#[allow(dead_code)]
fn bad_add(a: i32, b: i32) -> i32 {
    a - b
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(1, 2), 3);
    }

    #[test]
    fn test_bad_add() {
        // This assert would fire and test will fail.
        // Please note, that private functions can be tested too!
        assert_eq!(bad_add(1, 2), 3);
    }
}
```

Tests can be run with `cargo test`.

```shell
$ cargo test

running 2 tests
test tests::test_bad_add ... FAILED
test tests::test_add ... ok

failures:

---- tests::test_bad_add stdout ----
        thread 'tests::test_bad_add' panicked at 'assertion failed: `(left == right)`
  left: `-1`,
 right: `3`', src/lib.rs:21:8
note: Run with `RUST_BACKTRACE=1` for a backtrace.


failures:
    tests::test_bad_add

test result: FAILED. 1 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out
```

<a id="section-testing-unit_testing--tests-and-"></a>

### Tests and `?`

None of the previous unit test examples had a return type. But in Rust 2018,
your unit tests can return `Result<()>`, which lets you use `?` in them! This
can make them much more concise.

```rust
fn sqrt(number: f64) -> Result<f64, String> {
    if number >= 0.0 {
        Ok(number.powf(0.5))
    } else {
        Err("negative floats don't have square roots".to_owned())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sqrt() -> Result<(), String> {
        let x = 4.0;
        assert_eq!(sqrt(x)?.powf(2.0), x);
        Ok(())
    }
}
```

See ["The Edition Guide"][section-testing-unit_testing-ref-5] for more details.

<a id="section-testing-unit_testing--testing-panics"></a>

### Testing panics

To check functions that should panic under certain circumstances, use attribute
`#[should_panic]`. This attribute accepts optional parameter `expected = ` with
the text of the panic message. If your function can panic in multiple ways, it helps
make sure your test is testing the correct panic.

**Note**: Rust also allows a shorthand form `#[should_panic = "message"]`, which works
exactly like `#[should_panic(expected = "message")]`. Both are valid; the latter is more commonly
used and is considered more explicit.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
pub fn divide_non_zero_result(a: u32, b: u32) -> u32 {
    if b == 0 {
        panic!("Divide-by-zero error");
    } else if a < b {
        panic!("Divide result is zero");
    }
    a / b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_divide() {
        assert_eq!(divide_non_zero_result(10, 2), 5);
    }

    #[test]
    #[should_panic]
    fn test_any_panic() {
        divide_non_zero_result(1, 0);
    }

    #[test]
    #[should_panic(expected = "Divide result is zero")]
    fn test_specific_panic() {
        divide_non_zero_result(1, 10);
    }

    #[test]
    #[should_panic = "Divide result is zero"] // This also works
    fn test_specific_panic_shorthand() {
        divide_non_zero_result(1, 10);
    }
}
```

Running these tests gives us:

```shell
$ cargo test

running 4 tests
test tests::test_any_panic ... ok
test tests::test_divide ... ok
test tests::test_specific_panic ... ok
test tests::test_specific_panic_shorthand ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

   Doc-tests tmp-test-should-panic

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

<a id="section-testing-unit_testing--running-specific-tests"></a>

### Running specific tests

To run specific tests one may specify the test name to `cargo test` command.

```shell
$ cargo test test_any_panic
running 1 test
test tests::test_any_panic ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 3 filtered out

   Doc-tests tmp-test-should-panic

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

To run multiple tests one may specify part of a test name that matches all the
tests that should be run.

```shell
$ cargo test panic
running 3 tests
test tests::test_any_panic ... ok
test tests::test_specific_panic ... ok
test tests::test_specific_panic_shorthand ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 1 filtered out

   Doc-tests tmp-test-should-panic

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

<a id="section-testing-unit_testing--ignoring-tests"></a>

### Ignoring tests

Tests can be marked with the `#[ignore]` attribute to exclude some tests. Or to run
them with command `cargo test -- --ignored`

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 2), 4);
    }

    #[test]
    fn test_add_hundred() {
        assert_eq!(add(100, 2), 102);
        assert_eq!(add(2, 100), 102);
    }

    #[test]
    #[ignore]
    fn ignored_test() {
        assert_eq!(add(0, 0), 0);
    }
}
```

```shell
$ cargo test
running 3 tests
test tests::ignored_test ... ignored
test tests::test_add ... ok
test tests::test_add_hundred ... ok

test result: ok. 2 passed; 0 failed; 1 ignored; 0 measured; 0 filtered out

   Doc-tests tmp-ignore

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

$ cargo test -- --ignored
running 1 test
test tests::ignored_test ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

   Doc-tests tmp-ignore

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

[section-testing-unit_testing-ref-1]: 13-attributes.md
[section-testing-unit_testing-ref-2]: 19-std-library-types.md#section-std-panic
[section-testing-unit_testing-ref-3]: 17-macro_rules.md
[section-testing-unit_testing-ref-4]: 10-modules.md
[section-testing-unit_testing-ref-5]: https://doc.rust-lang.org/edition-guide/rust-2018/error-handling-and-panics/question-mark-in-main-and-tests.html

<a id="section-testing-doc_testing"></a>

<a id="section-testing-doc_testing--documentation-testing"></a>

## Documentation testing

The primary way of documenting a Rust project is through annotating the source
code. Documentation comments are written in
[CommonMark Markdown specification][section-testing-doc_testing-ref-2] and support code blocks in them.
Rust takes care about correctness, so these code blocks are compiled and used
as documentation tests.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
/// First line is a short summary describing function.
///
/// The next lines present detailed documentation. Code blocks start with
/// triple backquotes and have implicit `fn main()` inside
/// and `extern crate <cratename>`. Assume we're testing a `playground` library
/// crate or using the Playground's Test action:
///
/// ```
/// let result = playground::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// Usually doc comments may include sections "Examples", "Panics" and "Failures".
///
/// The next function divides two numbers.
///
/// # Examples
///
/// ```
/// let result = playground::div(10, 2);
/// assert_eq!(result, 5);
/// ```
///
/// # Panics
///
/// The function panics if the second argument is zero.
///
/// ```rust,should_panic
/// // panics on division by zero
/// playground::div(10, 0);
/// ```
pub fn div(a: i32, b: i32) -> i32 {
    if b == 0 {
        panic!("Divide-by-zero error");
    }

    a / b
}
```

Code blocks in documentation are automatically tested
when running the regular `cargo test` command:

```shell
$ cargo test
running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

   Doc-tests playground

running 3 tests
test src/lib.rs - add (line 7) ... ok
test src/lib.rs - div (line 21) ... ok
test src/lib.rs - div (line 31) ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

<a id="section-testing-doc_testing--motivation-behind-documentation-tests"></a>

### Motivation behind documentation tests

The main purpose of documentation tests is to serve as examples that exercise
the functionality, which is one of the most important
[guidelines][section-testing-doc_testing-ref-4]. It allows using examples from docs as
complete code snippets. But using `?` makes compilation fail since `main`
returns `unit`. The ability to hide some source lines from documentation comes
to the rescue: one may write `fn try_main() -> Result<(), ErrorType>`, hide it
and `unwrap` it in hidden `main`. Sounds complicated? Here's an example:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
/// Using hidden `try_main` in doc tests.
///
/// ```
/// # // hidden lines start with `#` symbol, but they're still compilable!
/// # fn try_main() -> Result<(), String> { // line that wraps the body shown in doc
/// let res = playground::try_div(10, 2)?;
/// # Ok(()) // returning from try_main
/// # }
/// # fn main() { // starting main that'll unwrap()
/// #    try_main().unwrap(); // calling try_main and unwrapping
/// #                         // so that test will panic in case of error
/// # }
/// ```
pub fn try_div(a: i32, b: i32) -> Result<i32, String> {
    if b == 0 {
        Err(String::from("Divide-by-zero"))
    } else {
        Ok(a / b)
    }
}
```

<a id="section-testing-doc_testing--see-also"></a>

### See Also

* [RFC505][section-testing-doc_testing-ref-3] on documentation style
* [API Guidelines][section-testing-doc_testing-ref-1] on documentation guidelines

[section-testing-doc_testing-ref-1]: https://rust-lang-nursery.github.io/api-guidelines/documentation.html
[section-testing-doc_testing-ref-2]: https://commonmark.org/
[section-testing-doc_testing-ref-3]: https://github.com/rust-lang/rfcs/blob/master/text/0505-api-comment-conventions.md
[section-testing-doc_testing-ref-4]: https://rust-lang-nursery.github.io/api-guidelines/documentation.html#examples-use--not-try-not-unwrap-c-question-mark

<a id="section-testing-integration_testing"></a>

<a id="section-testing-integration_testing--integration-testing"></a>

## Integration testing

[Unit tests][section-testing-integration_testing-ref-1] are testing one module in isolation at a time: they're small
and can test private code. Integration tests are external to your crate and use
only its public interface in the same way any other code would. Their purpose is
to test that many parts of your library work correctly together.

Cargo looks for integration tests in `tests` directory next to `src`.

File `src/lib.rs`:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Define this in a crate called `adder`.
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

File with test: `tests/integration_test.rs`:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
#[test]
fn test_add() {
    assert_eq!(adder::add(3, 2), 5);
}
```

Running tests with `cargo test` command:

```shell
$ cargo test
running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

     Running target/debug/deps/integration_test-bcd60824f5fbfe19

running 1 test
test test_add ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out

   Doc-tests adder

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

Each Rust source file in the `tests` directory is compiled as a separate crate. In
order to share some code between integration tests we can make a module with public
functions, importing and using it within tests.

File `tests/common/mod.rs`:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
pub fn setup() {
    // some setup code, like creating required files/directories, starting
    // servers, etc.
}
```

File with test: `tests/integration_test.rs`

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// importing common module.
mod common;

#[test]
fn test_add() {
    // using common code.
    common::setup();
    assert_eq!(adder::add(3, 2), 5);
}
```

Creating the module as `tests/common.rs` also works, but is not recommended
because the test runner will treat the file as a test crate and try to run tests
inside it.

[section-testing-integration_testing-ref-1]: #section-testing-unit_testing
[section-testing-integration_testing-ref-2]: 10-modules.md

<a id="section-testing-dev_dependencies"></a>

<a id="section-testing-dev_dependencies--development-dependencies"></a>

## Development dependencies

Sometimes there is a need to have dependencies for tests (or examples,
or benchmarks) only. Such dependencies are added to `Cargo.toml` in the
`[dev-dependencies]` section. These dependencies are not propagated to other
packages which depend on this package.

One such example is [`pretty_assertions`](https://docs.rs/pretty_assertions/1.0.0/pretty_assertions/index.html), which extends standard `assert_eq!` and `assert_ne!` macros, to provide colorful diff.
File `Cargo.toml`:

```toml
# standard crate data is left out
[dev-dependencies]
pretty_assertions = "1"
```

File `src/lib.rs`:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;
    use pretty_assertions::assert_eq; // crate for test-only use. Cannot be used in non-test code.

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
    }
}
```

<a id="section-testing-dev_dependencies--see-also"></a>

### See Also

[Cargo][section-testing-dev_dependencies-ref-1] docs on specifying dependencies.

[section-testing-dev_dependencies-ref-1]: http://doc.crates.io/specifying-dependencies.html
