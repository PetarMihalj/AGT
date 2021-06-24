def get_member(src: str, member_name: str, 
        fc: context.FunctionContext):
    dest = fc.scope_man.new_tmp_var_name("member")
    fc.types[dest] = fc.types[src].types[member_name]

    stmn = fc.types[src].mangled_name
    ind = fc.types[src].members.index(member_name)

    fc.code.extend([ 
        f"\t%{dest} = getelementptr inbounds " +
        f"%{stmn}, %{stmn}* %{src}, i32 0, i32 {ind}"
    ])
    return dest

