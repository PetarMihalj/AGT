let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/thesis/compiler
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 prog1.st
badd +130 ~/system_data/dotfiles/init.vim
badd +1 lexer.py
badd +31 term://.//22681:/bin/bash
badd +1 term://.//22682:/bin/bash
badd +2 parser.py
badd +1 parser_rules/atomic.py
badd +12 parser_rules/expressions.py
badd +2 parser_rules/statements.py
badd +4 parser_rules/structural.py
badd +1 parser_rules/__init__.py
badd +8 expressions.py
badd +455 parser_rules.py
badd +9379 term://.//2317:/bin/bash
badd +3 prog2.st
badd +287 parser.out
badd +2 prog3.st
badd +19 template_engine.py
badd +61 term://.//3745:/bin/bash
badd +1 flattener.py
badd +113 flatIR.py
badd +1 term://.//22690:/bin/bash
badd +12 ~/thesis/llvm_test/example.bc
badd +0 term://.//5267:/bin/bash
argglobal
silent! argdel *
set stal=2
edit prog1.st
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 118 + 118) / 236)
exe '2resize ' . ((&lines * 29 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
exe '3resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 117 + 118) / 236)
exe '4resize ' . ((&lines * 29 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 117 + 118) / 236)
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
let s:l = 37 - ((30 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
37
normal! 0
wincmd w
argglobal
if bufexists('lexer.py') | buffer lexer.py | else | edit lexer.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 49 - ((23 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
49
normal! 025|
wincmd w
argglobal
if bufexists('parser_rules.py') | buffer parser_rules.py | else | edit parser_rules.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 46 - ((0 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
46
normal! 09|
wincmd w
argglobal
if bufexists('term://.//22682:/bin/bash') | buffer term://.//22682:/bin/bash | else | edit term://.//22682:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 9327 - ((28 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
9327
normal! 029|
wincmd w
exe '1resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 118 + 118) / 236)
exe '2resize ' . ((&lines * 29 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
exe '3resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 117 + 118) / 236)
exe '4resize ' . ((&lines * 29 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 117 + 118) / 236)
tabedit flatIR.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
2wincmd k
wincmd w
wincmd w
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe '2resize ' . ((&lines * 10 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 117 + 118) / 236)
exe '3resize ' . ((&lines * 19 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 4resize ' . ((&columns * 118 + 118) / 236)
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
let s:l = 132 - ((17 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
132
normal! 015|
wincmd w
argglobal
if bufexists('term://.//22690:/bin/bash') | buffer term://.//22690:/bin/bash | else | edit term://.//22690:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 18 - ((1 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
18
normal! 0
wincmd w
argglobal
if bufexists('prog1.st') | buffer prog1.st | else | edit prog1.st | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 30 - ((11 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
30
normal! 08|
wincmd w
argglobal
if bufexists('parser_rules.py') | buffer parser_rules.py | else | edit parser_rules.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 501 - ((36 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
501
normal! 09|
wincmd w
4wincmd w
exe '1resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe '2resize ' . ((&lines * 10 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 117 + 118) / 236)
exe '3resize ' . ((&lines * 19 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 4resize ' . ((&columns * 118 + 118) / 236)
tabedit ~/thesis/llvm_test/example.bc
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
let s:l = 22 - ((21 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 09|
lcd ~/thesis/compiler
wincmd w
argglobal
if bufexists('term://.//5267:/bin/bash') | buffer term://.//5267:/bin/bash | else | edit term://.//5267:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 159 - ((60 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
159
normal! 030|
lcd ~/thesis/compiler
wincmd w
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
tabnext 2
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
