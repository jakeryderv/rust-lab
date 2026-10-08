<a id="section-appendix-04-useful-development-tools"></a>

<a id="section-appendix-04-useful-development-tools--appendix-d-useful-development-tools"></a>

# Appendix D: Useful Development Tools

[Chapter index](../SUMMARY.md)

**In this chapter**

- [Automatic Formatting with `rustfmt`](#section-appendix-04-useful-development-tools--automatic-formatting-with-rustfmt)
- [Fix Your Code with `rustfix`](#section-appendix-04-useful-development-tools--fix-your-code-with-rustfix)
- [More Lints with Clippy](#section-appendix-04-useful-development-tools--more-lints-with-clippy)
- [IDE Integration Using `rust-analyzer`](#section-appendix-04-useful-development-tools--ide-integration-using-rust-analyzer)


In this appendix, we talk about some useful development tools that the Rust
project provides. We’ll look at automatic formatting, quick ways to apply
warning fixes, a linter, and integrating with IDEs.

<a id="section-appendix-04-useful-development-tools--automatic-formatting-with-rustfmt"></a>

## Automatic Formatting with `rustfmt`

The `rustfmt` tool reformats your code according to the community code style.
Many collaborative projects use `rustfmt` to prevent arguments about which
style to use when writing Rust: Everyone formats their code using the tool.

Rust installations include `rustfmt` by default, so you should already have the
programs `rustfmt` and `cargo-fmt` on your system. These two commands are
analogous to `rustc` and `cargo` in that `rustfmt` allows finer grained control
and `cargo-fmt` understands conventions of a project that uses Cargo. To format
any Cargo project, enter the following:

```console
$ cargo fmt
```

Running this command reformats all the Rust code in the current crate. This
should only change the code style, not the code semantics. For more information
on `rustfmt`, see [its documentation][section-appendix-04-useful-development-tools-ref-1].

<a id="section-appendix-04-useful-development-tools--fix-your-code-with-rustfix"></a>

## Fix Your Code with `rustfix`

The `rustfix` tool is included with Rust installations and can automatically
fix compiler warnings that have a clear way to correct the problem that’s
likely what you want. You’ve probably seen compiler warnings before. For
example, consider this code:

Filename: src/main.rs

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Here, we’re defining the variable `x` as mutable, but we never actually mutate
it. Rust warns us about that:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

The warning suggests that we remove the `mut` keyword. We can automatically
apply that suggestion using the `rustfix` tool by running the command `cargo
fix`:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

When we look at _src/main.rs_ again, we’ll see that `cargo fix` has changed the
code:

Filename: src/main.rs

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

The variable `x` is now immutable, and the warning no longer appears.

You can also use the `cargo fix` command to transition your code between
different Rust editions. Editions are covered in [Appendix E][section-appendix-04-useful-development-tools-ref-2]<!--
ignore -->.

<a id="section-appendix-04-useful-development-tools--more-lints-with-clippy"></a>

## More Lints with Clippy

The Clippy tool is a collection of lints to analyze your code so that you can
catch common mistakes and improve your Rust code. Clippy is included with
standard Rust installations.

To run Clippy’s lints on any Cargo project, enter the following:

```console
$ cargo clippy
```

For example, say you write a program that uses an approximation of a
mathematical constant, such as pi, as this program does:

Filename: `src/main.rs`

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```


Running `cargo clippy` on this project results in this error:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

This error lets you know that Rust already has a more precise `PI` constant
defined, and that your program would be more correct if you used the constant
instead. You would then change your code to use the `PI` constant.

The following code doesn’t result in any errors or warnings from Clippy:

Filename: `src/main.rs`

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```


For more information on Clippy, see [its documentation][section-appendix-04-useful-development-tools-ref-3].

<a id="section-appendix-04-useful-development-tools--ide-integration-using-rust-analyzer"></a>

## IDE Integration Using `rust-analyzer`

To help with IDE integration, the Rust community recommends using
[`rust-analyzer`][section-appendix-04-useful-development-tools-ref-4]<!-- ignore -->. This tool is a set of
compiler-centric utilities that speak [Language Server Protocol][section-appendix-04-useful-development-tools-ref-5]<!--
ignore -->, which is a specification for IDEs and programming languages to
communicate with each other. Different clients can use `rust-analyzer`, such as
[the Rust analyzer plug-in for Visual Studio Code][section-appendix-04-useful-development-tools-ref-6].

Visit the `rust-analyzer` project’s [home page][section-appendix-04-useful-development-tools-ref-4]<!-- ignore -->
for installation instructions, then install the language server support in your
particular IDE. Your IDE will gain capabilities such as autocompletion, jump to
definition, and inline errors.

[section-appendix-04-useful-development-tools-ref-1]: https://github.com/rust-lang/rustfmt
[section-appendix-04-useful-development-tools-ref-2]: 05-editions.md
[section-appendix-04-useful-development-tools-ref-3]: https://github.com/rust-lang/rust-clippy
[section-appendix-04-useful-development-tools-ref-4]: https://rust-analyzer.github.io
[section-appendix-04-useful-development-tools-ref-5]: http://langserver.org/
[section-appendix-04-useful-development-tools-ref-6]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer
