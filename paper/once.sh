export THESIS_SRCDIR=$(readlink -f './source')
export THESIS_BUILDDIR=$(readlink -f './build')
export THESIS_RESDIR=$(readlink -f './res')

(cd $THESIS_SRCDIR && pdflatex -interaction=nonstopmode -output-directory=$THESIS_BUILDDIR diplomski.tex)
