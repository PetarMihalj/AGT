let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/thesis/compiler
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +100 parser_rules.py
badd +0 term://.//1523:/bin/bash
badd +33 prog4.st
badd +51 lexer.py
badd +4 ast.py
badd +10046 term://.//7959:/bin/bash
badd +80 lang_ast.py
badd +72 parser.py
badd +0 term://.//32756:/bin/bash
badd +0 helpers.py
badd +43 prog1.st
badd +0 parser.out
badd +2853 term://.//19901:/bin/bash
argglobal
silent! argdel *
set stal=2
edit parser_rules.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
wincmd w
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 78 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 78 + 118) / 236)
exe 'vert 3resize ' . ((&columns * 78 + 118) / 236)
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
let s:l = 94 - ((35 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
94
normal! 09|
wincmd w
argglobal
if bufexists('term://.//1523:/bin/bash') | buffer term://.//1523:/bin/bash | else | edit term://.//1523:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 6247 - ((26 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
6247
normal! 020|
wincmd w
argglobal
if bufexists('prog4.st') | buffer prog4.st | else | edit prog4.st | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 31 - ((30 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 09|
wincmd w
exe 'vert 1resize ' . ((&columns * 78 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 78 + 118) / 236)
exe 'vert 3resize ' . ((&columns * 78 + 118) / 236)
tabedit parser_rules.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
wincmd w
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
exe 'vert 1resize ' . ((&columns * 78 + 118) / 236)
exe '2resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 54 + 118) / 236)
exe '3resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 54 + 118) / 236)
exe '4resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 102 + 118) / 236)
exe '5resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 102 + 118) / 236)
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
let s:l = 259 - ((0 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
259
normal! 031|
wincmd w
argglobal
if bufexists('parser.py') | buffer parser.py | else | edit parser.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 79 - ((22 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
79
normal! 017|
wincmd w
argglobal
if bufexists('lang_ast.py') | buffer lang_ast.py | else | edit lang_ast.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 65 - ((5 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
65
normal! 07|
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
let s:l = 1 - ((0 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
if bufexists('term://.//19901:/bin/bash') | buffer term://.//19901:/bin/bash | else | edit term://.//19901:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 10030 - ((29 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
10030
normal! 0
wincmd w
4wincmd w
exe 'vert 1resize ' . ((&columns * 78 + 118) / 236)
exe '2resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 54 + 118) / 236)
exe '3resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 54 + 118) / 236)
exe '4resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 102 + 118) / 236)
exe '5resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 102 + 118) / 236)
tabedit parser.out
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
let s:l = 2675 - ((59 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2675
normal! 014|
tabedit helpers.py
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
let s:l = 22 - ((21 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
22
normal! 022|
tabedit parser.py
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
let s:l = 83 - ((59 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
83
normal! 08|
wincmd w
argglobal
if bufexists('term://.//32756:/bin/bash') | buffer term://.//32756:/bin/bash | else | edit term://.//32756:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 965 - ((53 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
965
normal! 030|
wincmd w
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
tabedit lexer.py
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
let s:l = 30 - ((29 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
30
normal! 05|
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
