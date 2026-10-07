# Rust Project Learning Ladder

Use this alongside the **Rust Book**, **Rustlings**, documentation, and real code.

The goal is to progress from:

```text
learning Rust syntax
        ↓
writing Rust code
        ↓
building Rust programs
        ↓
designing Rust applications
        ↓
understanding advanced Rust
```

## Project Ladder

| Level | Build | Main things learned |
|---|---|---|
| **0** | Tiny programs | Syntax, compiler feedback, basic types |
| **1** | Single-file utility | Ownership, borrowing, `Option`, `Result` |
| **2** | Multi-module program | Modules, visibility, structs, enums, API design |
| **3** | Real CLI | Cargo ecosystem, argument parsing, errors |
| **4** | Persistent CLI | Files, config, serialization, saved state |
| **5** | Library + CLI | Public APIs, crate boundaries, testing |
| **6** | REPL | Parsing, command architecture, long-lived state |
| **7** | TUI | Event loops, state machines, terminal I/O, components |
| **8** | Async/network app | Futures, Tokio, tasks, HTTP, channels |
| **9** | Desktop GUI | UI architecture, events, concurrency |
| **10** | Workspace application | Multiple crates, architecture, reusable components |
| **11** | Advanced Rust | Macros, proc macros, unsafe, FFI, performance |

---

## Learning Progression

Learn through three tracks at the same time:

| Track | Progression |
|---|---|
| **Language** | ownership → enums → errors → traits → generics → lifetimes → iterators → smart pointers → concurrency → macros |
| **Ecosystem** | Cargo → crates → docs.rs → testing → common crates → workspaces → publishing |
| **Projects** | utility → CLI → persistence → library → REPL → TUI → async → GUI → workspace |

Do **not** finish one track before starting the others.

Use this loop:

```text
Book / Rustlings concept
        ↓
practice small example
        ↓
use it in project
        ↓
encounter real crate/API
        ↓
read relevant docs/examples
        ↓
refactor project
        ↓
continue
```

---

## Suggested Project Evolution

Instead of many disconnected beginner projects, evolve one project:

```text
basic program
    ↓
multi-module program
    ↓
CLI
    ↓
config + persistence
    ↓
library + CLI
    ↓
REPL
    ↓
TUI
    ↓
async/networking
    ↓
desktop GUI
    ↓
multi-crate workspace
    ↓
macros / plugins / advanced Rust
```

This lets each stage introduce a new software-engineering problem without restarting from scratch.

---

## Crates to Learn as Needed

| Need | Representative crates |
|---|---|
| CLI | `clap` |
| Serialization | `serde`, `serde_json` |
| Application errors | `anyhow` |
| Library errors | `thiserror` |
| Async | `tokio` |
| HTTP | `reqwest` |
| Diagnostics | `tracing` |
| TUI | `ratatui`, `crossterm` |
| GUI | `egui`, `eframe` |

Do not study all of these beforehand. Introduce them when the project requires them.

---

## Resource Roles

| Resource | Use it for |
|---|---|
| **Rust Book** | Learn how Rust works |
| **Rustlings** | Practice concepts and syntax |
| **Personal project** | Learn to build real Rust software |
| **std docs** | Look up standard-library APIs |
| **docs.rs** | Learn crate APIs |
| **Cargo Book** | Packages, crates, features, workspaces |
| **Rust CLI Book** | Bridge into real application development |
| **Existing Rust projects** | Learn idiomatic architecture and patterns |

## Core Rule

Don't try to learn all of Rust before building things.

```text
learn concept
→ use concept
→ hit limitation
→ learn next concept
→ improve project
```

The progression is roughly:

**syntax → ownership → types → traits → errors → modules → crates → macros → state → concurrency → architecture → advanced metaprogramming**
