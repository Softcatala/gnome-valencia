# perquè funcioni:
# - crea una carpeta /tmp/gnome-valencia
# - crea una carpeta /tmp/gnome-valencia/valencia
# - clona el repositori que vulguis a /tmp/gnome-valencia
# - desa la traducció ja feta a /tmp/gnome-valencia/valencia (ha de tenir el nom del repositori en el nom del fitxer)
# - canvia les dues variables del principi de tot (PKG i BRANCH)
# - executa només el primer script si només s'ha d'actualitzar la branca master, si també s'ha d'actualitzar una altra branca executa la segona part de l'script
# - per la primera part de l'script, aquest ja assumeix que ets dins d'un repositori, ajusta el primer "cd" segons necessitat

PKG="gnome-todo"
BRANCH="gnome-3-26"

cd ../../$PKG/po && git status && git checkout ca.po && rm -rf *.tmp *.pot && git rebase && git status && mv ../../valencia/$PKG.*.ca\@valencia.po ca\@valencia.po && git add ca\@valencia.po && git commit -m"[l10n] Updated Catalan (Valencian) translation" --author "Xavi Ivars <xavi.ivars@gmail.com>" && git push && echo $PKG

cp ca\@valencia.po TMP && git checkout $BRANCH && mv TMP ca\@valencia.po && git add ca\@valencia.po && git commit -m"[l10n] Updated Catalan (Valencian) translation" --author "Xavi Ivars <xavi.ivars@gmail.com>" && git push && git checkout master && echo $PKG



