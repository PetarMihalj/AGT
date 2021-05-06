fn printpos(ptr, pos){
    out(ptr[pos]!);
}

fn setpos(ptr, pos, val){
    ptr[pos]! = val;
}

fn main() -> i32{
    let A = heap_alloc<i32>(10);
    setpos(A, 3, 123);
    setpos(A, 6, 456);
    printpos(A, 3);
    printpos(A, 6);
    printpos(A, 5);
    heap_free(A);

    // B will sometimes be allocated exactly where A was, and overwrite its contents.
    // of course, this is a memory error, but it will probably continue without crashing.

    let B = heap_alloc<i32>(10);
    setpos(B, 3, 0);
    setpos(B, 6, 0);
    printpos(A, 3);
    printpos(A, 6);
    printpos(A, 5);

    return 0;
}
