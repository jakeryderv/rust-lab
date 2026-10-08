<a id="section-meta"></a>

<a id="section-meta--meta"></a>

# Meta

[Chapter index](SUMMARY.md)

**In this chapter**

- [Documentation](#section-meta-doc)
- [Playground](#section-meta-playground)


Some topics aren't exactly relevant to how your program runs but provide you
tooling or infrastructure support which just makes things better for
everyone. These topics include:

- [Documentation][section-meta-ref-1]: Generate library documentation for users via the included
  `rustdoc`.
- [Playground][section-meta-ref-2]: Integrate the Rust Playground in your documentation.

[section-meta-ref-1]: #section-meta-doc
[section-meta-ref-2]: #section-meta-playground

<a id="section-meta-doc"></a>

<a id="section-meta-doc--documentation"></a>

## Documentation

Use `cargo doc` to build documentation in `target/doc`, `cargo doc --open`
will automatically open it in your web browser.

Use `cargo test` to run all tests (including documentation tests), and `cargo
test --doc` to only run documentation tests.

These commands will appropriately invoke `rustdoc` (and `rustc`) as required.

<a id="section-meta-doc--doc-comments"></a>

### Doc comments

Doc comments are very useful for big projects that require documentation. When
running `rustdoc`, these are the comments that get compiled into
documentation. They are denoted by a `///`, and support [Markdown][section-meta-doc-ref-1].

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

````rust
#![crate_name = "doc"]

/// A human being is represented here
pub struct Person {
    /// A person must have a name, no matter how much Juliet may hate it
    name: String,
}

impl Person {
    /// Creates a person with the given name.
    ///
    /// # Examples
    ///
    /// ```
    /// // You can have rust code between fences inside the comments
    /// // If you pass --test to `rustdoc`, it will even test it for you!
    /// use doc::Person;
    /// let person = Person::new("name");
    /// ```
    pub fn new(name: &str) -> Person {
        Person {
            name: name.to_string(),
        }
    }

    /// Gives a friendly hello!
    ///
    /// Says "Hello, [name](Person::name)" to the `Person` it is called on.
    pub fn hello(&self) {
        println!("Hello, {}!", self.name);
    }
}

fn main() {
    let john = Person::new("John");

    john.hello();
}
````

To run the tests, first build the code as a library, then tell `rustdoc` where
to find the library so it can link it into each doctest program:

```shell
$ rustc doc.rs --crate-type lib
$ rustdoc --test --extern doc="libdoc.rlib" doc.rs
```

<a id="section-meta-doc--doc-attributes"></a>

### Doc attributes

Below are a few examples of the most common `#[doc]` attributes used with
`rustdoc`.

<a id="section-meta-doc--inline"></a>

#### `inline`

Used to inline docs, instead of linking out to separate page.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
#[doc(inline)]
pub use bar::Bar;

/// bar docs
pub mod bar {
    /// the docs for Bar
    pub struct Bar;
}
```

<a id="section-meta-doc--no_inline"></a>

#### `no_inline`

Used to prevent linking out to separate page or anywhere.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Example from libcore/prelude
#[doc(no_inline)]
pub use crate::mem::drop;
```

<a id="section-meta-doc--hidden"></a>

#### `hidden`

Using this tells `rustdoc` not to include this in documentation:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// Example from the futures-rs library
#[doc(hidden)]
pub use self::async_await::*;
```

For documentation, `rustdoc` is widely used by the community. It's what is used
to generate the [std library docs](https://doc.rust-lang.org/std/).

<a id="section-meta-doc--see-also"></a>

#### See also:

- [The Rust Book: Making Useful Documentation Comments][section-meta-doc-ref-2]
- [The rustdoc Book][section-meta-doc-ref-4]
- [The Reference: Doc comments][section-meta-doc-ref-3]
- [RFC 1574: API Documentation Conventions][section-meta-doc-ref-5]
- [RFC 1946: Relative links to other items from doc comments (intra-rustdoc links)][section-meta-doc-ref-6]
- [Is there any documentation style guide for comments? (reddit)][section-meta-doc-ref-7]

[section-meta-doc-ref-1]: https://en.wikipedia.org/wiki/Markdown
[section-meta-doc-ref-2]: https://doc.rust-lang.org/book/ch14-02-publishing-to-crates-io.html#making-useful-documentation-comments
[section-meta-doc-ref-3]: https://doc.rust-lang.org/stable/reference/comments.html#doc-comments
[section-meta-doc-ref-4]: https://doc.rust-lang.org/rustdoc/index.html
[section-meta-doc-ref-5]: https://rust-lang.github.io/rfcs/1574-more-api-documentation-conventions.html#appendix-a-full-conventions-text
[section-meta-doc-ref-6]: https://rust-lang.github.io/rfcs/1946-intra-rustdoc-links.html
[section-meta-doc-ref-7]: https://www.reddit.com/r/rust/comments/ahb50s/is_there_any_documentation_style_guide_for/

<a id="section-meta-playground"></a>

<a id="section-meta-playground--playground"></a>

## Playground

The [Rust Playground](https://play.rust-lang.org/) is a way to experiment with
Rust code through a web interface.

<a id="section-meta-playground--using-it-with-mdbook"></a>

### Using it with `mdbook`

In [`mdbook`][section-meta-playground-ref-3], you can make code examples playable and editable.

```rust
fn main() {
    println!("Hello World!");
}
```

This allows the reader to both run your code sample, but also modify and tweak
it. The key here is the adding of the word `editable` to your codefence block
separated by a comma.

````markdown
```rust,editable
//...place your code here
```
````

Additionally, you can add `ignore` if you want `mdbook` to skip your code when
it builds and tests.

````markdown
```rust,editable,ignore
//...place your code here
```
````

<a id="section-meta-playground--using-it-with-docs"></a>

### Using it with docs

You may have noticed in some of the [official Rust docs][section-meta-playground-ref-4] a
button that says "Run", which opens the code sample up in a new tab in Rust
Playground. This feature is enabled if you use the `#[doc]` attribute called
[`html_playground_url`][section-meta-playground-ref-6].

```text
#![doc(html_playground_url = "https://play.rust-lang.org/")]
//! ```
//! println!("Hello World");
//! ```
```

<a id="section-meta-playground--see-also"></a>

#### See also:

- [The Rust Playground][section-meta-playground-ref-1]
- [The Rust Playground On Github][section-meta-playground-ref-2]
- [The rustdoc Book][section-meta-playground-ref-5]

[section-meta-playground-ref-1]: https://play.rust-lang.org/
[section-meta-playground-ref-2]: https://github.com/integer32llc/rust-playground/
[section-meta-playground-ref-3]: https://github.com/rust-lang/mdBook
[section-meta-playground-ref-4]: https://doc.rust-lang.org/core/
[section-meta-playground-ref-5]: https://doc.rust-lang.org/rustdoc/what-is-rustdoc.html
[section-meta-playground-ref-6]: https://doc.rust-lang.org/rustdoc/write-documentation/the-doc-attribute.html#html_playground_url
