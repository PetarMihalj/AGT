import llvmlite.ir as ir
import llvmlite.binding as bind

module = ir.Module(name='__file__')
module.triple = f"{bind.get_default_triple()}"

double = ir.DoubleType()
fnType = ir.FunctionType(double, (double, double))
voidType = ir.VoidType()
intType = ir.IntType(32)
kvadratType = ir.LiteralStructType((intType, intType))


func = ir.Function(module, ir.FunctionType(intType, ()),
                   "main")
block = func.append_basic_block("entry")
builder = ir.IRBuilder(block)
res = builder.call(func3, (ir.Constant(double, 1.0), ir.Constant(double, 1.0)))
res2 = builder.fptosi(res, intType)
builder.ret(res2)

print()

print(module)
