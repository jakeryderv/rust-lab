<a id="section-crates"></a>

<a id="section-crates--crates"></a>

# Crates

[Chapter index](SUMMARY.md)

**In this chapter**

- [Creating a Library](#section-crates-lib)
- [Using a Library](#section-crates-using_lib)


A crate is a compilation unit in Rust. Whenever `rustc some_file.rs` is called,
`some_file.rs` is treated as the *crate file*. If `some_file.rs` has `mod`
declarations in it, then the contents of the module files would be inserted in
places where `mod` declarations in the crate file are found, *before* running
the compiler over it. In other words, modules do *not* get compiled
individually, only crates get compiled.

A crate can be compiled into a binary or into a library. By default, `rustc`
will produce a binary from a crate. This behavior can be overridden by passing
the `--crate-type` flag to `lib`.

<a id="section-crates-lib"></a>

<a id="section-crates-lib--creating-a-library"></a>

## Creating a Library

Let's create a library, and then see how to link it to another crate.

In `rary.rs`:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
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

```shell
$ rustc --crate-type=lib rary.rs
$ ls lib*
library.rlib
```

Libraries get prefixed with "lib", and by default they get named after their
crate file, but this default name can be overridden by passing
the `--crate-name` option to `rustc` or by using the [`crate_name`
attribute][section-crates-lib-ref-1].

[section-crates-lib-ref-1]: 13-attributes.md#section-attribute-crate

<a id="section-crates-using_lib"></a>

<a id="section-crates-using_lib--using-a-library"></a>

## Using a Library

To link a crate to this new library you may use `rustc`'s `--extern` flag. All
of its items will then be imported under a module named the same as the library.
This module generally behaves the same way as any other module.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// extern crate rary; // May be required for Rust 2015 edition or earlier

fn main() {
    rary::public_function();

    // Error! `private_function` is private
    //rary::private_function();

    rary::indirect_access();
}
```

```txt
# Where library.rlib is the path to the compiled library, assumed that it's
# in the same directory here:
$ rustc executable.rs --extern rary=library.rlib && ./executable
called rary's `public_function()`
called rary's `indirect_access()`, that
> called rary's `private_function()`
```
