
; ModuleID = "__file__"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

declare i32 @puts(i8* nocapture) nounwind

@.hello = private unnamed_addr constant [13 x i8] c"hello world\0A\00"

%Foo = type {
    i64,      
    i32     
}

%FooBar = type {
    %Foo,      
    i32     
}

define i32 @main(i32 %argc, i8** %argv) {
    %1 = getelementptr [13 x i8], [13 x i8]* @.hello, i32 0, i32 0
    call i32 @puts(i8* %1)


    %foobar = alloca %FooBar
    %3 = getelementptr %FooBar, %FooBar* %foobar, i32 0, i32 0, i32 1
    store i32 3, i32* %3

    %4 = load i32, i32* %3

    ret i32 %4
}

