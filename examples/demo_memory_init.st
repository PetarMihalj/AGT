struct rect<T>{
    let a = T;
    let b = T;
}

fn main() -> i32{
    let a = in<i32>();
    let b = in<i32>();

    type irect = rect<i32>;

    let rect_heap = heap_init<irect>(a,b);

    out(rect_heap!.a);
    out(rect_heap!.b);

    heap_free(rect_heap);
    out(rect_heap!.a);
    out(rect_heap!.b);
}
