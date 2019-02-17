arc([], _, _).

arc(X, 'S1', RList) :- pushArc(X, 'N1', 'S2', RList).
arc([H|T], 'S1', RList) :- catTest('AUX', H), arc(T, 'S3', RList).
arc([H|T], 'S2', RList) :- catTest('V', H), arc(T, 'S5', RList).
arc(X, 'S3', RList) :- pushArc(X, 'N1', 'S4', RList).
arc([H|T], 'S4', RList) :- catTest('V', H), arc(T, 'S5', RList).
arc(X, 'S5', RList) :- pushArc(X, 'N1', 'S6', RList).
arc(X, 'S5', RList) :- popArc(X, RList).
arc(X, 'S6', RList) :- pushArc(X, 'P1', 'S6', RList).
arc(X, 'S6', RList) :- popArc(X, RList).

arc([H|T], 'N1', RList) :- catTest('DET', H), arc(T, 'N2', RList).
arc([H|T], 'N1', RList) :- catTest('NPR', H), arc(T, 'N3', RList).
arc([H|T], 'N2', RList) :- catTest('ADJ', H), arc(T, 'N2', RList).
arc([H|T], 'N2', RList) :- catTest('N', H), arc(T, 'N4', RList).
arc(X, 'N3', RList) :- popArc(X, RList).
arc(X, 'N4', RList) :- pushArc(X, 'P1', 'N4', RList).
arc(X, 'N4', RList) :- popArc(X, RList).

arc([H|T], 'P1', RList) :- catTest('PREP', H), arc(T, 'P2', RList).
arc(X, 'P2', RList) :- pushArc(X, 'N1', 'P3', RList).
arc(X, 'P3', RList) :- popArc(X, RList).

pushArc(X, NN, RN, RList) :- append([RN], RList, URList), arc(X, NN, URList).
popArc(X, [NN | URList]) :- arc(X, NN, URList).

catTest('DET', 'The').
catTest('DET', 'the').
catTest('ADJ', 'big').
catTest('ADJ', 'old').
catTest('N', 'tree').
catTest('N', 'house').
catTest('N', 'stream').
catTest('V', 'shades').
catTest('PREP', 'by').
catTest('AUX', 'has').

sentence(X) :- arc(X, 'S1', []), !.
