sentence(X, R) :- np(X, Y), vp(Y, R).

np(X, R) :- det(X, Y), n(Y, R).

vp(X, R) :- v(X, Y), adv(Y, R).
vp(X, R) :- v(X, Y), pp(Y, R).
vp(X, R) :- v(X, Y), np(Y, R).
vp(X, R) :- v(X, Y), np(Y, Z), pp(Z, R).
vp(X, R) :- aux(X, Y), v(Y, Z), adv(Z, R).

pp(X, R) :- prep(X, Y), np(Y, R).

det(X, R) :- art(X, Y), adj(Y, R).
det(X, R) :- art(X, R).

art(['The' | T], T).
art(['an' | T], T).

n(['Boy' | T], T).
n(['Apple' | T], T).

v(['ate' | T], T).

prep(['on' | T], T).
prep(['in' | T], T).

adj(['short' | T], T).
adj(['tall' | T], T).

adv(['fast' | T], T).
adv(['slow' | T], T).

aux(['has' | T], T).
aux(['had' | T], T).

validSentence(X) :- sentence(X, []), !.
