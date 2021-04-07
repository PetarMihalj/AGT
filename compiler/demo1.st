//
// compile time computation example
//

/*
Struct definitions have:
    - a name
    - type parameters (plain names like "A", "B", ...)
    - bunch of statements of form:
        - type <ID> = <TypeExpression>  (these declare type variables)
        - let <ID> = <TypeExpression>   (these declare type variables,
                                         but also specify concrete members,
                                         which can be referenced at runtime)

Function definitions have:
    - a name
    - type parameters (plain names like "A", "B", ...)
        - can only be used in a context of type expression
    - arguments       (plain names like "a", "b", ...)
        - can be used both in the context of type and runtime expression
            - refers to type in type expr, and concrete data in runtime expr
        

A program consists of a collection of function and struct definitions.
These are first parsed by type/runtime semantics UNAWARE parser,
and then their bodies are contextually split into type and runtime expressions.
    - for example, in the statement "type a =  a.t", expression "a.t" is made
      to be a type expression, since it occurs where a type is needed.
When this second phase ends, we are left with a collection of function and structure definitions,
in an AST form (nodes specified in "lang_ast.py"). We call this form LAST (language AST).


Type Construction:
    - The next phase of compilation is called type construction.
    - This process is modeled by a nondeterministic functional language,
      which manipulates four primary entities:
        - TypeGenerators
            - Function definitions and struct definitions
        - TypeVariables
            - simple names like "a", "A", which are local to the TypeScope
                - these can include mangled variable names from local scopes 
                - are all distinct in a scope, otherwise its syntactic error
        - TypeExpressions
            - resolve to types, in a functional (pure) way.
        - TypeScopes
            - Contain two distinct 
            - Localization for TypeVariables, are initialized wh 









Every struct or function definition consists of bunch of statements.



type statements can only be at the beginning of func/struct
type inference on functions/structs is done in order of:
  (type and regular parameters) -> type statements -> return type -> other statements
      notice that this is ok:
          -structures shouldnt refer to themselves in type statements 
              (so full definition isnt needed
          --functions shouldnt refer to themselves in type statements 
                (when regular statements get parsed, full function def is already inferred)
*/

// if they arent equal, division by _1 crashes this nondeterministic branch
struct assert_equal<A,B>{
    type _1 = A == B;
    type _2 = i1 / _1;
}

struct assert_not_equal<A,B>{
    type _1 = A != B;
    type _2 = i1 / _1;
}

struct fib<T>{
    type _1 = assert_equal<T, i1>;
    type t = i1;
}
struct fib<T>{
    type _1 = assert_equal<T, i2>;
    type t = i1;
}

struct fib<T>{
    type _1 = assert_not_equal<T, i1>;
    type _2 = assert_not_equal<T, i2>;
    type t = fib<T-i1>.t+fib<T-i2>.t;
}

// notice the i32 parametrized constructor
// that one creates an i32 with default value equal to parameter
fn ct_fib<T>() -> i32{
    type f = fib<T>.t;
    let value = i32<f>();
    return value;
}

fn main(){
    let v = ct_fib<i5>();
}
