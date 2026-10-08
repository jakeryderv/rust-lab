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

Follow the Book in chapter order, explore the matching Rust by Example sections, and practice with Rustlings. Links point to local Markdown files; `—` means there is no dedicated counterpart.

| Rust Book | Rustlings | Rust by Example |
| :--- | :--- | :--- |
| [1. Getting Started](references/book/ch01-00-getting-started.md) | [Intro](rustlings/exercises/00_intro/README.md) | [Hello World](references/rust-by-example/hello.md), [Cargo](references/rust-by-example/cargo.md) |
| [2. Programming a Guessing Game](references/book/ch02-00-guessing-game-tutorial.md) | — | Supporting examples: [String Conversions](references/rust-by-example/conversion/string.md), [Match](references/rust-by-example/flow_control/match.md), [Loop](references/rust-by-example/flow_control/loop.md) |
| [3. Common Programming Concepts](references/book/ch03-00-common-programming-concepts.md) | [Variables](rustlings/exercises/01_variables/README.md), [Functions](rustlings/exercises/02_functions/README.md), [If](rustlings/exercises/03_if/README.md), [Primitive Types](rustlings/exercises/04_primitive_types/README.md) | [Variable Bindings](references/rust-by-example/variable_bindings.md), [Primitives](references/rust-by-example/primitives.md), [Functions](references/rust-by-example/fn.md), [Expressions](references/rust-by-example/expression.md), [Flow of Control](references/rust-by-example/flow_control.md), [Comments](references/rust-by-example/hello/comment.md) |
| [4. Understanding Ownership](references/book/ch04-00-understanding-ownership.md) | [Move Semantics](rustlings/exercises/06_move_semantics/README.md), [Primitive Types (slices)](rustlings/exercises/04_primitive_types/README.md) | [Ownership and Moves](references/rust-by-example/scope/move.md), [Borrowing](references/rust-by-example/scope/borrow.md), [Arrays and Slices](references/rust-by-example/primitives/array.md) |
| [5. Structs](references/book/ch05-00-structs.md) | [Structs](rustlings/exercises/07_structs/README.md) | [Structures](references/rust-by-example/custom_types/structs.md), [Methods](references/rust-by-example/fn/methods.md) |
| [6. Enums and Pattern Matching](references/book/ch06-00-enums.md) | [Enums](rustlings/exercises/08_enums/README.md), [Options](rustlings/exercises/12_options/README.md) | [Enums](references/rust-by-example/custom_types/enum.md), [Match](references/rust-by-example/flow_control/match.md), [Option](references/rust-by-example/std/option.md), [If Let](references/rust-by-example/flow_control/if_let.md), [Let-Else](references/rust-by-example/flow_control/let_else.md) |
| [7. Packages, Crates, and Modules](references/book/ch07-00-managing-growing-projects-with-packages-crates-and-modules.md) | [Modules](rustlings/exercises/10_modules/README.md) | [Modules](references/rust-by-example/mod.md), [Crates](references/rust-by-example/crates.md), [Cargo Conventions](references/rust-by-example/cargo/conventions.md) |
| [8. Common Collections](references/book/ch08-00-common-collections.md) | [Vectors](rustlings/exercises/05_vecs/README.md), [Strings](rustlings/exercises/09_strings/README.md), [Hashmaps](rustlings/exercises/11_hashmaps/README.md) | [Vectors](references/rust-by-example/std/vec.md), [Strings](references/rust-by-example/std/str.md), [HashMap](references/rust-by-example/std/hash.md) |
| [9. Error Handling](references/book/ch09-00-error-handling.md) | [Error Handling](rustlings/exercises/13_error_handling/README.md) | [Error Handling](references/rust-by-example/error.md), [Panic](references/rust-by-example/error/panic.md), [Result](references/rust-by-example/error/result.md), [The `?` Operator](references/rust-by-example/error/result/enter_question_mark.md) |
| [10. Generics, Traits, and Lifetimes](references/book/ch10-00-generics.md) | [Generics](rustlings/exercises/14_generics/README.md), [Traits](rustlings/exercises/15_traits/README.md), [Lifetimes](rustlings/exercises/16_lifetimes/README.md) | [Generics](references/rust-by-example/generics.md), [Traits](references/rust-by-example/trait.md), [Lifetimes](references/rust-by-example/scope/lifetime.md) |
| [11. Automated Tests](references/book/ch11-00-testing.md) | [Tests](rustlings/exercises/17_tests/README.md) | [Testing](references/rust-by-example/testing.md), [Unit Testing](references/rust-by-example/testing/unit_testing.md), [Integration Testing](references/rust-by-example/testing/integration_testing.md), [Documentation Testing](references/rust-by-example/testing/doc_testing.md) |
| [12. Command Line Project](references/book/ch12-00-an-io-project.md) | — | [Program Arguments](references/rust-by-example/std_misc/arg.md), [File I/O](references/rust-by-example/std_misc/file.md), [Paths](references/rust-by-example/std_misc/path.md) |
| [13. Iterators and Closures](references/book/ch13-00-functional-features.md) | [Iterators](rustlings/exercises/18_iterators/README.md) | [Closures](references/rust-by-example/fn/closures.md), [Iterators](references/rust-by-example/trait/iter.md), [Higher Order Functions](references/rust-by-example/fn/hof.md) |
| [14. More About Cargo and Crates.io](references/book/ch14-00-more-about-cargo.md) | — | Related topics: [Cargo](references/rust-by-example/cargo.md), [Documentation](references/rust-by-example/meta/doc.md) |
| [15. Smart Pointers](references/book/ch15-00-smart-pointers.md) | [Smart Pointers](rustlings/exercises/19_smart_pointers/README.md) (save `arc1` for Ch. 16; `cow1` is an extension) | [Box, Stack, and Heap](references/rust-by-example/std/box.md), [Rc](references/rust-by-example/std/rc.md), [RAII](references/rust-by-example/scope/raii.md), [Drop](references/rust-by-example/trait/drop.md) |
| [16. Fearless Concurrency](references/book/ch16-00-concurrency.md) | [Threads](rustlings/exercises/20_threads/README.md), [Smart Pointers (`arc1`)](rustlings/exercises/19_smart_pointers/README.md) | [Threads](references/rust-by-example/std_misc/threads.md), [Channels](references/rust-by-example/std_misc/channels.md), [Arc](references/rust-by-example/std/arc.md) |
| [17. Async and Await](references/book/ch17-00-async-await.md) | — | — |
| [18. Object-Oriented Features](references/book/ch18-00-oop.md) | Review: [Traits](rustlings/exercises/15_traits/README.md), [Enums](rustlings/exercises/08_enums/README.md) | [Trait Objects with `dyn`](references/rust-by-example/trait/dyn.md) |
| [19. Patterns and Matching](references/book/ch19-00-patterns.md) | Review: [Enums](rustlings/exercises/08_enums/README.md), [Options](rustlings/exercises/12_options/README.md) | [Destructuring](references/rust-by-example/flow_control/match/destructuring.md), [Guards](references/rust-by-example/flow_control/match/guard.md), [Bindings](references/rust-by-example/flow_control/match/binding.md), [While Let](references/rust-by-example/flow_control/while_let.md) |
| [20. Advanced Features](references/book/ch20-00-advanced-features.md) | [Macros](rustlings/exercises/21_macros/README.md) | [Unsafe Operations](references/rust-by-example/unsafe.md), [Associated Types](references/rust-by-example/generics/assoc_items/types.md), [Supertraits](references/rust-by-example/trait/supertraits.md), [New Type Idiom](references/rust-by-example/generics/new_types.md), [Type Aliases](references/rust-by-example/types/alias.md), [Macros](references/rust-by-example/macros.md) |
| [21. Multithreaded Web Server](references/book/ch21-00-final-project-a-web-server.md) | Review: [Threads](rustlings/exercises/20_threads/README.md) | Review: [Threads](references/rust-by-example/std_misc/threads.md), [Channels](references/rust-by-example/std_misc/channels.md) |
| [Appendix D. Development Tools](references/book/appendix-04-useful-development-tools.md) | [Clippy](rustlings/exercises/22_clippy/README.md) | — |

Additional practice: [Rustlings quizzes](rustlings/exercises/quizzes/README.md). After Chapter 10, pair [Rustlings conversions](rustlings/exercises/23_conversions/README.md) with Rust by Example's [Conversion](references/rust-by-example/conversion.md) and [Casting](references/rust-by-example/types/cast.md) sections.
