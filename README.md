# rust-lab

[rust book](https://doc.rust-lang.org/book/)
[rust by example](https://doc.rust-lang.org/rust-by-example/)
[rustlings](https://github.com/rust-lang/rustlings/)

[Local reference library](references/README.md)

```
rust-lab/
├── notes/
├── references/
├── rustlings/
├── experiments/
└── projects/
```

| Directory | Purpose |
| :--- | :---: |
| `notes/` | Concepts, references, study notes |
| `references/` | Local Markdown copies of the Rust Book and Rust by Example |
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
| [1. Getting Started](references/book/01-getting-started.md) | [1. Hello World](references/rust-by-example/01-hello-world.md), [12. Cargo](references/rust-by-example/12-cargo.md) | [Intro](rustlings/exercises/00_intro/README.md) |
| [2. Programming a Guessing Game](references/book/02-guessing-game-tutorial.md) | — | — |
| [3. Common Programming Concepts](references/book/03-common-programming-concepts.md) | [2. Primitives](references/rust-by-example/02-primitives.md), [4. Variable Bindings](references/rust-by-example/04-variable-bindings.md), [7. Expressions](references/rust-by-example/07-expressions.md), [8. Flow of Control](references/rust-by-example/08-flow-of-control.md), [9. Functions](references/rust-by-example/09-functions.md) | [Variables](rustlings/exercises/01_variables/README.md), [Functions](rustlings/exercises/02_functions/README.md), [If](rustlings/exercises/03_if/README.md), [Primitive Types](rustlings/exercises/04_primitive_types/README.md) |
| [4. Understanding Ownership](references/book/04-understanding-ownership.md) | [15. Scoping rules](references/rust-by-example/15-scoping-rules.md) | [Move Semantics](rustlings/exercises/06_move_semantics/README.md) |
| [5. Structs](references/book/05-structs.md) | [3. Custom Types](references/rust-by-example/03-custom-types.md) | [Structs](rustlings/exercises/07_structs/README.md) |
| [6. Enums and Pattern Matching](references/book/06-enums.md) | [3. Custom Types](references/rust-by-example/03-custom-types.md), [8. Flow of Control](references/rust-by-example/08-flow-of-control.md) | [Enums](rustlings/exercises/08_enums/README.md), [Options](rustlings/exercises/12_options/README.md) |
| [7. Packages, Crates, and Modules](references/book/07-managing-growing-projects-with-packages-crates-and-modules.md) | [10. Modules](references/rust-by-example/10-modules.md), [11. Crates](references/rust-by-example/11-crates.md), [12. Cargo](references/rust-by-example/12-cargo.md) | [Modules](rustlings/exercises/10_modules/README.md) |
| [8. Common Collections](references/book/08-common-collections.md) | [19. Std library types](references/rust-by-example/19-std-library-types.md) | [Vectors](rustlings/exercises/05_vecs/README.md), [Strings](rustlings/exercises/09_strings/README.md), [Hashmaps](rustlings/exercises/11_hashmaps/README.md) |
| [9. Error Handling](references/book/09-error-handling.md) | [18. Error handling](references/rust-by-example/18-error-handling.md) | [Error Handling](rustlings/exercises/13_error_handling/README.md) |
| [10. Generics, Traits, and Lifetimes](references/book/10-generics.md) | [14. Generics](references/rust-by-example/14-generics.md), [15. Scoping rules](references/rust-by-example/15-scoping-rules.md), [16. Traits](references/rust-by-example/16-traits.md) | [Generics](rustlings/exercises/14_generics/README.md), [Traits](rustlings/exercises/15_traits/README.md), [Lifetimes](rustlings/exercises/16_lifetimes/README.md) |
| [11. Automated Tests](references/book/11-testing.md) | [21. Testing](references/rust-by-example/21-testing.md) | [Tests](rustlings/exercises/17_tests/README.md) |
| [12. Command Line Project](references/book/12-an-io-project.md) | [20. Std misc](references/rust-by-example/20-std-misc.md) | — |
| [13. Iterators and Closures](references/book/13-functional-features.md) | [9. Functions](references/rust-by-example/09-functions.md), [16. Traits](references/rust-by-example/16-traits.md) | [Iterators](rustlings/exercises/18_iterators/README.md) |
| [14. More About Cargo and Crates.io](references/book/14-more-about-cargo.md) | [12. Cargo](references/rust-by-example/12-cargo.md) | — |
| [15. Smart Pointers](references/book/15-smart-pointers.md) | [19. Std library types](references/rust-by-example/19-std-library-types.md) | [Smart Pointers](rustlings/exercises/19_smart_pointers/README.md) |
| [16. Fearless Concurrency](references/book/16-concurrency.md) | [20. Std misc](references/rust-by-example/20-std-misc.md) | [Threads](rustlings/exercises/20_threads/README.md) |
| [17. Async and Await](references/book/17-async-await.md) | — | — |
| [18. Object-Oriented Features](references/book/18-oop.md) | [16. Traits](references/rust-by-example/16-traits.md) | [Traits](rustlings/exercises/15_traits/README.md), [Enums](rustlings/exercises/08_enums/README.md) |
| [19. Patterns and Matching](references/book/19-patterns.md) | [8. Flow of Control](references/rust-by-example/08-flow-of-control.md) | [Enums](rustlings/exercises/08_enums/README.md), [Options](rustlings/exercises/12_options/README.md) |
| [20. Advanced Features](references/book/20-advanced-features.md) | [17. macro_rules!](references/rust-by-example/17-macro_rules.md), [22. Unsafe Operations](references/rust-by-example/22-unsafe-operations.md) | [Macros](rustlings/exercises/21_macros/README.md) |
| [21. Multithreaded Web Server](references/book/21-final-project-a-web-server.md) | [20. Std misc](references/rust-by-example/20-std-misc.md) | [Threads](rustlings/exercises/20_threads/README.md) |
| [Appendix D. Development Tools](references/book/appendices/04-useful-development-tools.md) | — | [Clippy](rustlings/exercises/22_clippy/README.md) |

Additional practice: [Rustlings quizzes](rustlings/exercises/quizzes/README.md). After Chapter 10, pair [Rustlings conversions](rustlings/exercises/23_conversions/README.md) with Rust by Example's [5. Types](references/rust-by-example/05-types.md) and [6. Conversion](references/rust-by-example/06-conversion.md) chapters.
