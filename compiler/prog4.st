struct s1<V,A,T>{
    type t = A.t;
    A<V> petar;
    V<T> reverse;
}

struct vector<V, A = allocator<V>>{

}

struct allocator<V>{

}

struct wrapper<T>{

}

// s1<int, vector<int>, wrapper<vector<int>>**>
