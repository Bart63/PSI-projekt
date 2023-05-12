Plik do generowania i wizualizacji mapy. Jakiś mi się wkradł błąd w łączeniu miast obrzeżnych ale nwm dlaczego, ogarnę to w weekend.

Poza tym to:

Ten plik, generuje klasę miasta czyli:
kwadratowy array o rozmiarze "size"
czyli np. dla rozmiaru 4:
[[1, 2, 3 ,4],
[5, 6, 7, 8],
[9, 10, 11, 12],
[13, 14, 15, 16]]

gdzie każdy z numerków reprezentuje skrzyżowanie i wchodzi w nich skład
[numer_skrzyżowania, [lista połączonych_skrzyżowań] np. [1, True, []

każdy element z  "połączonych skrzyżowań" składa się z:
[numer_połączonego_skrzyżowania, stanu swiateł (T-zielone/F-czerwone), listy aut na skrzyżowaniu) np. 

Proszę o to aby auto miało informajce;
color np. w [b,g,r] i stopień przejechania drogi <0,1>