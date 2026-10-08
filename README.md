# rust-lab

[rust book](https://doc.rust-lang.org/book/)
[rust by example](https://doc.rust-lang.org/rust-by-example/)
[rustlings](https://github.com/rust-lang/rustlings/)

```
rust-lab/
├── notes/
├── rustlings/
├── experiments/
└── projects/
```

| Directory | Purpose |
| :--- | :---: |
| `notes/` | Concepts, references, study notes |
| `rustlings/` | Rustlings exercises |
| `experiments/` | Quick throwaway tests, API exploration, syntax trials, crate experiments |
| `projects/` | Intentional programs with some structure or progression |

> `experiments/`     "I want to see how this works"
> `project/`         "I want to build something"

## roadmap

Read the Book chapter, work through the related Rust by Example chapters, then complete the Rustlings exercise groups.
Repeated entries are review; `—` means there is no direct match.

| Rust Book | Rust by Example | Rustlings |
| :--- | :--- | :--- |
| [1. Getting Started](https://doc.rust-lang.org/book/ch01-00-getting-started.html) | [1. Hello World](https://doc.rust-lang.org/rust-by-example/hello.html), [12. Cargo](https://doc.rust-lang.org/rust-by-example/cargo.html) | [Intro](rustlings/exercises/00_intro/README.md) |
| [2. Programming a Guessing Game](https://doc.rust-lang.org/book/ch02-00-guessing-game-tutorial.html) | — | — |
| [3. Common Programming Concepts](https://doc.rust-lang.org/book/ch03-00-common-programming-concepts.html) | [2. Primitives](https://doc.rust-lang.org/rust-by-example/primitives.html), [4. Variable Bindings](https://doc.rust-lang.org/rust-by-example/variable_bindings.html), [7. Expressions](https://doc.rust-lang.org/rust-by-example/expression.html), [8. Flow of Control](https://doc.rust-lang.org/rust-by-example/flow_control.html), [9. Functions](https://doc.rust-lang.org/rust-by-example/fn.html) | [Variables](rustlings/exercises/01_variables/README.md), [Functions](rustlings/exercises/02_functions/README.md), [If](rustlings/exercises/03_if/README.md), [Primitive Types](rustlings/exercises/04_primitive_types/README.md) |
| [4. Understanding Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) | [15. Scoping rules](https://doc.rust-lang.org/rust-by-example/scope.html) | [Move Semantics](rustlings/exercises/06_move_semantics/README.md) |
| [5. Structs](https://doc.rust-lang.org/book/ch05-00-structs.html) | [3. Custom Types](https://doc.rust-lang.org/rust-by-example/custom_types.html) | [Structs](rustlings/exercises/07_structs/README.md) |
| [6. Enums and Pattern Matching](https://doc.rust-lang.org/book/ch06-00-enums.html) | [3. Custom Types](https://doc.rust-lang.org/rust-by-example/custom_types.html), [8. Flow of Control](https://doc.rust-lang.org/rust-by-example/flow_control.html) | [Enums](rustlings/exercises/08_enums/README.md), [Options](rustlings/exercises/12_options/README.md) |
| [7. Packages, Crates, and Modules](https://doc.rust-lang.org/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.html) | [10. Modules](https://doc.rust-lang.org/rust-by-example/mod.html), [11. Crates](https://doc.rust-lang.org/rust-by-example/crates.html), [12. Cargo](https://doc.rust-lang.org/rust-by-example/cargo.html) | [Modules](rustlings/exercises/10_modules/README.md) |
| [8. Common Collections](https://doc.rust-lang.org/book/ch08-00-common-collections.html) | [19. Std library types](https://doc.rust-lang.org/rust-by-example/std.html) | [Vectors](rustlings/exercises/05_vecs/README.md), [Strings](rustlings/exercises/09_strings/README.md), [Hashmaps](rustlings/exercises/11_hashmaps/README.md) |
| [9. Error Handling](https://doc.rust-lang.org/book/ch09-00-error-handling.html) | [18. Error handling](https://doc.rust-lang.org/rust-by-example/error.html) | [Error Handling](rustlings/exercises/13_error_handling/README.md) |
| [10. Generics, Traits, and Lifetimes](https://doc.rust-lang.org/book/ch10-00-generics.html) | [14. Generics](https://doc.rust-lang.org/rust-by-example/generics.html), [15. Scoping rules](https://doc.rust-lang.org/rust-by-example/scope.html), [16. Traits](https://doc.rust-lang.org/rust-by-example/trait.html) | [Generics](rustlings/exercises/14_generics/README.md), [Traits](rustlings/exercises/15_traits/README.md), [Lifetimes](rustlings/exercises/16_lifetimes/README.md) |
| [11. Automated Tests](https://doc.rust-lang.org/book/ch11-00-testing.html) | [21. Testing](https://doc.rust-lang.org/rust-by-example/testing.html) | [Tests](rustlings/exercises/17_tests/README.md) |
| [12. Command Line Project](https://doc.rust-lang.org/book/ch12-00-an-io-project.html) | [20. Std misc](https://doc.rust-lang.org/rust-by-example/std_misc.html) | — |
| [13. Iterators and Closures](https://doc.rust-lang.org/book/ch13-00-functional-features.html) | [9. Functions](https://doc.rust-lang.org/rust-by-example/fn.html), [16. Traits](https://doc.rust-lang.org/rust-by-example/trait.html) | [Iterators](rustlings/exercises/18_iterators/README.md) |
| [14. More About Cargo and Crates.io](https://doc.rust-lang.org/book/ch14-00-more-about-cargo.html) | [12. Cargo](https://doc.rust-lang.org/rust-by-example/cargo.html) | — |
| [15. Smart Pointers](https://doc.rust-lang.org/book/ch15-00-smart-pointers.html) | [19. Std library types](https://doc.rust-lang.org/rust-by-example/std.html) | [Smart Pointers](rustlings/exercises/19_smart_pointers/README.md) |
| [16. Fearless Concurrency](https://doc.rust-lang.org/book/ch16-00-concurrency.html) | [20. Std misc](https://doc.rust-lang.org/rust-by-example/std_misc.html) | [Threads](rustlings/exercises/20_threads/README.md) |
| [17. Async and Await](https://doc.rust-lang.org/book/ch17-00-async-await.html) | — | — |
| [18. Object-Oriented Features](https://doc.rust-lang.org/book/ch18-00-oop.html) | [16. Traits](https://doc.rust-lang.org/rust-by-example/trait.html) | [Traits](rustlings/exercises/15_traits/README.md), [Enums](rustlings/exercises/08_enums/README.md) |
| [19. Patterns and Matching](https://doc.rust-lang.org/book/ch19-00-patterns.html) | [8. Flow of Control](https://doc.rust-lang.org/rust-by-example/flow_control.html) | [Enums](rustlings/exercises/08_enums/README.md), [Options](rustlings/exercises/12_options/README.md) |
| [20. Advanced Features](https://doc.rust-lang.org/book/ch20-00-advanced-features.html) | [17. macro_rules!](https://doc.rust-lang.org/rust-by-example/macros.html), [22. Unsafe Operations](https://doc.rust-lang.org/rust-by-example/unsafe.html) | [Macros](rustlings/exercises/21_macros/README.md) |
| [21. Multithreaded Web Server](https://doc.rust-lang.org/book/ch21-00-final-project-a-web-server.html) | [20. Std misc](https://doc.rust-lang.org/rust-by-example/std_misc.html) | [Threads](rustlings/exercises/20_threads/README.md) |
| [Appendix D. Development Tools](https://doc.rust-lang.org/book/appendix-04-useful-development-tools.html) | — | [Clippy](rustlings/exercises/22_clippy/README.md) |

Additional practice: [Rustlings quizzes](rustlings/exercises/quizzes/README.md). After Chapter 10, pair [Rustlings conversions](rustlings/exercises/23_conversions/README.md) with Rust by Example's [5. Types](https://doc.rust-lang.org/rust-by-example/types.html) and [6. Conversion](https://doc.rust-lang.org/rust-by-example/conversion.html) chapters.
