let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/thesis/compiler
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +37 prog1.st
badd +130 ~/system_data/dotfiles/init.vim
badd +1 lexer.py
badd +1 term://.//2305:/bin/bash
badd +1 term://.//2308:/bin/bash
badd +1 parser.py
badd +1 parser_rules/atomic.py
badd +12 parser_rules/expressions.py
badd +2 parser_rules/statements.py
badd +4 parser_rules/structural.py
badd +1 parser_rules/__init__.py
badd +8 expressions.py
badd +415 parser_rules.py
badd +9379 term://.//2317:/bin/bash
badd +3 prog2.st
badd +0 parser.out
badd +2 prog3.st
badd +11 template_engine.py
badd +0 term://.//10873:/bin/bash
badd +0 term://.//15112:/bin/bash
badd +0 flattener.py
badd +26 flatIR.py
badd +0 term://.//16691:/bin/bash
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
let s:l = 29 - ((22 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
29
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
let s:l = 47 - ((0 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
47
normal! 025|
wincmd w
argglobal
if bufexists('term://.//2305:/bin/bash') | buffer term://.//2305:/bin/bash | else | edit term://.//2305:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 31 - ((30 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
31
normal! 0
wincmd w
argglobal
if bufexists('term://.//2308:/bin/bash') | buffer term://.//2308:/bin/bash | else | edit term://.//2308:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 186 - ((27 * winheight(0) + 14) / 29)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
186
normal! 0
wincmd w
exe '1resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 118 + 118) / 236)
exe '2resize ' . ((&lines * 29 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
exe '3resize ' . ((&lines * 31 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 117 + 118) / 236)
exe '4resize ' . ((&lines * 29 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 117 + 118) / 236)
tabedit parser.py
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
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 20 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 118 + 118) / 236)
exe '2resize ' . ((&lines * 19 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
exe '3resize ' . ((&lines * 20 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 118 + 118) / 236)
exe '4resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 117 + 118) / 236)
exe '5resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 117 + 118) / 236)
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
let s:l = 48 - ((18 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
48
normal! 05|
wincmd w
argglobal
if bufexists('term://.//15112:/bin/bash') | buffer term://.//15112:/bin/bash | else | edit term://.//15112:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 2872 - ((18 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2872
normal! 029|
wincmd w
argglobal
if bufexists('prog3.st') | buffer prog3.st | else | edit prog3.st | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 2 - ((1 * winheight(0) + 10) / 20)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2
normal! 018|
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
let s:l = 391 - ((26 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
391
normal! 023|
wincmd w
argglobal
if bufexists('parser.out') | buffer parser.out | else | edit parser.out | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 287 - ((14 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
287
normal! 0
wincmd w
exe '1resize ' . ((&lines * 20 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 118 + 118) / 236)
exe '2resize ' . ((&lines * 19 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 118 + 118) / 236)
exe '3resize ' . ((&lines * 20 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 118 + 118) / 236)
exe '4resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 117 + 118) / 236)
exe '5resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 5resize ' . ((&columns * 117 + 118) / 236)
tabedit parser_rules.py
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
exe 'vert 1resize ' . ((&columns * 113 + 118) / 236)
exe '2resize ' . ((&lines * 19 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 113 + 118) / 236)
exe '3resize ' . ((&lines * 10 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 113 + 118) / 236)
exe 'vert 4resize ' . ((&columns * 122 + 118) / 236)
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
let s:l = 28 - ((3 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
28
normal! 023|
wincmd w
argglobal
if bufexists('term://.//16691:/bin/bash') | buffer term://.//16691:/bin/bash | else | edit term://.//16691:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 588 - ((18 * winheight(0) + 9) / 19)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
588
normal! 029|
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
let s:l = 25 - ((3 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
25
normal! 02|
wincmd w
argglobal
if bufexists('flatIR.py') | buffer flatIR.py | else | edit flatIR.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 23 - ((22 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
23
normal! 0
wincmd w
exe '1resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 113 + 118) / 236)
exe '2resize ' . ((&lines * 19 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 113 + 118) / 236)
exe '3resize ' . ((&lines * 10 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 113 + 118) / 236)
exe 'vert 4resize ' . ((&columns * 122 + 118) / 236)
tabedit template_engine.py
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
exe '1resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe '2resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 3resize ' . ((&columns * 118 + 118) / 236)
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
let s:l = 17 - ((16 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17
normal! 017|
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
let s:l = 7 - ((4 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
7
normal! 015|
wincmd w
argglobal
if bufexists('term://.//10873:/bin/bash') | buffer term://.//10873:/bin/bash | else | edit term://.//10873:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 785 - ((60 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
785
normal! 029|
wincmd w
exe '1resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 1resize ' . ((&columns * 117 + 118) / 236)
exe '2resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 2resize ' . ((&columns * 117 + 118) / 236)
exe 'vert 3resize ' . ((&columns * 118 + 118) / 236)
tabnext 3
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
