<a id="section-trait"></a>

<a id="section-trait--traits"></a>

# Traits

[Chapter index](SUMMARY.md)

**In this chapter**

- [Derive](#section-trait-derive)
- [Returning Traits with `dyn`](#section-trait-dyn)
- [Operator Overloading](#section-trait-ops)
- [Drop](#section-trait-drop)
- [Iterators](#section-trait-iter)
- [`impl Trait`](#section-trait-impl_trait)
- [Clone](#section-trait-clone)
- [Supertraits](#section-trait-supertraits)
- [Disambiguating overlapping traits](#section-trait-disambiguating)


A `trait` is a collection of methods defined for an unknown type:
`Self`. They can access other methods declared in the same trait.

Traits can be implemented for any data type. In the example below,
we define `Animal`, a group of methods. The `Animal` `trait` is
then implemented for the `Sheep` data type, allowing the use of
methods from `Animal` with a `Sheep`.

```rust
struct Sheep { naked: bool, name: &'static str }

trait Animal {
    // Associated function signature; `Self` refers to the implementor type.
    fn new(name: &'static str) -> Self;

    // Method signatures; these will return a string.
    fn name(&self) -> &'static str;
    fn noise(&self) -> &'static str;

    // Traits can provide default method definitions.
    fn talk(&self) {
        println!("{} says {}", self.name(), self.noise());
    }
}

impl Sheep {
    fn is_naked(&self) -> bool {
        self.naked
    }

    fn shear(&mut self) {
        if self.is_naked() {
            // Implementor methods can use the implementor's trait methods.
            println!("{} is already naked...", self.name());
        } else {
            println!("{} gets a haircut!", self.name);

            self.naked = true;
        }
    }
}

// Implement the `Animal` trait for `Sheep`.
impl Animal for Sheep {
    // `Self` is the implementor type: `Sheep`.
    fn new(name: &'static str) -> Sheep {
        Sheep { name: name, naked: false }
    }

    fn name(&self) -> &'static str {
        self.name
    }

    fn noise(&self) -> &'static str {
        if self.is_naked() {
            "baaaaah?"
        } else {
            "baaaaah!"
        }
    }

    // Default trait methods can be overridden.
    fn talk(&self) {
        // For example, we can add some quiet contemplation.
        println!("{} pauses briefly... {}", self.name, self.noise());
    }
}

fn main() {
    // Type annotation is necessary in this case.
    let mut dolly: Sheep = Animal::new("Dolly");
    // TODO ^ Try removing the type annotations.

    dolly.talk();
    dolly.shear();
    dolly.talk();
}
```

<a id="section-trait-derive"></a>

<a id="section-trait-derive--derive"></a>

## Derive

The compiler is capable of providing basic implementations for some traits via
the `#[derive]` [attribute][section-trait-derive-ref-1]. These traits can still be
manually implemented if a more complex behavior is required.

The following is a list of derivable traits:

* Comparison traits:
  [`Eq`][section-trait-derive-ref-2], [`PartialEq`][section-trait-derive-ref-3], [`Ord`][section-trait-derive-ref-4], [`PartialOrd`][section-trait-derive-ref-5].
* [`Clone`][section-trait-derive-ref-6], to create `T` from `&T` via a copy.
* [`Copy`][section-trait-derive-ref-7], to give a type 'copy semantics' instead of 'move semantics'.
* [`Hash`][section-trait-derive-ref-8], to compute a hash from `&T`.
* [`Default`][section-trait-derive-ref-9], to create an empty instance of a data type.
* [`Debug`][section-trait-derive-ref-10], to format a value using the `{:?}` formatter.

```rust
// `Centimeters`, a tuple struct that can be compared
#[derive(PartialEq, PartialOrd)]
struct Centimeters(f64);

// `Inches`, a tuple struct that can be printed
#[derive(Debug)]
struct Inches(i32);

impl Inches {
    fn to_centimeters(&self) -> Centimeters {
        let &Inches(inches) = self;

        Centimeters(inches as f64 * 2.54)
    }
}

// `Seconds`, a tuple struct with no additional attributes
struct Seconds(i32);

fn main() {
    let _one_second = Seconds(1);

    // Error: `Seconds` can't be printed; it doesn't implement the `Debug` trait
    //println!("One second looks like: {:?}", _one_second);
    // TODO ^ Try uncommenting this line

    // Error: `Seconds` can't be compared; it doesn't implement the `PartialEq` trait
    //let _this_is_true = (_one_second == _one_second);
    // TODO ^ Try uncommenting this line

    let foot = Inches(12);

    println!("One foot equals {:?}", foot);

    let meter = Centimeters(100.0);

    let cmp =
        if foot.to_centimeters() < meter {
            "smaller"
        } else {
            "bigger"
        };

    println!("One foot is {} than one meter.", cmp);
}
```

<a id="section-trait-derive--see-also"></a>

#### See also:

[`derive`][section-trait-derive-ref-11]

[section-trait-derive-ref-1]: 13-attributes.md
[section-trait-derive-ref-2]: https://doc.rust-lang.org/std/cmp/trait.Eq.html
[section-trait-derive-ref-3]: https://doc.rust-lang.org/std/cmp/trait.PartialEq.html
[section-trait-derive-ref-4]: https://doc.rust-lang.org/std/cmp/trait.Ord.html
[section-trait-derive-ref-5]: https://doc.rust-lang.org/std/cmp/trait.PartialOrd.html
[section-trait-derive-ref-6]: https://doc.rust-lang.org/std/clone/trait.Clone.html
[section-trait-derive-ref-7]: https://doc.rust-lang.org/core/marker/trait.Copy.html
[section-trait-derive-ref-8]: https://doc.rust-lang.org/std/hash/trait.Hash.html
[section-trait-derive-ref-9]: https://doc.rust-lang.org/std/default/trait.Default.html
[section-trait-derive-ref-10]: https://doc.rust-lang.org/std/fmt/trait.Debug.html
[section-trait-derive-ref-11]: https://doc.rust-lang.org/reference/attributes.html#derive

<a id="section-trait-dyn"></a>

<a id="section-trait-dyn--returning-traits-with-dyn"></a>

## Returning Traits with `dyn`

The Rust compiler needs to know how much space every function's return type requires. This means all
your functions have to return a concrete type. Unlike other languages, if you have a trait like
`Animal`, you can't write a function that returns `Animal`, because its different implementations
will need different amounts of memory.

However, there's an easy workaround. Instead of returning a trait object directly, our functions
return a `Box` which _contains_ some `Animal`. A `box` is just a reference to some memory in the
heap. Because a reference has a statically-known size, and the compiler can guarantee it points to a
heap-allocated `Animal`, we can return a trait from our function!

Rust tries to be as explicit as possible whenever it allocates memory on the heap. So if your
function returns a pointer-to-trait-on-heap in this way, you need to write the return type with the
`dyn` keyword, e.g. `Box<dyn Animal>`.

```rust
struct Sheep {}
struct Cow {}

trait Animal {
    // Instance method signature
    fn noise(&self) -> &'static str;
}

// Implement the `Animal` trait for `Sheep`.
impl Animal for Sheep {
    fn noise(&self) -> &'static str {
        "baaaaah!"
    }
}

// Implement the `Animal` trait for `Cow`.
impl Animal for Cow {
    fn noise(&self) -> &'static str {
        "moooooo!"
    }
}

// Returns some struct that implements Animal, but we don't know which one at compile time.
fn random_animal(random_number: f64) -> Box<dyn Animal> {
    if random_number < 0.5 {
        Box::new(Sheep {})
    } else {
        Box::new(Cow {})
    }
}

fn main() {
    let random_number = 0.234;
    let animal = random_animal(random_number);
    println!("You've randomly chosen an animal, and it says {}", animal.noise());
}

```

<a id="section-trait-ops"></a>

<a id="section-trait-ops--operator-overloading"></a>

## Operator Overloading

In Rust, many of the operators can be overloaded via traits. That is, some operators can
be used to accomplish different tasks based on their input arguments. This is possible
because operators are syntactic sugar for method calls. For example, the `+` operator in
`a + b` calls the `add` method (as in `a.add(b)`). This `add` method is part of the `Add`
trait. Hence, the `+` operator can be used by any implementor of the `Add` trait.

A list of the traits, such as `Add`, that overload operators can be found in [`core::ops`][section-trait-ops-ref-2].

```rust
use std::ops;

struct Foo;
struct Bar;

#[derive(Debug)]
struct FooBar;

#[derive(Debug)]
struct BarFoo;

// The `std::ops::Add` trait is used to specify the functionality of `+`.
// Here, we make `Add<Bar>` - the trait for addition with a RHS of type `Bar`.
// The following block implements the operation: Foo + Bar = FooBar
impl ops::Add<Bar> for Foo {
    type Output = FooBar;

    fn add(self, _rhs: Bar) -> FooBar {
        println!("> Foo.add(Bar) was called");

        FooBar
    }
}

// By reversing the types, we end up implementing non-commutative addition.
// Here, we make `Add<Foo>` - the trait for addition with a RHS of type `Foo`.
// This block implements the operation: Bar + Foo = BarFoo
impl ops::Add<Foo> for Bar {
    type Output = BarFoo;

    fn add(self, _rhs: Foo) -> BarFoo {
        println!("> Bar.add(Foo) was called");

        BarFoo
    }
}

fn main() {
    println!("Foo + Bar = {:?}", Foo + Bar);
    println!("Bar + Foo = {:?}", Bar + Foo);
}
```

<a id="section-trait-ops--see-also"></a>

#### See Also

[Add][section-trait-ops-ref-1], [Syntax Index][section-trait-ops-ref-3]

[section-trait-ops-ref-1]: https://doc.rust-lang.org/core/ops/trait.Add.html
[section-trait-ops-ref-2]: https://doc.rust-lang.org/core/ops/
[section-trait-ops-ref-3]:https://doc.rust-lang.org/book/appendix-02-operators.html

<a id="section-trait-drop"></a>

<a id="section-trait-drop--drop"></a>

## Drop

The [`Drop`][section-trait-drop-ref-1] trait only has one method: `drop`, which is called automatically
when an object goes out of scope. The main use of the `Drop` trait is to free the
resources that the implementor instance owns.

`Box`, `Vec`, `String`, `File`, and `Process` are some examples of types that
implement the `Drop` trait to free resources. The `Drop` trait can also be
manually implemented for any custom data type.

The following example adds a print to console to the `drop` function to announce
when it is called.

```rust
struct Droppable {
    name: &'static str,
}

// This trivial implementation of `drop` adds a print to console.
impl Drop for Droppable {
    fn drop(&mut self) {
        println!("> Dropping {}", self.name);
    }
}

fn main() {
    let _a = Droppable { name: "a" };

    // block A
    {
        let _b = Droppable { name: "b" };

        // block B
        {
            let _c = Droppable { name: "c" };
            let _d = Droppable { name: "d" };

            println!("Exiting block B");
        }
        println!("Just exited block B");

        println!("Exiting block A");
    }
    println!("Just exited block A");

    // Variable can be manually dropped using the `drop` function
    drop(_a);
    // TODO ^ Try commenting this line

    println!("end of the main function");

    // `_a` *won't* be `drop`ed again here, because it already has been
    // (manually) `drop`ed
}
```

For a more practical example, here's how the `Drop` trait can be used to automatically
clean up temporary files when they're no longer needed:

```rust
use std::fs::File;
use std::path::PathBuf;

struct TempFile {
    file: File,
    path: PathBuf,
}

impl TempFile {
    fn new(path: PathBuf) -> std::io::Result<Self> {
        // Note: File::create() will overwrite existing files
        let file = File::create(&path)?;

        Ok(Self { file, path })
    }
}

// When TempFile is dropped:
// 1. First, our custom drop implementation runs. The file is still open at this point,
//    but we can remove it from the filesystem by path.
// 2. Then, after our drop returns, Rust automatically drops each field,
//    so File's drop runs and closes the file handle.
impl Drop for TempFile {
    fn drop(&mut self) {
        // Note: the File is still open here — field destructors run after this method.
        if let Err(e) = std::fs::remove_file(&self.path) {
            eprintln!("Failed to remove temporary file: {}", e);
        }
        println!("> Dropped temporary file: {:?}", self.path);
        // After this method returns, Rust will drop each field (including `file`),
        // which closes the underlying file handle.
    }
}

fn main() -> std::io::Result<()> {
    // Create a new scope to demonstrate drop behavior
    {
        let temp = TempFile::new("test.txt".into())?;
        println!("Temporary file created");
        // File will be automatically cleaned up when temp goes out of scope
    }
    println!("End of scope - file should be cleaned up");

    // We can also manually drop if needed
    let temp2 = TempFile::new("another_test.txt".into())?;
    drop(temp2); // Explicitly drop the file
    println!("Manually dropped file");

    Ok(())
}
```

[section-trait-drop-ref-1]: https://doc.rust-lang.org/std/ops/trait.Drop.html

<a id="section-trait-iter"></a>

<a id="section-trait-iter--iterators"></a>

## Iterators

The [`Iterator`][section-trait-iter-ref-2] trait is used to implement iterators over collections
such as arrays.

The trait requires only a method to be defined for the `next` element,
which may be manually defined in an `impl` block or automatically
defined (as in arrays and ranges).

As a point of convenience for common situations, the `for` construct
turns some collections into iterators using the [`.into_iter()`][section-trait-iter-ref-1] method.

```rust
struct Fibonacci {
    curr: u32,
    next: u32,
}

// Implement `Iterator` for `Fibonacci`.
// The `Iterator` trait only requires a method to be defined for the `next` element,
// and an `associated type` to declare the return type of the iterator.
impl Iterator for Fibonacci {
    // We can refer to this type using Self::Item
    type Item = u32;

    // Here, we define the sequence using `.curr` and `.next`.
    // The return type is `Option<T>`:
    //     * When the `Iterator` is finished, `None` is returned.
    //     * Otherwise, the next value is wrapped in `Some` and returned.
    // We use Self::Item in the return type, so we can change
    // the type without having to update the function signatures.
    fn next(&mut self) -> Option<Self::Item> {
        let current = self.curr;

        self.curr = self.next;
        self.next = current + self.next;

        // Since there's no endpoint to a Fibonacci sequence, the `Iterator`
        // will never return `None`, and `Some` is always returned.
        Some(current)
    }
}

// Returns a Fibonacci sequence generator
fn fibonacci() -> Fibonacci {
    Fibonacci { curr: 0, next: 1 }
}

fn main() {
    // `0..3` is an `Iterator` that generates: 0, 1, and 2.
    let mut sequence = 0..3;

    println!("Four consecutive `next` calls on 0..3");
    println!("> {:?}", sequence.next());
    println!("> {:?}", sequence.next());
    println!("> {:?}", sequence.next());
    println!("> {:?}", sequence.next());

    // `for` works through an `Iterator` until it returns `None`.
    // Each `Some` value is unwrapped and bound to a variable (here, `i`).
    println!("Iterate through 0..3 using `for`");
    for i in 0..3 {
        println!("> {}", i);
    }

    // The `take(n)` method reduces an `Iterator` to its first `n` terms.
    println!("The first four terms of the Fibonacci sequence are: ");
    for i in fibonacci().take(4) {
        println!("> {}", i);
    }

    // The `skip(n)` method shortens an `Iterator` by dropping its first `n` terms.
    println!("The next four terms of the Fibonacci sequence are: ");
    for i in fibonacci().skip(4).take(4) {
        println!("> {}", i);
    }

    let array = [1u32, 3, 3, 7];

    // The `iter` method produces an `Iterator` over an array/slice.
    println!("Iterate the following array {:?}", &array);
    for i in array.iter() {
        println!("> {}", i);
    }
}
```

[section-trait-iter-ref-1]: https://doc.rust-lang.org/std/iter/trait.IntoIterator.html
[section-trait-iter-ref-2]: https://doc.rust-lang.org/core/iter/trait.Iterator.html

<a id="section-trait-impl_trait"></a>

<a id="section-trait-impl_trait--impl-trait"></a>

## `impl Trait`

`impl Trait` can be used in two locations:

1. as an argument type
2. as a return type

<a id="section-trait-impl_trait--as-an-argument-type"></a>

### As an argument type

If your function is generic over a trait but you don't mind the specific type, you can simplify the function declaration using `impl Trait` as the type of the argument.

For example, consider the following code:

```rust
fn parse_csv_document<R: std::io::BufRead>(src: R) -> std::io::Result<Vec<Vec<String>>> {
    src.lines()
        .map(|line| {
            // For each line in the source
            line.map(|line| {
                // If the line was read successfully, process it, if not, return the error
                line.split(',') // Split the line separated by commas
                    .map(|entry| String::from(entry.trim())) // Remove leading and trailing whitespace
                    .collect() // Collect all strings in a row into a Vec<String>
            })
        })
        .collect() // Collect all lines into a Vec<Vec<String>>
}
```

`parse_csv_document` is generic, allowing it to take any type which implements BufRead, such as `BufReader<File>` or `[u8]`,
but it's not important what type `R` is, and `R` is only used to declare the type of `src`, so the function can also be written as:

```rust
fn parse_csv_document(src: impl std::io::BufRead) -> std::io::Result<Vec<Vec<String>>> {
    src.lines()
        .map(|line| {
            // For each line in the source
            line.map(|line| {
                // If the line was read successfully, process it, if not, return the error
                line.split(',') // Split the line separated by commas
                    .map(|entry| String::from(entry.trim())) // Remove leading and trailing whitespace
                    .collect() // Collect all strings in a row into a Vec<String>
            })
        })
        .collect() // Collect all lines into a Vec<Vec<String>>
}
```

Note that using `impl Trait` as an argument type means that you cannot explicitly state what form of the function you use, i.e. `parse_csv_document::<std::io::Empty>(std::io::empty())` will not work with the second example.

<a id="section-trait-impl_trait--as-a-return-type"></a>

### As a return type

If your function returns a type that implements `MyTrait`, you can write its
return type as `-> impl MyTrait`. This can help simplify your type signatures quite a lot!

```rust
use std::iter;
use std::vec::IntoIter;

// This function combines two `Vec<i32>` and returns an iterator over it.
// Look how complicated its return type is!
fn combine_vecs_explicit_return_type(
    v: Vec<i32>,
    u: Vec<i32>,
) -> iter::Cycle<iter::Chain<IntoIter<i32>, IntoIter<i32>>> {
    v.into_iter().chain(u.into_iter()).cycle()
}

// This is the exact same function, but its return type uses `impl Trait`.
// Look how much simpler it is!
fn combine_vecs(
    v: Vec<i32>,
    u: Vec<i32>,
) -> impl Iterator<Item=i32> {
    v.into_iter().chain(u.into_iter()).cycle()
}

fn main() {
    let v1 = vec![1, 2, 3];
    let v2 = vec![4, 5];
    let mut v3 = combine_vecs(v1, v2);
    assert_eq!(Some(1), v3.next());
    assert_eq!(Some(2), v3.next());
    assert_eq!(Some(3), v3.next());
    assert_eq!(Some(4), v3.next());
    assert_eq!(Some(5), v3.next());
    println!("all done");
}
```

More importantly, some Rust types can't be written out. For example, every
closure has its own unnamed concrete type. Before `impl Trait` syntax, you had
to allocate on the heap in order to return a closure. But now you can do it all
statically, like this:

```rust
// Returns a function that adds `y` to its input
fn make_adder_function(y: i32) -> impl Fn(i32) -> i32 {
    let closure = move |x: i32| { x + y };
    closure
}

fn main() {
    let plus_one = make_adder_function(1);
    assert_eq!(plus_one(2), 3);
}
```

You can also use `impl Trait` to return an iterator that uses `map` or `filter`
closures! This makes using `map` and `filter` easier. Because closure types don't
have names, you can't write out an explicit return type if your function returns
iterators with closures. But with `impl Trait` you can do this easily:

```rust
fn double_positives<'a>(numbers: &'a Vec<i32>) -> impl Iterator<Item = i32> + 'a {
    numbers
        .iter()
        .filter(|x| x > &&0)
        .map(|x| x * 2)
}

fn main() {
    let singles = vec![-3, -2, 2, 3];
    let doubles = double_positives(&singles);
    assert_eq!(doubles.collect::<Vec<i32>>(), vec![4, 6]);
}
```

<a id="section-trait-clone"></a>

<a id="section-trait-clone--clone-and-copy"></a>

## Clone and Copy

When dealing with resources, the default behavior is to transfer them during
assignments or function calls. However, sometimes we need to make a
copy of the resource as well.

The [`Clone`][section-trait-clone-ref-1] trait helps us do exactly this. Most commonly, we can
use the `.clone()` method defined by the `Clone` trait.

<a id="section-trait-clone--copy-implicit-cloning"></a>

### Copy: Implicit Cloning

The [`Copy`][section-trait-clone-ref-2] trait allows a type to be duplicated simply by copying bits,
with no additional logic required. When a type implements `Copy`, assignments
and function calls will implicitly copy the value instead of moving it.

**Important:** `Copy` requires `Clone` - any type that implements `Copy` must
also implement `Clone`. This is because `Copy` is defined as a subtrait:
`trait Copy: Clone {}`. The `Clone` implementation for `Copy` types simply
copies the bits.

Not all types can implement `Copy`. A type can only be `Copy` if:
- All of its components are `Copy`
- It doesn't manage external resources (like heap memory, file handles, etc.)

```rust
// A unit struct without resources
// Note: Copy requires Clone, so we must derive both
#[derive(Debug, Clone, Copy)]
struct Unit;

// A tuple struct with resources that implements the `Clone` trait
// This CANNOT be Copy because Box<T> is not Copy
#[derive(Clone, Debug)]
struct Pair(Box<i32>, Box<i32>);

fn main() {
    // Instantiate `Unit`
    let unit = Unit;
    // Copy `Unit` - this is an implicit copy, not a move!
    // Because Unit implements Copy, the value is duplicated automatically
    let copied_unit = unit;

    // Both `Unit`s can be used independently
    println!("original: {:?}", unit);
    println!("copy: {:?}", copied_unit);

    // Instantiate `Pair`
    let pair = Pair(Box::new(1), Box::new(2));
    println!("original: {:?}", pair);

    // Move `pair` into `moved_pair`, moves resources
    // Pair does not implement Copy, so this is a move
    let moved_pair = pair;
    println!("moved: {:?}", moved_pair);

    // Error! `pair` has lost its resources
    //println!("original: {:?}", pair);
    // TODO ^ Try uncommenting this line

    // Clone `moved_pair` into `cloned_pair` (resources are included)
    // Unlike Copy, Clone is explicit - we must call .clone()
    let cloned_pair = moved_pair.clone();
    // Drop the moved original pair using std::mem::drop
    drop(moved_pair);

    // Error! `moved_pair` has been dropped
    //println!("moved and dropped: {:?}", moved_pair);
    // TODO ^ Try uncommenting this line

    // The result from .clone() can still be used!
    println!("clone: {:?}", cloned_pair);
}
```

[section-trait-clone-ref-1]: https://doc.rust-lang.org/std/clone/trait.Clone.html
[section-trait-clone-ref-2]: https://doc.rust-lang.org/std/marker/trait.Copy.html

<a id="section-trait-supertraits"></a>

<a id="section-trait-supertraits--supertraits"></a>

## Supertraits

Rust doesn't have "inheritance", but you can define a trait as being a superset
of another trait. For example:

```rust
trait Person {
    fn name(&self) -> String;
}

// Person is a supertrait of Student.
// Implementing Student requires you to also impl Person.
trait Student: Person {
    fn university(&self) -> String;
}

trait Programmer {
    fn fav_language(&self) -> String;
}

// CompSciStudent (computer science student) is a subtrait of both Programmer
// and Student. Implementing CompSciStudent requires you to impl both supertraits.
trait CompSciStudent: Programmer + Student {
    fn git_username(&self) -> String;
}

fn comp_sci_student_greeting(student: &dyn CompSciStudent) -> String {
    format!(
        "My name is {} and I attend {}. My favorite language is {}. My Git username is {}",
        student.name(),
        student.university(),
        student.fav_language(),
        student.git_username()
    )
}

struct CSStudent {
    name: String,
    university: String,
    fav_language: String,
    git_username: String
}

impl Programmer for CSStudent {
    fn fav_language(&self) -> String {
        self.fav_language.clone()
    }
}

impl Student for CSStudent {
    fn university(&self) -> String {
        self.university.clone()
    }
}

impl Person for CSStudent {
    fn name(&self) -> String {
        self.name.clone()
    }
}

impl CompSciStudent for CSStudent {
    fn git_username(&self) -> String {
        self.git_username.clone()
    }
}

fn main() {
    let student = CSStudent {
        name: String::from("Alice"),
        university: String::from("MIT"),
        fav_language: String::from("Rust"),
        git_username: String::from("alice_codes"),
    };

    let greeting = comp_sci_student_greeting(&student);
    println!("{}", greeting);
}
```

<a id="section-trait-supertraits--see-also"></a>

#### See also:

[The Rust Programming Language chapter on supertraits][section-trait-supertraits-ref-1]

[section-trait-supertraits-ref-1]: https://doc.rust-lang.org/book/ch19-03-advanced-traits.html#using-supertraits-to-require-one-traits-functionality-within-another-trait

<a id="section-trait-disambiguating"></a>

<a id="section-trait-disambiguating--disambiguating-overlapping-traits"></a>

## Disambiguating overlapping traits

A type can implement many different traits. What if two traits both require
the same name for a function? For example, many traits might have a method
named `get()`. They might even have different return types!

Good news: because each trait implementation gets its own `impl` block, it's
clear which trait's `get` method you're implementing.

What about when it comes time to _call_ those methods? To disambiguate between
them, we have to use Fully Qualified Syntax.

```rust
trait UsernameWidget {
    // Get the selected username out of this widget
    fn get(&self) -> String;
}

trait AgeWidget {
    // Get the selected age out of this widget
    fn get(&self) -> u8;
}

// A form with both a UsernameWidget and an AgeWidget
struct Form {
    username: String,
    age: u8,
}

impl UsernameWidget for Form {
    fn get(&self) -> String {
        self.username.clone()
    }
}

impl AgeWidget for Form {
    fn get(&self) -> u8 {
        self.age
    }
}

fn main() {
    let form = Form {
        username: "rustacean".to_owned(),
        age: 28,
    };

    // If you uncomment this line, you'll get an error saying
    // "multiple `get` found". Because, after all, there are multiple methods
    // named `get`.
    // println!("{}", form.get());

    let username = <Form as UsernameWidget>::get(&form);
    assert_eq!("rustacean".to_owned(), username);
    let age = <Form as AgeWidget>::get(&form);
    assert_eq!(28, age);
}
```

<a id="section-trait-disambiguating--see-also"></a>

#### See also:

[The Rust Programming Language chapter on Fully Qualified syntax][section-trait-disambiguating-ref-1]

[section-trait-disambiguating-ref-1]: https://doc.rust-lang.org/book/ch19-03-advanced-traits.html#fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name
