let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/thesis
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +0 compiler/ex/demo_fib.st
badd +0 term://.//87309:/bin/bash
badd +0 compiler/type_inference/recursive_logger.py
badd +31 compiler/type_inference/type_gens.py
badd +7 compiler/type_inference/type_gens_io.py
badd +7 compiler/type_inference/type_gens_lifetime.py
badd +7 compiler/type_inference/type_gens_memory.py
badd +7 compiler/type_inference/type_gens_misc.py
badd +8 compiler/type_inference/type_gens_ops.py
badd +0 compiler/type_inference/type_gens_typing.py
badd +0 compiler/type_inference/type_engine.py
badd +402 compiler/type_inference/type_engine_rules.py
badd +0 compiler/helpers.py
badd +23 compiler/type_inference/__init__.py
badd +15 compiler/type_inference/__main__.py
badd +0 compiler/type_inference/flat_ir.py
badd +0 compiler/semantics_parsing/semantic_ast.py
badd +0 compiler/type_inference/type_system.py
argglobal
%argdel
set stal=2
edit compiler/ex/demo_fib.st
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 28 + 30) / 60)
exe 'vert 1resize ' . ((&columns * 113 + 118) / 236)
exe '2resize ' . ((&lines * 28 + 30) / 60)
exe 'vert 2resize ' . ((&columns * 113 + 118) / 236)
exe 'vert 3resize ' . ((&columns * 122 + 118) / 236)
argglobal
enew
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
wincmd w
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 17 - ((15 * winheight(0) + 14) / 28)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17
normal! 030|
wincmd w
argglobal
if bufexists("term://.//87309:/bin/bash") | buffer term://.//87309:/bin/bash | else | edit term://.//87309:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 3591 - ((56 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3591
normal! 026|
wincmd w
3wincmd w
exe '1resize ' . ((&lines * 28 + 30) / 60)
exe 'vert 1resize ' . ((&columns * 113 + 118) / 236)
exe '2resize ' . ((&lines * 28 + 30) / 60)
exe 'vert 2resize ' . ((&columns * 113 + 118) / 236)
exe 'vert 3resize ' . ((&columns * 122 + 118) / 236)
tabedit compiler/type_inference/type_engine.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 199 - ((43 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
199
normal! 027|
tabedit compiler/helpers.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 50 - ((49 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
50
normal! 019|
tabedit compiler/type_inference/recursive_logger.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 14 - ((13 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
14
normal! 022|
tabedit compiler/type_inference/type_gens.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 31 - ((30 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 024|
wincmd w
argglobal
if bufexists("compiler/type_inference/type_gens_typing.py") | buffer compiler/type_inference/type_gens_typing.py | else | edit compiler/type_inference/type_gens_typing.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 7 - ((6 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
tabedit compiler/type_inference/type_system.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 65 - ((34 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
65
normal! 037|
tabedit compiler/type_inference/flat_ir.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 211 - ((20 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
211
normal! 055|
tabedit compiler/type_inference/type_engine_rules.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 413 - ((36 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
413
normal! 021|
tabedit compiler/semantics_parsing/semantic_ast.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 501 - ((55 * winheight(0) + 28) / 57)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
501
normal! 0
tabnext 1
set stal=1
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=filnxtToOFI
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
