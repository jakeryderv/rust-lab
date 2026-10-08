<a id="section-variable_bindings"></a>

<a id="section-variable_bindings--variable-bindings"></a>

# Variable Bindings

[Chapter index](SUMMARY.md)

**In this chapter**

- [Mutability](#section-variable_bindings-mut)
- [Scope and Shadowing](#section-variable_bindings-scope)
- [Declare first](#section-variable_bindings-declare)
- [Freezing](#section-variable_bindings-freeze)


Rust provides type safety via static typing. Variable bindings can be type
annotated when declared. However, in most cases, the compiler will be able
to infer the type of the variable from the context, heavily reducing the
annotation burden.

Values (like literals) can be bound to variables, using the `let` binding.

```rust
fn main() {
    let an_integer = 1u32;
    let a_boolean = true;
    let unit = ();

    // copy `an_integer` into `copied_integer`
    let copied_integer = an_integer;

    println!("An integer: {}", copied_integer);
    println!("A boolean: {}", a_boolean);
    println!("Meet the unit value: {:?}", unit);

    // The compiler warns about unused variable bindings; these warnings can
    // be silenced by prefixing the variable name with an underscore
    let _unused_variable = 3u32;

    let noisy_unused_variable = 2u32;
    // FIXME ^ Prefix with an underscore to suppress the warning
    // Please note that warnings may not be shown in a browser
}
```

<a id="section-variable_bindings-mut"></a>

<a id="section-variable_bindings-mut--mutability"></a>

## Mutability

Variable bindings are immutable by default, but this can be overridden using
the `mut` modifier.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    let _immutable_binding = 1;
    let mut mutable_binding = 1;

    println!("Before mutation: {}", mutable_binding);

    // Ok
    mutable_binding += 1;

    println!("After mutation: {}", mutable_binding);

    // Error! Cannot assign a new value to an immutable variable
    _immutable_binding += 1;
}
```

The compiler will throw a detailed diagnostic about mutability errors.

<a id="section-variable_bindings-scope"></a>

<a id="section-variable_bindings-scope--scope-and-shadowing"></a>

## Scope and Shadowing

Variable bindings have a scope, and are constrained to live in a *block*. A
block is a collection of statements enclosed by braces `{}`.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    // This binding lives in the main function
    let long_lived_binding = 1;

    // This is a block, and has a smaller scope than the main function
    {
        // This binding only exists in this block
        let short_lived_binding = 2;

        println!("inner short: {}", short_lived_binding);
    }
    // End of the block

    // Error! `short_lived_binding` doesn't exist in this scope
    println!("outer short: {}", short_lived_binding);
    // FIXME ^ Comment out this line

    println!("outer long: {}", long_lived_binding);
}
```

Also, [variable shadowing][section-variable_bindings-scope-ref-1] is allowed.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    let shadowed_binding = 1;

    {
        println!("before being shadowed: {}", shadowed_binding);

        // This binding *shadows* the outer one
        let shadowed_binding = "abc";

        println!("shadowed in inner block: {}", shadowed_binding);
    }
    println!("outside inner block: {}", shadowed_binding);

    // This binding *shadows* the previous binding
    let shadowed_binding = 2;
    println!("shadowed in outer block: {}", shadowed_binding);
}
```

[section-variable_bindings-scope-ref-1]: https://en.wikipedia.org/wiki/Variable_shadowing

<a id="section-variable_bindings-declare"></a>

<a id="section-variable_bindings-declare--declare-first"></a>

## Declare first

It is possible to declare variable bindings first and initialize them later, but all variable bindings must be initialized before they are used: the compiler forbids use of uninitialized variable bindings, as it would lead to undefined behavior.

It is not common to declare a variable binding and initialize it later in the function.
It is more difficult for a reader to find the initialization when initialization is separated from declaration.
It is common to declare and initialize a variable binding near where the variable will be used.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    // Declare a variable binding
    let a_binding;

    {
        let x = 2;

        // Initialize the binding
        a_binding = x * x;
    }

    println!("a binding: {}", a_binding);

    let another_binding;

    // Error! Use of uninitialized binding
    println!("another binding: {}", another_binding);
    // FIXME ^ Comment out this line

    another_binding = 1;

    println!("another binding: {}", another_binding);
}
```

<a id="section-variable_bindings-freeze"></a>

<a id="section-variable_bindings-freeze--freezing"></a>

## Freezing

When data is bound by the same name immutably, it also *freezes*. *Frozen* data can't be
modified until the immutable binding goes out of scope:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
fn main() {
    let mut _mutable_integer = 7i32;

    {
        // Shadowing by immutable `_mutable_integer`
        let _mutable_integer = _mutable_integer;

        // Error! `_mutable_integer` is frozen in this scope
        _mutable_integer = 50;
        // FIXME ^ Comment out this line

        // `_mutable_integer` goes out of scope
    }

    // Ok! `_mutable_integer` is not frozen in this scope
    _mutable_integer = 3;
}
```
