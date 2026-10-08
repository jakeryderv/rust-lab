<a id="section-cargo"></a>

<a id="section-cargo--cargo"></a>

# Cargo

[Chapter index](SUMMARY.md)

**In this chapter**

- [Dependencies](#section-cargo-deps)
- [Conventions](#section-cargo-conventions)
- [Tests](#section-cargo-test)
- [Build Scripts](#section-cargo-build_scripts)


`cargo` is the official Rust package management tool. It has lots of really
useful features to improve code quality and developer velocity! These include

- Dependency management and integration with [crates.io](https://crates.io) (the
  official Rust package registry)
- Awareness of unit tests
- Awareness of benchmarks

This chapter will go through some quick basics, but you can find the
comprehensive docs in [The Cargo Book](https://doc.rust-lang.org/cargo/).

<a id="section-cargo-deps"></a>

<a id="section-cargo-deps--dependencies"></a>

## Dependencies

Most programs have dependencies on some libraries. If you have ever managed
dependencies by hand, you know how much of a pain this can be. Luckily, the Rust
ecosystem comes standard with `cargo`! `cargo` can manage dependencies for a
project.

To create a new Rust project,

```sh
# A binary
cargo new foo

# A library
cargo new --lib bar
```

For the rest of this chapter, let's assume we are making a binary, rather than
a library, but all of the concepts are the same.

After the above commands, you should see a file hierarchy like this:

```txt
.
├── bar
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
└── foo
    ├── Cargo.toml
    └── src
        └── main.rs
```

The `main.rs` is the root source file for your new `foo` project -- nothing new there.
The `Cargo.toml` is the config file for `cargo` for this project. If you
look inside it, you should see something like this:

```toml
[package]
name = "foo"
version = "0.1.0"
authors = ["mark"]

[dependencies]
```

The `name` field under `[package]` determines the name of the project. This is
used by `crates.io` if you publish the crate (more later). It is also the name
of the output binary when you compile.

The `version` field is a crate version number using [Semantic
Versioning](http://semver.org/).

The `authors` field is a list of authors used when publishing the crate.

The `[dependencies]` section lets you add dependencies for your project.

For example, suppose that we want our program to have a great CLI. You can find
lots of great packages on [crates.io](https://crates.io) (the official Rust
package registry). One popular choice is [clap](https://crates.io/crates/clap).
As of this writing, the most recent published version of `clap` is `2.27.1`. To
add a dependency to our program, we can simply add the following to our
`Cargo.toml` under `[dependencies]`: `clap = "2.27.1"`. And that's it! You can start using
`clap` in your program.

`cargo` also supports [other types of dependencies][section-cargo-deps-ref-2]. Here is just
a small sampling:

```toml
[package]
name = "foo"
version = "0.1.0"
authors = ["mark"]

[dependencies]
clap = "2.27.1" # from crates.io
rand = { git = "https://github.com/rust-lang-nursery/rand" } # from online repo
bar = { path = "../bar" } # from a path in the local filesystem
```

`cargo` is more than a dependency manager. All of the available
configuration options are listed in the [format specification][section-cargo-deps-ref-1] of
`Cargo.toml`.

To build our project we can execute `cargo build` anywhere in the project
directory (including subdirectories!). We can also do `cargo run` to build and
run. Notice that these commands will resolve all dependencies, download crates
if needed, and build everything, including your crate. (Note that it only
rebuilds what it has not already built, similar to `make`).

Voila! That's all there is to it!

[section-cargo-deps-ref-1]: https://doc.rust-lang.org/cargo/reference/manifest.html
[section-cargo-deps-ref-2]: https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html

<a id="section-cargo-conventions"></a>

<a id="section-cargo-conventions--conventions"></a>

## Conventions

In the previous chapter, we saw the following directory hierarchy:

```txt
foo
├── Cargo.toml
└── src
    └── main.rs
```

Suppose that we wanted to have two binaries in the same project, though. What
then?

It turns out that `cargo` supports this. The default binary name is `main`, as
we saw before, but you can add additional binaries by placing them in a `bin/`
directory:

```txt
foo
├── Cargo.toml
└── src
    ├── main.rs
    └── bin
        └── my_other_bin.rs
```

To tell `cargo` to only compile or run this binary, we just pass `cargo` the
`--bin my_other_bin` flag, where `my_other_bin` is the name of the binary we
want to work with.

In addition to extra binaries, `cargo` supports [more features][section-cargo-conventions-ref-1] such as
benchmarks, tests, and examples.

In the next chapter, we will look more closely at tests.

[section-cargo-conventions-ref-1]: https://doc.rust-lang.org/cargo/guide/project-layout.html

<a id="section-cargo-test"></a>

<a id="section-cargo-test--testing"></a>

## Testing

As we know testing is integral to any piece of software! Rust has first-class
support for unit and integration testing ([see this
chapter](https://doc.rust-lang.org/book/ch11-00-testing.html) in TRPL).

From the testing chapters linked above, we see how to write unit tests and
integration tests. Organizationally, we can place unit tests in the modules they
test and integration tests in their own `tests/` directory:

```txt
foo
├── Cargo.toml
├── src
│   └── main.rs
│   └── lib.rs
└── tests
    ├── my_test.rs
    └── my_other_test.rs
```

Each file in `tests` is a separate
[integration test](https://doc.rust-lang.org/book/ch11-03-test-organization.html#integration-tests),
i.e. a test that is meant to test your library as if it were being called from a dependent
crate.

The [Testing][section-cargo-test-ref-1] chapter elaborates on the three different testing styles:
[Unit][section-cargo-test-ref-2], [Doc][section-cargo-test-ref-4], and [Integration][section-cargo-test-ref-3].

`cargo` naturally provides an easy way to run all of your tests!

```shell
$ cargo test
```

You should see output like this:

```shell
$ cargo test
   Compiling blah v0.1.0 (file:///nobackup/blah)
    Finished dev [unoptimized + debuginfo] target(s) in 0.89 secs
     Running target/debug/deps/blah-d3b32b97275ec472

running 4 tests
test test_bar ... ok
test test_baz ... ok
test test_foo_bar ... ok
test test_foo ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

You can also run tests whose name matches a pattern:

```shell
$ cargo test test_foo
```

```shell
$ cargo test test_foo
   Compiling blah v0.1.0 (file:///nobackup/blah)
    Finished dev [unoptimized + debuginfo] target(s) in 0.35 secs
     Running target/debug/deps/blah-d3b32b97275ec472

running 2 tests
test test_foo ... ok
test test_foo_bar ... ok

test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 2 filtered out
```

One word of caution: Cargo may run multiple tests concurrently, so make sure
that they don't race with each other.

One example of this concurrency causing issues is if two tests output to a
file, such as below:

```rust
#[cfg(test)]
mod tests {
    // Import the necessary modules
    use std::fs::OpenOptions;
    use std::io::Write;

    // This test writes to a file
    #[test]
    fn test_file() {
        // Opens the file ferris.txt or creates one if it doesn't exist.
        let mut file = OpenOptions::new()
            .append(true)
            .create(true)
            .open("ferris.txt")
            .expect("Failed to open ferris.txt");

        // Print "Ferris" 5 times.
        for _ in 0..5 {
            file.write_all("Ferris\n".as_bytes())
                .expect("Could not write to ferris.txt");
        }
    }

    // This test tries to write to the same file
    #[test]
    fn test_file_also() {
        // Opens the file ferris.txt or creates one if it doesn't exist.
        let mut file = OpenOptions::new()
            .append(true)
            .create(true)
            .open("ferris.txt")
            .expect("Failed to open ferris.txt");

        // Print "Corro" 5 times.
        for _ in 0..5 {
            file.write_all("Corro\n".as_bytes())
                .expect("Could not write to ferris.txt");
        }
    }
}
```

Although the intent is to get the following:

```shell
$ cat ferris.txt
Ferris
Ferris
Ferris
Ferris
Ferris
Corro
Corro
Corro
Corro
Corro
```

What actually gets put into `ferris.txt` is this:

```shell
$ cargo test test_file && cat ferris.txt
Corro
Ferris
Corro
Ferris
Corro
Ferris
Corro
Ferris
Corro
Ferris
```

[section-cargo-test-ref-1]: 21-testing.md
[section-cargo-test-ref-2]: 21-testing.md#section-testing-unit_testing
[section-cargo-test-ref-3]: 21-testing.md#section-testing-integration_testing
[section-cargo-test-ref-4]: 21-testing.md#section-testing-doc_testing

<a id="section-cargo-build_scripts"></a>

<a id="section-cargo-build_scripts--build-scripts"></a>

## Build Scripts

Sometimes a normal build from `cargo` is not enough. Perhaps your crate needs
some pre-requisites before `cargo` will successfully compile, things like code
generation, or some native code that needs to be compiled. To solve this problem
we have build scripts that Cargo can run.

To add a build script to your package it can either be specified in the
`Cargo.toml` as follows:

```toml
[package]
...
build = "build.rs"
```

Otherwise Cargo will look for a `build.rs` file in the project directory by
default.

<a id="section-cargo-build_scripts--how-to-use-a-build-script"></a>

### How to use a build script

The build script is simply another Rust file that will be compiled and invoked
prior to compiling anything else in the package. Hence it can be used to fulfill
pre-requisites of your crate.

Cargo provides the script with inputs via environment variables [specified
here][section-cargo-build_scripts-ref-1] that can be used.

The script provides output via stdout. All lines printed are written to
`target/debug/build/<pkg>/output`. Further, lines prefixed with `cargo:` will be
interpreted by Cargo directly and hence can be used to define parameters for the
package's compilation.

For further specification and examples have a read of the
[Cargo specification][section-cargo-build_scripts-ref-2].

[section-cargo-build_scripts-ref-1]: https://doc.rust-lang.org/cargo/reference/environment-variables.html#environment-variables-cargo-sets-for-build-scripts

[section-cargo-build_scripts-ref-2]: https://doc.rust-lang.org/cargo/reference/build-scripts.html
