<div align="center">

<!-- Logo:
<img src="assets/images/logo.png" alt="Introduction to Julia" width="220">
-->

# Introduction to Julia

**Praktyczny, 13-lekcyjny kurs języka Julia do obliczeń naukowych i numerycznych.**

[![Course CI](https://github.com/Cartesian-School/Introduction-to-Julia/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/Cartesian-School/Introduction-to-Julia/actions/workflows/ci.yaml)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-yellow.svg)](LICENSE)
[![Content License: CC BY-NC-SA 4.0](https://img.shields.io/badge/content%20license-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE-CC-BY-NC-SA.md)
[![Julia](https://img.shields.io/badge/julia-1.11.3-9558B2.svg)](https://julialang.org/downloads/)
![Lessons](https://img.shields.io/badge/lessons-13-blue.svg)
![Language](https://img.shields.io/badge/course%20language-Russian-red.svg)

[English](README.md) · [Русский](README.ru.md) · **Polski**

</div>

---

## O kursie

**Introduction to Julia** to praktyczny kurs dla programistów, którzy chcą poznać język Julia poprzez wykonywalne przykłady, a nie wyłącznie przez teorię.

Kurs rozpoczyna się od podstaw języka, a następnie przechodzi do zagadnień, w których Julia jest szczególnie mocna: obliczeń naukowych, metod numerycznych i programowania wysokiej wydajności.

Zakres kursu obejmuje:

- napisy i Unicode;
- struktury danych oraz instrukcje sterujące;
- funkcje i broadcasting;
- zarządzanie pakietami i odtwarzalne środowiska;
- wizualizację i tworzenie wykresów;
- wielokrotną dyspozycję metod;
- benchmarkowanie i analizę wydajności;
- numeryczną algebrę liniową;
- faktoryzacje macierzy.

Wszystkie lekcje przygotowano w postaci notebooków Jupyter. Każdy notebook łączy objaśnienia, wykonywalne przykłady, ćwiczenia, rozwiązania wzorcowe i automatyczną weryfikację wyników.

Materiał bazuje na kursie JuliaAcademy *Introduction to Julia* i został znacząco zaadaptowany, rozszerzony, zweryfikowany i zaktualizowany dla Julia **1.11.3**. Obecna edycja zawiera również dodatkowe materiały z zakresu wydajności, numerycznej algebry liniowej i faktoryzacji macierzy.

---

## Język kursu

**Główna treść dydaktyczna jest napisana po rosyjsku.** Nazwy plików, kod Julia, nazwy API oraz większość identyfikatorów technicznych pozostają w języku angielskim.

Dokumentacja repozytorium jest dostępna w trzech wersjach językowych:

- **English:** [README.md](README.md)
- **Русский:** [README.ru.md](README.ru.md)
- **Polski:** [README.pl.md](README.pl.md)

---

## Efekty uczenia się

Po ukończeniu kursu będziesz potrafić:

- **pisać idiomatyczny kod w Julii** z użyciem zmiennych, napisów, instrukcji sterujących, funkcji, funkcji anonimowych, broadcastingu i konwencji mutacji;
- **pracować z podstawowymi strukturami danych Julii** — krotkami, krotkami nazwanymi, słownikami, wektorami, macierzami i tablicami;
- **poprawnie obsługiwać napisy Unicode** i rozumieć różnicę między iteracją po znakach a indeksowaniem UTF-8;
- **używać wielokrotnej dyspozycji jako narzędzia projektowego**, a nie jedynie jako mechanizmu przeciążania metod;
- **zarządzać pakietami i odtwarzalnymi środowiskami** przy użyciu `Pkg`, `Project.toml` i `Manifest.toml`;
- **tworzyć wykresy i wizualizacje** z użyciem `Plots.jl` i różnych backendów;
- **poprawnie mierzyć wydajność kodu Julia** za pomocą `BenchmarkTools.jl` oraz rozumieć wpływ kompilacji, alokacji, stabilności typów i kolejności dostępu do pamięci;
- **rozwiązywać zadania numerycznej algebry liniowej** z użyciem wektorów, macierzy, norm, wyznaczników, układów równań liniowych i struktur macierzowych;
- **dobierać i stosować faktoryzacje macierzy**, w tym LU, QR, Cholesky, SVD oraz rozkład własny.

---

## Dla kogo jest ten kurs

Kurs jest przeznaczony dla osób, które już potrafią programować i chcą dodać Julię do swojego zestawu narzędzi.

### Wymagania wstępne

| Wymaganie | Poziom |
|---|---|
| Doświadczenie programistyczne | **Wymagane.** Wystarczy Python, MATLAB, R, C, C++, Java lub inny język. |
| Znajomość języka rosyjskiego | **Wymagana do czytania objaśnień.** |
| Znajomość Jupyter | **Pomocna.** Podstawy są omówione w lekcji 1. |
| Algebra liniowa | **Pomocna dla lekcji 11–13.** Niezbędne podstawy są wprowadzane w lekcji 11. |
| Wcześniejsza znajomość Julii | **Nie jest wymagana.** |

Kurs **nie jest przeznaczony jako pierwszy kurs programowania**. Zakłada znajomość takich pojęć jak zmienne, pętle, instrukcje warunkowe i funkcje.

---

## Zawartość kursu

Kurs jest podzielony na dwa bloki:

1. **Podstawy języka Julia** — lekcje 1–9
2. **Wydajność i numeryczna algebra liniowa** — lekcje 10–13

### Blok 1 — Podstawy języka Julia

| Nr | Lekcja | Główne zagadnienia |
|---|---|---|
| 1 | [Getting started](01%20-%20Getting%20started.ipynb) | Uruchamianie Julii, zmienne, wyjście, komentarze, arytmetyka |
| 2 | [Strings](02%20-%20Strings.ipynb) | Napisy, `Char`, interpolacja, konkatenacja, UTF-8, bezpieczne indeksowanie Unicode |
| 3 | [Data structures](03%20-%20Data%20structures.ipynb) | Krotki, krotki nazwane, słowniki, wektory, macierze, tablice, mutowalność, typy elementów |
| 4 | [Loops](04%20-%20Loops.ipynb) | `while`, `for`, zakresy, iteracja po kolekcjach |
| 5 | [Conditionals](05%20-%20Conditionals.ipynb) | `if` / `elseif` / `else`, operator trójargumentowy, short-circuit evaluation |
| 6 | [Functions](06%20-%20Functions.ipynb) | Formy deklaracji funkcji, funkcje anonimowe, programowanie generyczne, konwencja `!`, broadcasting |
| 7 | [Packages](07%20-%20Packages.ipynb) | `Pkg`, środowiska, instalowanie pakietów, odtwarzalność |
| 8 | [Plotting](08%20-%20Plotting.ipynb) | `Plots.jl`, `plot`, `plot!`, backendy, etykiety, wiele serii, animacja |
| 9 | [Multiple dispatch](09%20-%20Multiple%20dispatch.ipynb) | Funkcje generyczne, metody, hierarchia typów, specyficzność, wielokrotna dyspozycja |

### Blok 2 — Wydajność i numeryczna algebra liniowa

| Nr | Lekcja | Główne zagadnienia |
|---|---|---|
| 10 | [Julia is fast](10%20-%20Julia%20is%20fast.ipynb) | Benchmarkowanie, kompilacja, stabilność typów, alokacje, układ pamięci, porównanie z C i Pythonem |
| 11 | [Linear algebra concepts](11%20-%20Linear%20algebra%20concepts.ipynb) | Wektory, macierze, normy, rząd, wyznaczniki, transpozycja vs sprzężenie hermitowskie, układy równań |
| 12 | [Linear algebra in Julia](12%20-%20Linear%20algebra%20in%20Julia.ipynb) | `LinearAlgebra`, `dot`, `cross`, `norm`, `det`, `rank`, `\`, macierze strukturalne, podstawy BLAS |
| 13 | [Factorizations and other fun](13%20-%20Factorizations%20and%20other%20fun.ipynb) | LU, QR, Cholesky, SVD, wartości i wektory własne, ponowne użycie faktoryzacji |

> Lekcje 11 i 12 tworzą spójną parę: w lekcji 11 omawiane są podstawy matematyczne, a w lekcji 12 te same operacje są realizowane bezpośrednio w Julii.

---

## Instalacja

### 1. Zainstaluj Julię

Wszystkie notebooki zostały zweryfikowane dla **Julia 1.11.3**.

Na Linuxie i macOS przy użyciu `juliaup`:

```bash
curl -fsSL https://install.julialang.org | sh
juliaup add 1.11.3
juliaup default 1.11.3
```

Sprawdź instalację:

```bash
julia --version
```

Oczekiwany wynik:

```text
julia version 1.11.3
```

W systemie Windows możesz zainstalować Julię przez `juliaup` z Microsoft Store lub użyć oficjalnego instalatora dostępnego na stronie [Julia Downloads](https://julialang.org/downloads/).

---

### 2. Sklonuj repozytorium

```bash
git clone https://github.com/Cartesian-School/Introduction-to-Julia.git
cd Introduction-to-Julia
```

---

### 3. Odtwórz środowisko kursu

W katalogu głównym repozytorium uruchom:

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

Polecenie instaluje zależności zapisane w `Project.toml` i `Manifest.toml`.

> Pierwsze uruchomienie może potrwać kilka minut z powodu prekompilacji niektórych pakietów.

---

### 4. Zainstaluj kernel Jupyter

```bash
julia --project=. -e 'using Pkg; Pkg.add("IJulia"); using IJulia'
```

Jeśli Jupyter nie jest jeszcze zainstalowany, `IJulia` może zaproponować instalację prywatnego środowiska Miniconda.

---

### 5. Uruchom notebooki

Przez IJulia:

```bash
julia --project=. -e 'using IJulia; notebook(dir=".")'
```

Lub, jeśli Jupyter jest już zainstalowany:

```bash
jupyter lab
```

---

## Jak pracować z kursem

Przechodź przez lekcje w kolejności numerycznej.

W notebookach:

- uruchamiaj komórki skrótem **`Shift+Enter`**;
- wykonuj komórki od góry do dołu;
- ćwiczenia są oznaczone jako `✅ Задание N.M`;
- miejsce na własne rozwiązanie jest oznaczone jako `# Ваше решение`;
- rozwiązanie wzorcowe jest oznaczone jako `# Правильное решение`;
- weryfikacja odbywa się najczęściej przez `@assert` lub inną wykonywalną kontrolę.

Poprawnie wykonany `@assert` zwykle nie generuje żadnego wyjścia.

Niektóre wyjątki są wywoływane **celowo w celach dydaktycznych**. W takich miejscach przyczyna błędu jest wyjaśniona bezpośrednio obok odpowiedniej komórki.

---

## Odtwarzalność

Kurs został zaprojektowany tak, aby uruchamianie notebooków nie modyfikowało w sposób niejawny środowiska samego repozytorium.

Demonstracje zarządzania pakietami używają, gdy jest to potrzebne, środowisk izolowanych lub tymczasowych, a wbudowany walidator sprawdza kluczowe niezmienniki projektu.

Kanoniczne środowisko definiują:

- [`Project.toml`](Project.toml)
- [`Manifest.toml`](Manifest.toml)

Wszystkie 13 notebooków zostało wykonanych od początku do końca w środowisku Julia 1.11.3.

---

## Walidacja kursu

Repozytorium zawiera walidator całego kursu:

```bash
python3 tools/check_course.py
```

Sprawdza on między innymi:

- poprawność JSON notebooków;
- zgodność kernela Julia;
- kolejność `execution_count`;
- brak nieoczekiwanych błędów w outputach;
- obecność celów lekcji i nawigacji;
- strukturę „ćwiczenie / rozwiązanie”;
- poprawność numeracji ćwiczeń;
- wewnętrzne linki;
- brak absolutnych ścieżek lokalnych;
- brak przypadkowo ujawnionych sekretów lub danych przypominających credentials.

Sam walidator jest dodatkowo testowany na celowo uszkodzonych przypadkach:

```bash
python3 tools/test_check_course.py
```

Kontrole te są zintegrowane z CI.

---

## Uwagi dotyczące uruchamiania

### Celowe wyjątki

Niektóre lekcje celowo wywołują wyjątki, aby pokazać zachowanie Julii, między innymi:

- `MethodError`
- `ParseError`
- `StringIndexError`
- `KeyError`
- `DimensionMismatch`
- `PosDefException`

Takie błędy są uznawane za poprawne wyłącznie wtedy, gdy są jawnie wyjaśnione w treści lekcji obok odpowiedniej komórki.

### `PyCall` w lekcji 10

Na niektórych systemach Linux `PyCall` może nie zbudować się poprawnie, jeśli wybrana instalacja Pythona nie udostępnia zgodnej współdzielonej biblioteki `libpython`.

Jeśli wystąpi taki błąd, można przebudować `PyCall` z użyciem zarządzanego środowiska Pythona:

```julia
ENV["PYTHON"] = ""
using Pkg
Pkg.build("PyCall")
```

Następnie uruchom ponownie kernel Julii.

Stosuj to obejście tylko wtedy, gdy rzeczywiście pojawi się odpowiadający mu błąd kompilacji.

---

## Jakość repozytorium

Obecna edycja kursu została zweryfikowana pod kątem:

- zgodności z Julia 1.11.3;
- poprawności matematycznej;
- poprawności numerycznej algebry liniowej;
- semantyki wielokrotnej dyspozycji;
- indeksowania UTF-8 w napisach;
- odtwarzalności środowiska pakietów;
- kolejności wykonania komórek;
- kompletności ćwiczeń;
- rozdzielenia błędów celowych i przypadkowych;
- braku wycieków lokalnych ścieżek i danych uwierzytelniających;
- spójności dydaktycznej wszystkich 13 lekcji.

Szczegółową historię audytu znajdziesz w:

---

## Współtworzenie projektu

Issues i pull requesty są mile widziane.

Przed wysłaniem zmian:

1. uruchom ponownie kernel zmodyfikowanego notebooka;
2. wykonaj notebook od początku do końca;
3. upewnij się, że zapisane outputy odpowiadają aktualnemu kodowi;
4. uruchom:

```bash
python3 tools/check_course.py
python3 tools/test_check_course.py
```

Unikaj niezwiązanych ze zmianą modyfikacji formatowania JSON notebooków, ponieważ znacząco utrudniają one code review.

---

## Licencjonowanie

Repozytorium korzysta z podwójnego modelu licencjonowania.

| Materiał | Licencja | Zakres |
|---|---|---|
| Kod źródłowy | [MIT License](LICENSE) | Komórki z kodem Julia, skrypty pomocnicze, konfiguracja CI, pliki środowiska |
| Materiały kursowe | [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA.md) | Tekst lekcji, wyjaśnienia, ćwiczenia, diagramy, obrazy, README |

Licencja **CC BY-NC-SA 4.0** wymaga podania autorstwa, zabrania użycia komercyjnego bez odrębnego zezwolenia i wymaga rozpowszechniania utworów zależnych na tych samych warunkach.

Komercyjne wykorzystanie materiałów kursowych — w tym płatne szkolenia, warsztaty korporacyjne lub włączenie kursu do odpłatnego produktu edukacyjnego — wymaga odrębnej pisemnej zgody właściciela praw.

### Prawa autorskie

- Copyright © 2018–2020 Julia Computing, Inc. — oryginalne materiały JuliaAcademy *Introduction to Julia*.
- Copyright © 2026 Siergej Sobolewski — rosyjska adaptacja, modernizacja i dodatkowe materiały kursowe.

---

## Podziękowania

Kurs bazuje na pracy społeczności Julia oraz zespołu JuliaAcademy.

Szczególne podziękowania dla:

- **[Julia Computing](https://juliacomputing.com/)** i zespołu JuliaAcademy — za oryginalny kurs *Introduction to Julia*;
- **[Andreas Noack Jensen](https://x.com/anoackjensen)** — za oryginalne materiały dotyczące algebry liniowej i faktoryzacji wykorzystane przy opracowywaniu późniejszych lekcji;
- **społeczności Julia** — za język, dokumentację, pakiety i ekosystem wykorzystany w kursie.

---

## Utrzymanie kursu

Cartesian School

Repozytorium: [github.com/Cartesian-School/Introduction-to-Julia](https://github.com/Cartesian-School/Introduction-to-Julia)

Jeśli znajdziesz błąd, chcesz zaproponować poprawkę lub usprawnienie kursu — utwórz GitHub Issue lub Pull Request.

---

<div align="center">

[English](README.md) · [Русский](README.ru.md) · **Polski**

</div>
