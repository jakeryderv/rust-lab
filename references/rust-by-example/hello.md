# Hello World

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

`println!` is a [*macro*][macros] that prints text to the
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

### Activity

Compile and run the program locally to see the expected output. Next, add a new
line with a second `println!` macro so that the output shows:

```text
Hello World!
I'm a Rustacean!
```

[macros]: macros.md
