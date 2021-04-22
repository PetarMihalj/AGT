struct shared_ptr<T>{
    let item_ptr = @T;
    let count = @i32;
}

fn __init__(sptr_ptr, item_ptr){
    type T = sptr_ptr!.item!;
    type _1 = enable_if<sptr_ptr == @shared_ptr<T>>;
    type _2 = enable_if<@T == item_ptr>;

    sptr_ptr!.item_ptr = item_ptr;
    sptr_ptr!.count = heap_alloc<i32>(1);
}

fn __dest__(sptr_ptr){
    type T = sptr_ptr!.item!;
    type _1 = enable_if<sptr_ptr == @shared_ptr<T>>;

    sptr_ptr!.count! = sptr_ptr!.count! - 1;
    if (sptr_ptr!.count == 1){
        heap_free<T>(sptr_ptr!.item_ptr);
        heap_free<i32>(sptr_ptr!.count);
    }
}

fn __copy__(sptr_ptr_dest, sptr_ptr_src){
    type T = sptr_ptr_dest!.item!;
    type _1 = enable_if<sptr_ptr_dest == @shared_ptr<T>>;
    type _2 = enable_if<sptr_ptr_src == @shared_ptr<T>>;

    sptr_ptr_src!.count! = sptr_ptr_src!.count! + 1;

    sptr_ptr_dest!.item_ptr = sptr_ptr_src!.item_ptr;
    sptr_ptr_dest!.count = sptr_ptr_src!.count;
}

fn main(){
    let a = shared_ptr<i64>(heap_alloc<i64>(15i64));

}
