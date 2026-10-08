<a id="section-attribute"></a>

<a id="section-attribute--attributes"></a>

# Attributes

[Chapter index](SUMMARY.md)

**In this chapter**

- [`dead_code`](#section-attribute-unused)
- [Crates](#section-attribute-crate)
- [`cfg`](#section-attribute-cfg)
  - [Custom](#section-attribute-cfg-custom)


An attribute is metadata applied to some module, crate or item. This metadata
can be used to/for:

<!-- TODO: Link these to their respective examples -->

* [conditional compilation of code][section-attribute-ref-1]
* [set crate name, version and type (binary or library)][section-attribute-ref-2]
* disable [lints][section-attribute-ref-4] (warnings)
* enable compiler features (macros, glob imports, etc.)
* link to a foreign library
* mark functions as unit tests
* mark functions that will be part of a benchmark
* [attribute like macros][section-attribute-ref-5]

Attributes look like `#[outer_attribute]` or `#![inner_attribute]`,
with the difference between them being where they apply.

* `#[outer_attribute]` applies to the [item][section-attribute-ref-3] immediately
  following it. Some examples of items are: a function, a module
  declaration, a constant, a structure, an enum. Here is an example
  where attribute `#[derive(Debug)]` applies to the struct
  `Rectangle`:

  ```rust
  #[derive(Debug)]
  struct Rectangle {
      width: u32,
      height: u32,
  }
  ```

* `#![inner_attribute]` applies to the enclosing [item][section-attribute-ref-3] (typically a
  module or a crate). In other words, this attribute is interpreted as
  applying to the entire scope in which it's placed. Here is an example
  where `#![allow(unused_variables)]` applies to the whole crate (if
  placed in `main.rs`):

  ```rust
  #![allow(unused_variables)]

  fn main() {
      let x = 3; // This would normally warn about an unused variable.
  }
  ```

Attributes can take arguments with different syntaxes:

* `#[attribute = "value"]`
* `#[attribute(key = "value")]`
* `#[attribute(value)]`

Attributes can have multiple values and can be separated over multiple lines, too:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
#[attribute(value, value2)]


#[attribute(value, value2, value3,
            value4, value5)]
```

[section-attribute-ref-1]: #section-attribute-cfg
[section-attribute-ref-2]: #section-attribute-crate
[section-attribute-ref-3]: https://doc.rust-lang.org/stable/reference/items.html
[section-attribute-ref-4]: https://en.wikipedia.org/wiki/Lint_%28software%29
[section-attribute-ref-5]: https://doc.rust-lang.org/book/ch19-06-macros.html#attribute-like-macros

<a id="section-attribute-unused"></a>

<a id="section-attribute-unused--dead_code"></a>

## `dead_code`

The compiler provides a `dead_code`
[*lint*][section-attribute-unused-ref-1] that will warn
about unused functions. An *attribute* can be used to disable the lint.

```rust
fn used_function() {}

// `#[allow(dead_code)]` is an attribute that disables the `dead_code` lint
#[allow(dead_code)]
fn unused_function() {}

fn noisy_unused_function() {}
// FIXME ^ Add an attribute to suppress the warning

fn main() {
    used_function();
}
```

Note that in real programs, you should eliminate dead code. In these examples
we'll allow dead code in some places because of the interactive nature of the
examples.

[section-attribute-unused-ref-1]: https://en.wikipedia.org/wiki/Lint_%28software%29

<a id="section-attribute-crate"></a>

<a id="section-attribute-crate--crates"></a>

## Crates

The `crate_type` attribute can be used to tell the compiler whether a crate is
a binary or a library (and even which type of library), and the `crate_name`
attribute can be used to set the name of the crate.

However, it is important to note that both the `crate_type` and `crate_name`
attributes have **no** effect whatsoever when using Cargo, the Rust package
manager. Since Cargo is used for the majority of Rust projects, this means
real-world uses of `crate_type` and `crate_name` are relatively limited.

```rust
// This crate is a library
#![crate_type = "lib"]
// The library is named "rary"
#![crate_name = "rary"]

pub fn public_function() {
    println!("called rary's `public_function()`");
}

fn private_function() {
    println!("called rary's `private_function()`");
}

pub fn indirect_access() {
    print!("called rary's `indirect_access()`, that\n> ");

    private_function();
}
```

When the `crate_type` attribute is used, we no longer need to pass the
`--crate-type` flag to `rustc`.

```shell
$ rustc lib.rs
$ ls lib*
library.rlib
```

<a id="section-attribute-cfg"></a>

<a id="section-attribute-cfg--cfg"></a>

## `cfg`

Configuration conditional checks are possible through two different operators:

* the `cfg` attribute: `#[cfg(...)]` in attribute position
* the `cfg!` macro: `cfg!(...)` in boolean expressions

While the former enables conditional compilation, the latter conditionally
evaluates to `true` or `false` literals allowing for checks at run-time. Both
utilize identical argument syntax.

`cfg!`, unlike `#[cfg]`, does not remove any code and only evaluates to true or false. For example, all blocks in an if/else expression need to be valid when `cfg!` is used for the condition, regardless of what `cfg!` is evaluating.

```rust
// This function only gets compiled if the target OS is linux
#[cfg(target_os = "linux")]
fn are_you_on_linux() {
    println!("You are running linux!");
}

// And this function only gets compiled if the target OS is *not* linux
#[cfg(not(target_os = "linux"))]
fn are_you_on_linux() {
    println!("You are *not* running linux!");
}

fn main() {
    are_you_on_linux();

    println!("Are you sure?");
    if cfg!(target_os = "linux") {
        println!("Yes. It's definitely linux!");
    } else {
        println!("Yes. It's definitely *not* linux!");
    }
}
```

<a id="section-attribute-cfg--see-also"></a>

#### See also:

[the reference][section-attribute-cfg-ref-3], [`cfg!`][section-attribute-cfg-ref-1], and [macros][section-attribute-cfg-ref-2].

[section-attribute-cfg-ref-1]: https://doc.rust-lang.org/std/macro.cfg!.html
[section-attribute-cfg-ref-2]: 17-macro_rules.md
[section-attribute-cfg-ref-3]: https://doc.rust-lang.org/reference/attributes.html#conditional-compilation

<a id="section-attribute-cfg-custom"></a>

<a id="section-attribute-cfg-custom--custom"></a>

### Custom

Some conditionals like `target_os` are implicitly provided by `rustc`, but
custom conditionals must be passed to `rustc` using the `--cfg` flag.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
#[cfg(some_condition)]
fn conditional_function() {
    println!("condition met!");
}

fn main() {
    conditional_function();
}
```

Try to run this to see what happens without the custom `cfg` flag.

With the custom `cfg` flag:

```shell
$ rustc --cfg some_condition custom.rs && ./custom
condition met!
```
