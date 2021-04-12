let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/thesis/compiler
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +6 type_engine.py
badd +1 lang_ast.py
badd +1 term://.//5709:/bin/bash
badd +2 notes_te
badd +103 ex/demo1.st
badd +0 ex/demo2.st
argglobal
silent! argdel *
set stal=2
edit type_engine.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
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
exe 'vert 2resize ' . ((&columns * 78 + 118) / 236)
exe '3resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 78 + 118) / 236)
exe '4resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 78 + 118) / 236)
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
let s:l = 167 - ((47 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
167
normal! 0
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
let s:l = 1 - ((0 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
argglobal
if bufexists('notes_te') | buffer notes_te | else | edit notes_te | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 28 - ((27 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
28
normal! 0
wincmd w
argglobal
if bufexists('term://.//5709:/bin/bash') | buffer term://.//5709:/bin/bash | else | edit term://.//5709:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 1 - ((0 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 78 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 78 + 118) / 236)
exe '3resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 3resize ' . ((&columns * 78 + 118) / 236)
exe '4resize ' . ((&lines * 30 + 32) / 64)
exe 'vert 4resize ' . ((&columns * 78 + 118) / 236)
tabedit notes_te
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
let s:l = 1 - ((0 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 04|
wincmd w
argglobal
if bufexists('ex/demo1.st') | buffer ex/demo1.st | else | edit ex/demo1.st | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 34 - ((33 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
34
normal! 09|
wincmd w
argglobal
if bufexists('ex/demo2.st') | buffer ex/demo2.st | else | edit ex/demo2.st | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 3 - ((2 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 78 + 118) / 236)
exe 'vert 2resize ' . ((&columns * 78 + 118) / 236)
exe 'vert 3resize ' . ((&columns * 78 + 118) / 236)
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
