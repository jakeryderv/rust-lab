<a id="section-scope"></a>

<a id="section-scope--scoping-rules"></a>

# Scoping rules

[Chapter index](SUMMARY.md)

**In this chapter**

- [RAII](#section-scope-raii)
- [Ownership and moves](#section-scope-move)
  - [Mutability](#section-scope-move-mut)
  - [Partial moves](#section-scope-move-partial_move)
- [Borrowing](#section-scope-borrow)
  - [Mutability](#section-scope-borrow-mut)
  - [Aliasing](#section-scope-borrow-alias)
  - [The ref pattern](#section-scope-borrow-ref)
- [Lifetimes](#section-scope-lifetime)
  - [Explicit annotation](#section-scope-lifetime-explicit)
  - [Functions](#section-scope-lifetime-fn)
  - [Methods](#section-scope-lifetime-methods)
  - [Structs](#section-scope-lifetime-struct)
  - [Traits](#section-scope-lifetime-trait)
  - [Bounds](#section-scope-lifetime-lifetime_bounds)
  - [Coercion](#section-scope-lifetime-lifetime_coercion)
  - [Static](#section-scope-lifetime-static_lifetime)
  - [Elision](#section-scope-lifetime-elision)


Scopes play an important part in ownership, borrowing, and lifetimes.
That is, they indicate to the compiler when borrows are valid, when
resources can be freed, and when variables are created or destroyed.

<a id="section-scope-raii"></a>

<a id="section-scope-raii--raii"></a>

## RAII

Variables in Rust do more than just hold data in the stack: they also *own*
resources, e.g. `Box<T>` owns memory in the heap. Rust enforces [RAII][section-scope-raii-ref-1]
(Resource Acquisition Is Initialization), so whenever an object goes out of
scope, its destructor is called and its owned resources are freed.

This behavior shields against *resource leak* bugs, so you'll never have to
manually free memory or worry about memory leaks again! Here's a quick showcase:

```rust
// raii.rs
fn create_box() {
    // Allocate an integer on the heap
    let _box1 = Box::new(3i32);

    // `_box1` is destroyed here, and memory gets freed
}

fn main() {
    // Allocate an integer on the heap
    let _box2 = Box::new(5i32);

    // A nested scope:
    {
        // Allocate an integer on the heap
        let _box3 = Box::new(4i32);

        // `_box3` is destroyed here, and memory gets freed
    }

    // Creating lots of boxes just for fun
    // There's no need to manually free memory!
    for _ in 0u32..1_000 {
        create_box();
    }

    // `_box2` is destroyed here, and memory gets freed
}
```

Of course, we can double check for memory errors using [`valgrind`][section-scope-raii-ref-3]:

<!-- REUSE-IgnoreStart -->
<!-- Prevent REUSE from parsing the copyright statement in the sample code -->
```shell
$ rustc raii.rs && valgrind ./raii
==26873== Memcheck, a memory error detector
==26873== Copyright (C) 2002-2013, and GNU GPL'd, by Julian Seward et al.
==26873== Using Valgrind-3.9.0 and LibVEX; rerun with -h for copyright info
==26873== Command: ./raii
==26873==
==26873==
==26873== HEAP SUMMARY:
==26873==     in use at exit: 0 bytes in 0 blocks
==26873==   total heap usage: 1,013 allocs, 1,013 frees, 8,696 bytes allocated
==26873==
==26873== All heap blocks were freed -- no leaks are possible
==26873==
==26873== For counts of detected and suppressed errors, rerun with: -v
==26873== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 2 from 2)
```
<!-- REUSE-IgnoreEnd -->

No leaks here!

<a id="section-scope-raii--destructor"></a>

### Destructor

The notion of a destructor in Rust is provided through the [`Drop`][section-scope-raii-ref-4] trait. The
destructor is called when the resource goes out of scope. This trait is not
required to be implemented for every type, only implement it for your type if
you require its own destructor logic.

Run the below example to see how the [`Drop`][section-scope-raii-ref-4] trait works. When the variable in
the `main` function goes out of scope the custom destructor will be invoked.

```rust
struct ToDrop;

impl Drop for ToDrop {
    fn drop(&mut self) {
        println!("ToDrop is being dropped");
    }
}

fn main() {
    let x = ToDrop;
    println!("Made a ToDrop!");
}
```

<a id="section-scope-raii--see-also"></a>

#### See also:

[Box][section-scope-raii-ref-2]

[section-scope-raii-ref-1]: https://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization
[section-scope-raii-ref-2]: 19-std-library-types.md#section-std-box
[section-scope-raii-ref-3]: http://valgrind.org/info/
[section-scope-raii-ref-4]: https://doc.rust-lang.org/std/ops/trait.Drop.html

<a id="section-scope-move"></a>

<a id="section-scope-move--ownership-and-moves"></a>

## Ownership and moves

Because variables are in charge of freeing their own resources,
**resources can only have one owner**. This prevents resources
from being freed more than once. Note that not all variables own
resources (e.g. [references][section-scope-move-ref-1]).

When doing assignments (`let x = y`) or passing function arguments by value
(`foo(x)`), the *ownership* of the resources is transferred. In Rust-speak,
this is known as a *move*.

After moving resources, the previous owner can no longer be used. This avoids
creating dangling pointers.

```rust
// This function takes ownership of the heap allocated memory
fn destroy_box(c: Box<i32>) {
    println!("Destroying a box that contains {}", c);

    // `c` is destroyed and the memory freed
}

fn main() {
    // _Stack_ allocated integer
    let x = 5u32;

    // *Copy* `x` into `y` - no resources are moved
    let y = x;

    // Both values can be independently used
    println!("x is {}, and y is {}", x, y);

    // `a` is a pointer to a _heap_ allocated integer
    let a = Box::new(5i32);

    println!("a contains: {}", a);

    // *Move* `a` into `b`
    let b = a;
    // The pointer address of `a` is copied (not the data) into `b`.
    // Both are now pointers to the same heap allocated data, but
    // `b` now owns it.

    // Error! `a` can no longer access the data, because it no longer owns the
    // heap memory
    //println!("a contains: {}", a);
    // TODO ^ Try uncommenting this line

    // This function takes ownership of the heap allocated memory from `b`
    destroy_box(b);

    // Since the heap memory has been freed at this point, this action would
    // result in dereferencing freed memory, but it's forbidden by the compiler
    // Error! Same reason as the previous Error
    //println!("b contains: {}", b);
    // TODO ^ Try uncommenting this line
}
```

[section-scope-move-ref-1]: 08-flow-of-control.md#section-flow_control-match-destructuring-destructure_pointers

<a id="section-scope-move-mut"></a>

<a id="section-scope-move-mut--mutability"></a>

### Mutability

Mutability of data can be changed when ownership is transferred.

```rust
fn main() {
    let immutable_box = Box::new(5u32);

    println!("immutable_box contains {}", immutable_box);

    // Mutability error
    //*immutable_box = 4;

    // *Move* the box, changing the ownership (and mutability)
    let mut mutable_box = immutable_box;

    println!("mutable_box contains {}", mutable_box);

    // Modify the contents of the box
    *mutable_box = 4;

    println!("mutable_box now contains {}", mutable_box);
}
```

<a id="section-scope-move-partial_move"></a>

<a id="section-scope-move-partial_move--partial-moves"></a>

### Partial moves

Within the [destructuring][section-scope-move-partial_move-ref-2] of a single variable, both `by-move` and
`by-reference` pattern bindings can be used at the same time. Doing
this will result in a _partial move_ of the variable, which means
that parts of the variable will be moved while other parts stay. In
such a case, the parent variable cannot be used afterwards as a
whole, however the parts that are only referenced (and not moved)
can still be used. Note that types that implement the
[`Drop` trait][section-scope-move-partial_move-ref-1] cannot be partially moved from, because
its `drop` method would use it afterwards as a whole.

```rust
fn main() {
    #[derive(Debug)]
    struct Person {
        name: String,
        age: Box<u8>,
    }

    // Error! cannot move out of a type which implements the `Drop` trait
    //impl Drop for Person {
    //    fn drop(&mut self) {
    //        println!("Dropping the person struct {:?}", self)
    //    }
    //}
    // TODO ^ Try uncommenting these lines

    let person = Person {
        name: String::from("Alice"),
        age: Box::new(20),
    };

    // `name` is moved out of person, but `age` is referenced
    let Person { name, ref age } = person;

    println!("The person's age is {}", age);

    println!("The person's name is {}", name);

    // Error! borrow of partially moved value: `person` partial move occurs
    //println!("The person struct is {:?}", person);

    // `person` cannot be used but `person.age` can be used as it is not moved
    println!("The person's age from person struct is {}", person.age);
}
```

(In this example, we store the `age` variable on the heap to
illustrate the partial move: deleting `ref` in the above code would
give an error as the ownership of `person.age` would be moved to the
variable `age`. If `Person.age` were stored on the stack, `ref` would
not be required as the definition of `age` would copy the data from
`person.age` without moving it.)

<a id="section-scope-move-partial_move--see-also"></a>

##### See also:

[destructuring][section-scope-move-partial_move-ref-2]

[section-scope-move-partial_move-ref-1]: 16-traits.md#section-trait-drop
[section-scope-move-partial_move-ref-2]: 08-flow-of-control.md#section-flow_control-match-destructuring

<a id="section-scope-borrow"></a>

<a id="section-scope-borrow--borrowing"></a>

## Borrowing

Most of the time, we'd like to access data without taking ownership over
it. To accomplish this, Rust uses a *borrowing* mechanism. Instead of
passing objects by value (`T`), objects can be passed by reference (`&T`).

The compiler statically guarantees (via its borrow checker) that references
*always* point to valid objects. That is, while references to an object
exist, the object cannot be destroyed.

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// This function takes ownership of a box and destroys it
fn eat_box_i32(boxed_i32: Box<i32>) {
    println!("Destroying box that contains {}", boxed_i32);
}

// This function borrows an i32
fn borrow_i32(borrowed_i32: &i32) {
    println!("This int is: {}", borrowed_i32);
}

fn main() {
    // Create a boxed i32 in the heap, and an i32 on the stack
    // Remember: numbers can have arbitrary underscores added for readability
    // 5_i32 is the same as 5i32
    let boxed_i32 = Box::new(5_i32);
    let stacked_i32 = 6_i32;

    // Borrow the contents of the box. Ownership is not taken,
    // so the contents can be borrowed again.
    borrow_i32(&boxed_i32);
    borrow_i32(&stacked_i32);

    {
        // Take a reference to the data contained inside the box
        let _ref_to_i32: &i32 = &boxed_i32;

        // Error!
        // Can't destroy `boxed_i32` while the inner value is borrowed later in scope.
        eat_box_i32(boxed_i32);
        // FIXME ^ Comment out this line

        // Attempt to borrow `_ref_to_i32` after inner value is destroyed
        borrow_i32(_ref_to_i32);
        // `_ref_to_i32` goes out of scope and is no longer borrowed.
    }

    // `boxed_i32` can now give up ownership to `eat_box_i32` and be destroyed
    eat_box_i32(boxed_i32);
}
```

<a id="section-scope-borrow-mut"></a>

<a id="section-scope-borrow-mut--mutability"></a>

### Mutability

Mutable data can be mutably borrowed using `&mut T`. This is called
a *mutable reference* and gives read/write access to the borrower.
In contrast, `&T` borrows the data via an immutable reference, and
the borrower can read the data but not modify it:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
#[allow(dead_code)]
#[derive(Clone, Copy)]
struct Book {
    // `&'static str` is a reference to a string allocated in read only memory
    author: &'static str,
    title: &'static str,
    year: u32,
}

// This function takes a reference to a book
fn borrow_book(book: &Book) {
    println!("I immutably borrowed {} - {} edition", book.title, book.year);
}

// This function takes a reference to a mutable book and changes `year` to 2014
fn new_edition(book: &mut Book) {
    book.year = 2014;
    println!("I mutably borrowed {} - {} edition", book.title, book.year);
}

fn main() {
    // Create an immutable Book named `immutabook`
    let immutabook = Book {
        // string literals have type `&'static str`
        author: "Douglas Hofstadter",
        title: "Gödel, Escher, Bach",
        year: 1979,
    };

    // Create a mutable copy of `immutabook` and call it `mutabook`
    let mut mutabook = immutabook;

    // Immutably borrow an immutable object
    borrow_book(&immutabook);

    // Immutably borrow a mutable object
    borrow_book(&mutabook);

    // Borrow a mutable object as mutable
    new_edition(&mut mutabook);

    // Error! Cannot borrow an immutable object as mutable
    new_edition(&mut immutabook);
    // FIXME ^ Comment out this line
}
```

<a id="section-scope-borrow-mut--see-also"></a>

##### See also:

[`static`][section-scope-borrow-mut-ref-1]

[section-scope-borrow-mut-ref-1]: #section-scope-lifetime-static_lifetime

<a id="section-scope-borrow-alias"></a>

<a id="section-scope-borrow-alias--aliasing"></a>

### Aliasing

Data can be immutably borrowed any number of times, but while immutably
borrowed, the original data can't be mutably borrowed. On the other hand, only
*one* mutable borrow is allowed at a time. The original data can be borrowed
again only *after* the mutable reference has been used for the last time.

```rust
struct Point { x: i32, y: i32, z: i32 }

fn main() {
    let mut point = Point { x: 0, y: 0, z: 0 };

    let borrowed_point = &point;
    let another_borrow = &point;

    // Data can be accessed via the references and the original owner
    println!("Point has coordinates: ({}, {}, {})",
                borrowed_point.x, another_borrow.y, point.z);

    // Error! Can't borrow `point` as mutable because it's currently
    // borrowed as immutable.
    // let mutable_borrow = &mut point;
    // TODO ^ Try uncommenting this line

    // The borrowed values are used again here
    println!("Point has coordinates: ({}, {}, {})",
                borrowed_point.x, another_borrow.y, point.z);

    // The immutable references are no longer used for the rest of the code so
    // it is possible to reborrow with a mutable reference.
    let mutable_borrow = &mut point;

    // Change data via mutable reference
    mutable_borrow.x = 5;
    mutable_borrow.y = 2;
    mutable_borrow.z = 1;

    // Error! Can't borrow `point` as immutable because it's currently
    // borrowed as mutable.
    // let y = &point.y;
    // TODO ^ Try uncommenting this line

    // Error! Can't print because `println!` takes an immutable reference.
    // println!("Point Z coordinate is {}", point.z);
    // TODO ^ Try uncommenting this line

    // Ok! Mutable references can be passed as immutable to `println!`
    println!("Point has coordinates: ({}, {}, {})",
                mutable_borrow.x, mutable_borrow.y, mutable_borrow.z);

    // The mutable reference is no longer used for the rest of the code so it
    // is possible to reborrow
    let new_borrowed_point = &point;
    println!("Point now has coordinates: ({}, {}, {})",
             new_borrowed_point.x, new_borrowed_point.y, new_borrowed_point.z);
}
```

<a id="section-scope-borrow-ref"></a>

<a id="section-scope-borrow-ref--the-ref-pattern"></a>

### The ref pattern

When doing pattern matching or destructuring via the `let` binding, the `ref`
keyword can be used to take references to the fields of a struct/tuple. The
example below shows a few instances where this can be useful:

```rust
#[derive(Clone, Copy)]
struct Point { x: i32, y: i32 }

fn main() {
    let c = 'Q';

    // A `ref` borrow on the left side of an assignment is equivalent to
    // an `&` borrow on the right side.
    let ref ref_c1 = c;
    let ref_c2 = &c;

    println!("ref_c1 equals ref_c2: {}", *ref_c1 == *ref_c2);

    let point = Point { x: 0, y: 0 };

    // `ref` is also valid when destructuring a struct.
    let _copy_of_x = {
        // `ref_to_x` is a reference to the `x` field of `point`.
        let Point { x: ref ref_to_x, y: _ } = point;

        // Return a copy of the `x` field of `point`.
        *ref_to_x
    };

    // A mutable copy of `point`
    let mut mutable_point = point;

    {
        // `ref` can be paired with `mut` to take mutable references.
        let Point { x: _, y: ref mut mut_ref_to_y } = mutable_point;

        // Mutate the `y` field of `mutable_point` via a mutable reference.
        *mut_ref_to_y = 1;
    }

    println!("point is ({}, {})", point.x, point.y);
    println!("mutable_point is ({}, {})", mutable_point.x, mutable_point.y);

    // A mutable tuple that includes a pointer
    let mut mutable_tuple = (Box::new(5u32), 3u32);

    {
        // Destructure `mutable_tuple` to change the value of `last`.
        let (_, ref mut last) = mutable_tuple;
        *last = 2u32;
    }

    println!("tuple is {:?}", mutable_tuple);
}
```

<a id="section-scope-lifetime"></a>

<a id="section-scope-lifetime--lifetimes"></a>

## Lifetimes

A *lifetime* is a construct the compiler (or more specifically, its *borrow
checker*) uses to ensure all borrows are valid. Specifically, a variable's
lifetime begins when it is created and ends when it is destroyed. While
lifetimes and scopes are often referred to together, they are not the same.

Take, for example, the case where we borrow a variable via `&`. The
borrow has a lifetime that is determined by where it is declared. As a result,
the borrow is valid as long as it ends before the lender is destroyed. However,
the scope of the borrow is determined by where the reference is used.

In the following example and in the rest of this section, we will see how
lifetimes relate to scopes, as well as how the two differ.

```rust
// Lifetimes are annotated below with lines denoting the creation
// and destruction of each variable.
// `i` has the longest lifetime because its scope entirely encloses
// both `borrow1` and `borrow2`. The duration of `borrow1` compared
// to `borrow2` is irrelevant since they are disjoint.
fn main() {
    let i = 3; // Lifetime for `i` starts. ────────────────┐
    //                                                     │
    { //                                                   │
        let borrow1 = &i; // `borrow1` lifetime starts. ──┐│
        //                                                ││
        println!("borrow1: {}", borrow1); //              ││
    } // `borrow1` ends. ─────────────────────────────────┘│
    //                                                     │
    //                                                     │
    { //                                                   │
        let borrow2 = &i; // `borrow2` lifetime starts. ──┐│
        //                                                ││
        println!("borrow2: {}", borrow2); //              ││
    } // `borrow2` ends. ─────────────────────────────────┘│
    //                                                     │
}   // Lifetime ends. ─────────────────────────────────────┘
```

Note that no names or types are assigned to label lifetimes.
This restricts how lifetimes will be able to be used as we will see.

<a id="section-scope-lifetime-explicit"></a>

<a id="section-scope-lifetime-explicit--explicit-annotation"></a>

### Explicit annotation

The borrow checker uses explicit lifetime annotations to determine
how long references should be valid. In cases where lifetimes are not
elided[^section-scope-lifetime-explicit-1], Rust requires explicit annotations to determine what the
lifetime of a reference should be. The syntax for explicitly annotating
a lifetime uses an apostrophe character as follows:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
foo<'a>
// `foo` has a lifetime parameter `'a`
```

Similar to [closures][section-scope-lifetime-explicit-ref-1], using lifetimes requires generics.
Additionally, this lifetime syntax indicates that the lifetime of `foo`
may not exceed that of `'a`. Explicit annotation of a type has the form
`&'a T` where `'a` has already been introduced.

In cases with multiple lifetimes, the syntax is similar:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
foo<'a, 'b>
// `foo` has lifetime parameters `'a` and `'b`
```

In this case, the lifetime of `foo` cannot exceed that of either `'a` *or* `'b`.

See the following example for explicit lifetime annotation in use:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// `print_refs` takes two references to `i32` which have different
// lifetimes `'a` and `'b`. These two lifetimes must both be at
// least as long as the function `print_refs`.
fn print_refs<'a, 'b>(x: &'a i32, y: &'b i32) {
    println!("x is {} and y is {}", x, y);
}

// A function which takes no arguments, but has a lifetime parameter `'a`.
fn failed_borrow<'a>() {
    let _x = 12;

    // ERROR: `_x` does not live long enough
    let _y: &'a i32 = &_x;
    // Attempting to use the lifetime `'a` as an explicit type annotation
    // inside the function will fail because the lifetime of `&_x` is shorter
    // than that of `_y`. A short lifetime cannot be coerced into a longer one.
}

fn main() {
    // Create variables to be borrowed below.
    let (four, nine) = (4, 9);

    // Borrows (`&`) of both variables are passed into the function.
    print_refs(&four, &nine);
    // Any input which is borrowed must outlive the borrower.
    // In other words, the lifetime of `four` and `nine` must
    // be longer than that of `print_refs`.

    failed_borrow();
    // `failed_borrow` contains no references to force `'a` to be
    // longer than the lifetime of the function, but `'a` is longer.
    // Because the lifetime is never constrained, it defaults to `'static`.
}
```

[^section-scope-lifetime-explicit-1]: [elision][section-scope-lifetime-explicit-ref-3] implicitly annotates lifetimes and so is different.

<a id="section-scope-lifetime-explicit--see-also"></a>

##### See also:

[generics][section-scope-lifetime-explicit-ref-4] and [closures][section-scope-lifetime-explicit-ref-2]

[section-scope-lifetime-explicit-ref-1]: 09-functions.md#section-fn-closures-anonymity
[section-scope-lifetime-explicit-ref-2]: 09-functions.md#section-fn-closures
[section-scope-lifetime-explicit-ref-3]: #section-scope-lifetime-elision
[section-scope-lifetime-explicit-ref-4]: 14-generics.md

<a id="section-scope-lifetime-fn"></a>

<a id="section-scope-lifetime-fn--functions"></a>

### Functions

Ignoring [elision][section-scope-lifetime-fn-ref-2], function signatures with lifetimes have a few constraints:

* any reference *must* have an annotated lifetime.
* any reference being returned *must* have the same lifetime as an input or
be `static`.

Additionally, note that returning references without input is banned if it
would result in returning references to invalid data. The following example shows
off some valid forms of functions with lifetimes:

```rust
// One input reference with lifetime `'a` which must live
// at least as long as the function.
fn print_one<'a>(x: &'a i32) {
    println!("`print_one`: x is {}", x);
}

// Mutable references are possible with lifetimes as well.
fn add_one<'a>(x: &'a mut i32) {
    *x += 1;
}

// Multiple elements with different lifetimes. In this case, it
// would be fine for both to have the same lifetime `'a`, but
// in more complex cases, different lifetimes may be required.
fn print_multi<'a, 'b>(x: &'a i32, y: &'b i32) {
    println!("`print_multi`: x is {}, y is {}", x, y);
}

// Returning references that have been passed in is acceptable.
// However, the correct lifetime must be returned.
fn pass_x<'a, 'b>(x: &'a i32, _: &'b i32) -> &'a i32 { x }

//fn invalid_output<'a>() -> &'a String { &String::from("foo") }
// The above is invalid: `'a` must live longer than the function.
// Here, `&String::from("foo")` would create a `String`, followed by a
// reference. Then the data is dropped upon exiting the scope, leaving
// a reference to invalid data to be returned.

fn main() {
    let x = 7;
    let y = 9;

    print_one(&x);
    print_multi(&x, &y);

    let z = pass_x(&x, &y);
    print_one(z);

    let mut t = 3;
    add_one(&mut t);
    print_one(&t);
}
```

<a id="section-scope-lifetime-fn--see-also"></a>

##### See also:

[Functions][section-scope-lifetime-fn-ref-1]

[section-scope-lifetime-fn-ref-1]: 09-functions.md

[section-scope-lifetime-fn-ref-2]: #section-scope-lifetime-elision

<a id="section-scope-lifetime-methods"></a>

<a id="section-scope-lifetime-methods--methods"></a>

### Methods

Methods are annotated similarly to functions:

```rust
struct Owner(i32);

impl Owner {
    // Annotate lifetimes as in a standalone function.
    fn add_one<'a>(&'a mut self) { self.0 += 1; }
    fn print<'a>(&'a self) {
        println!("`print`: {}", self.0);
    }
}

fn main() {
    let mut owner = Owner(18);

    owner.add_one();
    owner.print();
}
```

<a id="section-scope-lifetime-methods--see-also"></a>

##### See also:

[methods][section-scope-lifetime-methods-ref-1]

[section-scope-lifetime-methods-ref-1]: 09-functions.md#section-fn-methods

<a id="section-scope-lifetime-struct"></a>

<a id="section-scope-lifetime-struct--structs"></a>

### Structs

Annotation of lifetimes in structures are also similar to functions:

```rust
// A type `Borrowed` which houses a reference to an
// `i32`. The reference to `i32` must outlive `Borrowed`.
#[derive(Debug)]
struct Borrowed<'a>(&'a i32);

// Similarly, both references here must outlive this structure.
#[derive(Debug)]
struct NamedBorrowed<'a> {
    x: &'a i32,
    y: &'a i32,
}

// An enum which is either an `i32` or a reference to one.
#[derive(Debug)]
enum Either<'a> {
    Num(i32),
    Ref(&'a i32),
}

fn main() {
    let x = 18;
    let y = 15;

    let single = Borrowed(&x);
    let double = NamedBorrowed { x: &x, y: &y };
    let reference = Either::Ref(&x);
    let number    = Either::Num(y);

    println!("x is borrowed in {:?}", single);
    println!("x and y are borrowed in {:?}", double);
    println!("x is borrowed in {:?}", reference);
    println!("y is *not* borrowed in {:?}", number);
}
```

<a id="section-scope-lifetime-struct--see-also"></a>

##### See also:

[`struct`s][section-scope-lifetime-struct-ref-1]

[section-scope-lifetime-struct-ref-1]: 03-custom-types.md#section-custom_types-structs

<a id="section-scope-lifetime-trait"></a>

<a id="section-scope-lifetime-trait--traits"></a>

### Traits

Annotation of lifetimes in trait methods basically are similar to functions.
Note that `impl` may have annotation of lifetimes too.

```rust
// A struct with annotation of lifetimes.
#[derive(Debug)]
struct Borrowed<'a> {
    x: &'a i32,
}

// Annotate lifetimes to impl.
impl<'a> Default for Borrowed<'a> {
    fn default() -> Self {
        Self {
            x: &10,
        }
    }
}

fn main() {
    let b: Borrowed = Default::default();
    println!("b is {:?}", b);
}
```

<a id="section-scope-lifetime-trait--see-also"></a>

##### See also:

[`trait`s][section-scope-lifetime-trait-ref-1]

[section-scope-lifetime-trait-ref-1]: 16-traits.md

<a id="section-scope-lifetime-lifetime_bounds"></a>

<a id="section-scope-lifetime-lifetime_bounds--bounds"></a>

### Bounds

Just like generic types can be bounded, lifetimes (themselves generic)
use bounds as well. The `:` character has a slightly different meaning here,
but `+` is the same. Note how the following read:

1. `T: 'a`: *All* references in `T` must outlive lifetime `'a`.
2. `T: Trait + 'a`: Type `T` must implement trait `Trait` and *all* references
in `T` must outlive `'a`.

The example below shows the above syntax in action used after keyword `where`:

```rust
use std::fmt::Debug; // Trait to bound with.

#[derive(Debug)]
struct Ref<'a, T: 'a>(&'a T);
// `Ref` contains a reference to a generic type `T` that has
// some lifetime `'a` unknown by `Ref`. `T` is bounded such that any
// *references* in `T` must outlive `'a`. Additionally, the lifetime
// of `Ref` may not exceed `'a`.

// A generic function which prints using the `Debug` trait.
fn print<T>(t: T) where
    T: Debug {
    println!("`print`: t is {:?}", t);
}

// Here a reference to `T` is taken where `T` implements
// `Debug` and all *references* in `T` outlive `'a`. In
// addition, `'a` must outlive the function.
fn print_ref<'a, T>(t: &'a T) where
    T: Debug + 'a {
    println!("`print_ref`: t is {:?}", t);
}

fn main() {
    let x = 7;
    let ref_x = Ref(&x);

    print_ref(&ref_x);
    print(ref_x);
}
```

<a id="section-scope-lifetime-lifetime_bounds--see-also"></a>

##### See also:

[generics][section-scope-lifetime-lifetime_bounds-ref-1], [bounds in generics][section-scope-lifetime-lifetime_bounds-ref-2], and
[multiple bounds in generics][section-scope-lifetime-lifetime_bounds-ref-3]

[section-scope-lifetime-lifetime_bounds-ref-1]: 14-generics.md
[section-scope-lifetime-lifetime_bounds-ref-2]: 14-generics.md#section-generics-bounds
[section-scope-lifetime-lifetime_bounds-ref-3]: 14-generics.md#section-generics-multi_bounds

<a id="section-scope-lifetime-lifetime_coercion"></a>

<a id="section-scope-lifetime-lifetime_coercion--coercion"></a>

### Coercion

A longer lifetime can be coerced into a shorter one
so that it works inside a scope it normally wouldn't work in.
This comes in the form of inferred coercion by the Rust compiler,
and also in the form of declaring a lifetime difference:

```rust
// Here, Rust infers a lifetime that is as short as possible.
// The two references are then coerced to that lifetime.
fn multiply<'a>(first: &'a i32, second: &'a i32) -> i32 {
    first * second
}

// `<'a: 'b, 'b>` reads as lifetime `'a` is at least as long as `'b`.
// Here, we take in an `&'a i32` and return a `&'b i32` as a result of coercion.
fn choose_first<'a: 'b, 'b>(first: &'a i32, _: &'b i32) -> &'b i32 {
    first
}

fn main() {
    let first = 2; // Longer lifetime

    {
        let second = 3; // Shorter lifetime

        println!("The product is {}", multiply(&first, &second));
        println!("{} is the first", choose_first(&first, &second));
    };
}
```

<a id="section-scope-lifetime-static_lifetime"></a>

<a id="section-scope-lifetime-static_lifetime--static"></a>

### Static

Rust has a few reserved lifetime names. One of those is `'static`. You
might encounter it in two situations:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
// A reference with 'static lifetime:
let s: &'static str = "hello world";

// 'static as part of a trait bound:
fn generic<T>(x: T) where T: 'static {}
```

Both are related but subtly different and this is a common source for
confusion when learning Rust. Here are some examples for each situation:

<a id="section-scope-lifetime-static_lifetime--reference-lifetime"></a>

#### Reference lifetime

As a reference lifetime `'static` indicates that the data pointed to by
the reference lives for the remaining lifetime of the running program.
It can still be coerced to a shorter lifetime.

There are two common ways to make a variable with `'static` lifetime, and both
are stored in the read-only memory of the binary:

* Make a constant with the `static` declaration.
* Make a `string` literal which has type: `&'static str`.

See the following example for a display of each method:

```rust
// Make a constant with `'static` lifetime.
static NUM: i32 = 18;

// Returns a reference to `NUM` where its `'static`
// lifetime is coerced to that of the input argument.
fn coerce_static<'a>(_: &'a i32) -> &'a i32 {
    &NUM
}

fn main() {
    {
        // Make a `string` literal and print it:
        let static_string = "I'm in read-only memory";
        println!("static_string: {}", static_string);

        // When `static_string` goes out of scope, the reference
        // can no longer be used, but the data remains in the binary.
    }

    {
        // Make an integer to use for `coerce_static`:
        let lifetime_num = 9;

        // Coerce `NUM` to lifetime of `lifetime_num`:
        let coerced_static = coerce_static(&lifetime_num);

        println!("coerced_static: {}", coerced_static);
    }

    println!("NUM: {} stays accessible!", NUM);
}
```

Since `'static` references only need to be valid for the _remainder_ of
a program's life, they can be created while the program is executed. Just to
demonstrate, the below example uses
[`Box::leak`](https://doc.rust-lang.org/std/boxed/struct.Box.html#method.leak)
to dynamically create `'static` references. In that case it definitely doesn't
live for the entire duration, but only from the leaking point onward.

> **Example note:** This example intentionally does not compile.

```rust
extern crate rand;
use rand::Fill;

fn random_vec() -> &'static [u64; 100] {
    let mut rng = rand::rng();
    let mut boxed = Box::new([0; 100]);
    boxed.fill(&mut rng);
    Box::leak(boxed)
}

fn main() {
    let first: &'static [u64; 100] = random_vec();
    let second: &'static [u64; 100] = random_vec();
    assert_ne!(first, second)
}
```

<a id="section-scope-lifetime-static_lifetime--trait-bound"></a>

#### Trait bound

As a trait bound, it means the type does not contain any non-static
references. Eg. the receiver can hold on to the type for as long as
they want and it will never become invalid until they drop it.

It's important to understand this means that any owned data always passes
a `'static` lifetime bound, but a reference to that owned data generally
does not:

> **Example note:** This example intentionally does not compile.

```rust
use std::fmt::Debug;

fn print_it(input: impl Debug + 'static) {
    println!("'static value passed in is: {:?}", input);
}

fn main() {
    // i is owned and contains no references, thus it's 'static:
    let i = 5;
    print_it(i);

    // oops, &i only has the lifetime defined by the scope of
    // main(), so it's not 'static:
    print_it(&i);
}
```

The compiler will tell you:

> **Example note:** Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.

```rust
error[E0597]: `i` does not live long enough
  --> src/lib.rs:15:15
   |
15 |     print_it(&i);
   |     ---------^^--
   |     |         |
   |     |         borrowed value does not live long enough
   |     argument requires that `i` is borrowed for `'static`
16 | }
   | - `i` dropped here while still borrowed
```

<a id="section-scope-lifetime-static_lifetime--see-also"></a>

##### See also:

[`'static` constants][section-scope-lifetime-static_lifetime-ref-1]

[section-scope-lifetime-static_lifetime-ref-1]: 03-custom-types.md#section-custom_types-constants

<a id="section-scope-lifetime-elision"></a>

<a id="section-scope-lifetime-elision--elision"></a>

### Elision

Some lifetime patterns are overwhelmingly common and so the borrow checker
will allow you to omit them to save typing and to improve readability.
This is known as elision. Elision exists in Rust solely because these patterns
are common.

The following code shows a few examples of elision. For a more comprehensive
description of elision, see [lifetime elision][section-scope-lifetime-elision-ref-1] in the book.

```rust
// `elided_input` and `annotated_input` essentially have identical signatures
// because the lifetime of `elided_input` is inferred by the compiler:
fn elided_input(x: &i32) {
    println!("`elided_input`: {}", x);
}

fn annotated_input<'a>(x: &'a i32) {
    println!("`annotated_input`: {}", x);
}

// Similarly, `elided_pass` and `annotated_pass` have identical signatures
// because the lifetime is added implicitly to `elided_pass`:
fn elided_pass(x: &i32) -> &i32 { x }

fn annotated_pass<'a>(x: &'a i32) -> &'a i32 { x }

fn main() {
    let x = 3;

    elided_input(&x);
    annotated_input(&x);

    println!("`elided_pass`: {}", elided_pass(&x));
    println!("`annotated_pass`: {}", annotated_pass(&x));
}
```

<a id="section-scope-lifetime-elision--see-also"></a>

##### See also:

[elision][section-scope-lifetime-elision-ref-1]

[section-scope-lifetime-elision-ref-1]: https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html#lifetime-elision
