<div align="center">

<img src="https://github.com/Cartesian-School/Julia-from-zero/blob/main/assets/images/kurs_logo.png" alt="Julia language logo" width="420" />

# Julia od zera

## Programowanie, obliczenia naukowe i metody numeryczne w Julia

**Praktyczny kurs dla programistów — od podstaw języka do projektu końcowego.**

[![Course CI](https://github.com/Cartesian-School/Julia-from-zero/actions/workflows/ci.yaml/badge.svg?branch=main&event=push)](https://github.com/Cartesian-School/Julia-from-zero/actions/workflows/ci.yaml)
[![Code License: MIT](https://img.shields.io/badge/code%20license-MIT-yellow.svg)](LICENSE)
[![Course Content: CC BY-NC-SA 4.0](https://img.shields.io/badge/course%20content-CC%20BY--NC--SA%204.0-lightgrey.svg)](LICENSE-CC-BY-NC-SA.md)
[![Julia](https://img.shields.io/badge/Julia-1.11.x-9558B2.svg)](https://julialang.org/)
![Lessons](https://img.shields.io/badge/lessons-15-blue.svg)
![Language](https://img.shields.io/badge/course%20language-Polish-red.svg)

**Polski** · [English](README.md) · [Русский](README.ru.md)

</div>

---

## O kursie

**Julia od zera** to praktyczny kurs języka Julia przygotowany przez **Cartesian School** dla osób, które znają już podstawowe pojęcia programistyczne i chcą nauczyć się Julii od początku — od składni i struktur danych po programowanie wysokiej wydajności, algebrę liniową, metody numeryczne i kompletny projekt końcowy.

„Od zera” oznacza tutaj **od zera w języku Julia**, a nie pierwszy kontakt z programowaniem. Kurs nie wymaga wcześniejszej znajomości Julii, ale zakłada rozumienie takich pojęć jak zmienna, funkcja, pętla, instrukcja warunkowa i podstawowy typ danych.

Kurs zawiera **15 lekcji, numerowanych od Lesson 0 do Lesson 14**. Materiał prowadzi od pierwszego notebooka do projektu **ThermalLab**, który łączy modelowanie, multiple dispatch, wizualizację, analizę wydajności, algebrę liniową i metody numeryczne.

Polska wersja kursu znajduje się w katalogu [`PL/`](PL/), a rosyjska wersja kursu w katalogu [`RU/`](RU/).

---

## Publiczny kurs i cel projektu

Repozytorium jest publicznie dostępne, aby ułatwić naukę Julii i przyczynić się do popularyzacji języka oraz jego ekosystemu — szczególnie wśród polskojęzycznych programistów, studentów i inżynierów.

Autor kursu chce w ten sposób wspierać społeczność Julia poprzez:

- tworzenie dostępnych materiałów edukacyjnych w języku polskim;
- pokazywanie praktycznych zastosowań Julii w programowaniu, obliczeniach naukowych i metodach numerycznych;
- udostępnianie przykładów, ćwiczeń i projektów, które można samodzielnie uruchamiać i analizować;
- zachęcanie do dalszej pracy z oficjalną dokumentacją i pakietami ekosystemu Julia.

### Ważne rozróżnienie licencyjne

Kod autorstwa Cartesian School jest udostępniany na licencji **MIT** i ma charakter open source.

Autorskie materiały dydaktyczne Cartesian School są udostępniane na licencji **CC BY-NC-SA 4.0**. Oznacza to, że można je kopiować, adaptować i rozwijać zgodnie z warunkami tej licencji, w tym z obowiązkiem atrybucji i ograniczeniem zastosowań komercyjnych.

Materiały pochodzące ze źródeł zewnętrznych pozostają objęte ich własnymi licencjami i wymaganiami dotyczącymi atrybucji.

---

## Czego nauczysz się w tym kursie

Po ukończeniu kursu będziesz potrafić:

- pisać czytelny i idiomatyczny kod w Julia;
- pracować z napisami Unicode, krotkami, słownikami, zbiorami, wektorami i macierzami;
- stosować pętle, warunki, comprehensions, broadcasting i iteratory;
- projektować funkcje z argumentami pozycyjnymi, nazwanymi, domyślnymi i varargs;
- rozumieć różnicę między funkcją a metodą;
- wykorzystywać **multiple dispatch** jako mechanizm projektowania rozszerzalnego API;
- zarządzać pakietami i środowiskami przez `Pkg`, `Project.toml` i `Manifest.toml`;
- tworzyć wykresy i analizować dane z użyciem `Plots.jl`;
- poprawnie mierzyć wydajność i interpretować benchmarki;
- rozpoznawać wpływ JIT, alokacji, stabilności typów i lokalności pamięci;
- wykonywać praktyczne obliczenia algebry liniowej;
- rozwiązywać układy równań przez operator `\`;
- stosować LU, QR, Cholesky, SVD, EVD i rozkład Schura;
- rozumieć specjalne struktury macierzy;
- analizować błędy numeryczne, conditioning i stabilność;
- implementować podstawowe metody znajdowania miejsc zerowych, całkowania i różniczkowania numerycznego;
- rozwiązywać proste ODE metodami Eulera i RK4;
- zbudować kompletny projekt łączący model danych, algorytmy, testy, wydajność, wizualizację i raportowanie.

---

## Dla kogo jest ten kurs

Kurs jest przeznaczony przede wszystkim dla:

- programistów Python, C, C++, Rust, Java, MATLAB, R i innych języków;
- studentów i absolwentów kierunków technicznych;
- inżynierów pracujących z modelowaniem i obliczeniami;
- osób zainteresowanych scientific computing, analizą danych i metodami numerycznymi;
- programistów, którzy chcą zrozumieć charakterystyczny dla Julii model programowania oparty na multiple dispatch.

### Wymagania wstępne

| Wymaganie | Poziom |
|---|---|
| Podstawy programowania | **Wymagane** |
| Wcześniejsza znajomość Julia | **Nie jest wymagana** |
| Jupyter Notebook / JupyterLab | Pomocne, ale niewymagane |
| Algebra liniowa | Pomocna od Lesson 10; podstawy są omawiane w kursie |
| Metody numeryczne | Niewymagane; wprowadzane w Lesson 13 |

---

## Struktura kursu

### Blok I — Fundamenty języka Julia

| Lesson | Temat | Notebook |
|---:|---|---|
| 0 | **Getting Started** | [Otwórz Lesson 0](PL/Lesson_0_Julia_Cartesian_School_PL.ipynb) |
| 1 | **Strings** | [Otwórz Lesson 1](PL/Lesson_1_Strings_Julia_Cartesian_School_PL.ipynb) |
| 2 | **Data Structures** | [Otwórz Lesson 2](PL/Lesson_2_Data_Structures_Julia_Cartesian_School_PL.ipynb) |
| 3 | **Loops** | [Otwórz Lesson 3](PL/Lesson_3_Loops_Julia_Cartesian_School_PL.ipynb) |
| 4 | **Conditionals** | [Otwórz Lesson 4](PL/Lesson_4_Conditionals_Julia_Cartesian_School_PL.ipynb) |
| 5 | **Functions** | [Otwórz Lesson 5](PL/Lesson_5_Functions_Julia_Cartesian_School_PL.ipynb) |

### Blok II — Ekosystem, wizualizacja i model programowania Julii

| Lesson | Temat | Notebook |
|---:|---|---|
| 6 | **Packages** | [Otwórz Lesson 6](PL/Lesson_6_Packages_Julia_Cartesian_School_PL.ipynb) |
| 7 | **Plotting** | [Otwórz Lesson 7](PL/Lesson_7_Plotting_Julia_Cartesian_School_PL.ipynb) |
| 8 | **Multiple Dispatch** | [Otwórz Lesson 8](PL/Lesson_8_Multiple_Dispatch_Julia_Cartesian_School_PL.ipynb) |

### Blok III — Wydajność i algebra liniowa

| Lesson | Temat | Notebook |
|---:|---|---|
| 9 | **Julia is Fast** | [Otwórz Lesson 9](PL/Lesson_9_Julia_is_Fast_Cartesian_School_PL.ipynb) |
| 10 | **Linear Algebra Concepts** | [Otwórz Lesson 10](PL/Lesson_10_Linear_Algebra_Concepts_Julia_Cartesian_School_PL.ipynb) |
| 11 | **Linear Algebra in Julia** | [Otwórz Lesson 11](PL/Lesson_11_Linear_Algebra_in_Julia_Cartesian_School_PL.ipynb) |
| 12 | **Factorizations and Other Fun** | [Otwórz Lesson 12](PL/Lesson_12_Factorizations_and_Other_Fun_Julia_Cartesian_School_PL.ipynb) |

### Blok IV — Metody numeryczne i projekt końcowy

| Lesson | Temat | Notebook |
|---:|---|---|
| 13 | **Numerical Computing** | [Otwórz Lesson 13](PL/Lesson_13_Numerical_Computing_Julia_Cartesian_School_PL.ipynb) |
| 14 | **Final Project / Capstone — ThermalLab** | [Otwórz Lesson 14](PL/Lesson_14_Final_Project_Capstone_Julia_Cartesian_PL.ipynb) |

---

## Projekt końcowy — ThermalLab

Lesson 14 jest projektem integrującym materiał z całego kursu.

**ThermalLab** modeluje proces chłodzenia zgodnie z prawem Newtona i obejmuje:

- własne typy `ThermalModel`, `MeasurementSet` i `SimulationResult`;
- abstrakcyjny interfejs integratora;
- implementacje Euler i RK4 przez multiple dispatch;
- generowanie syntetycznych danych pomiarowych;
- estymację parametru modelu przez least squares;
- residuals, MAE, RMSE i `R²`;
- porównanie dokładności i kosztu obliczeń;
- opcjonalne wykresy przez `Plots.jl`;
- eksport wyników do CSV;
- testy kontraktowe i walidację danych.

Projekt pokazuje pełny przepływ:

> **problem → model → kod → obliczenia → walidacja → wynik**

---

## Język kursu

Kanoniczne wersje dydaktyczne znajdują się w katalogach [`PL/`](PL/) i [`RU/`](RU/).

Tekst lekcji jest przygotowany po polsku. Kod Julia, nazwy funkcji, API, identyfikatory i techniczne terminy wymagające zgodności z dokumentacją pozostają w języku angielskim.

Dokumentacja repozytorium jest rozwijana w trzech wersjach:

- **English:** [README.md](README.md)
- **Polski:** [README.pl.md](README.pl.md)
- **Русский:** [README.ru.md](README.ru.md)

---

## Instalacja

### 1. Zainstaluj Julię

Kurs jest rozwijany dla serii **Julia 1.11.x**.

Oficjalne instrukcje instalacji:

<https://julialang.org/downloads/>

Po instalacji sprawdź:

```bash
julia --version
```

### 2. Sklonuj repozytorium

```bash
git clone https://github.com/Cartesian-School/Julia-from-zero.git
cd Julia-from-zero
```

### 3. Odtwórz środowisko

```bash
julia --project=. -e 'using Pkg; Pkg.instantiate()'
```

Repozytorium wykorzystuje:

- `Project.toml` — deklarowane zależności;
- `Manifest.toml` — rozwiązane wersje zależności.

### 4. Uruchom Jupyter

Jeżeli używasz IJulia:

```bash
julia --project=. -e 'using IJulia; notebook(dir=".")'
```

lub:

```bash
jupyter lab
```

Po uruchomieniu przejdź do wybranego katalogu językowego i rozpocznij od Lesson 0:

[`PL/Lesson_0_Julia_Cartesian_School_PL.ipynb`](PL/Lesson_0_Julia_Cartesian_School_PL.ipynb)
[`RU/Lesson_0_Julia_Cartesian_School_RU.ipynb`](RU/Lesson_0_Julia_Cartesian_School_RU.ipynb)

---

## Jak pracować z kursem

Przechodź przez notebooki od **Lesson 0** do **Lesson 14**.

Zalecany sposób pracy:

1. przeczytaj cel sekcji;
2. uruchom przykład;
3. przeanalizuj wynik;
4. wykonaj zadanie samodzielnie;
5. dopiero potem porównaj rozwiązanie;
6. sprawdź `@assert` i checkpoint;
7. przed przejściem dalej upewnij się, że rozumiesz przyczynę działania kodu, nie tylko jego składnię.

W kursie stosowany jest wspólny schemat:

| Element | Znaczenie |
|---|---|
| **Cel** | rezultat danego fragmentu |
| **Teoria** | definicja lub reguła |
| **Przykład** | wykonywalny kod |
| **Analiza** | interpretacja działania |
| **Ważne** | istotna zasada |
| **Typowy błąd** | częsty problem |
| **Spróbuj sam** | krótki eksperyment |
| **Praktyka** | zadanie |
| **Podsumowanie** | najważniejsze wnioski |

---

## Odtwarzalność i bezpieczeństwo środowiska

Kurs jest projektowany tak, aby przykłady dotyczące pakietów nie modyfikowały niejawnie środowiska projektu.

W szczególności:

- notebook nie powinien automatycznie wykonywać `Pkg.add(...)` bez wyraźnej potrzeby;
- eksperymenty z pakietami mogą używać środowisk tymczasowych;
- zależności projektu należy odtwarzać przez `Pkg.instantiate()`;
- kod korzystający z pakietów opcjonalnych powinien zachowywać się przewidywalnie również wtedy, gdy pakiet nie jest zainstalowany.

---

## Walidacja repozytorium

Repozytorium posiada workflow CI w `.github/workflows/ci.yaml`.

Jeżeli w repozytorium dostępne są narzędzia:

```bash
python3 tools/check_course.py
python3 tools/test_check_course.py
```

należy uruchamiać je przed scaleniem zmian do `main`.

Po zmianach w notebookach należy również:

1. uruchomić notebook od początku do końca;
2. sprawdzić brak nieoczekiwanych wyjątków;
3. zweryfikować nawigację i linki;
4. sprawdzić zgodność środowiska;
5. upewnić się, że CI obejmuje aktualny zestaw polskich notebooków.

**README nie powinien twierdzić, że wszystkie 15 lekcji przeszły wykonanie end-to-end, dopóki aktualna wersja repozytorium nie została w ten sposób zweryfikowana.**

---

## Jakość techniczna

Przy rozwijaniu kursu zwracamy szczególną uwagę na:

- poprawność semantyki Julia;
- poprawność przykładów API;
- prawidłową pracę z Unicode;
- rozróżnienie broadcastingu i algebry liniowej;
- prawidłowe użycie multiple dispatch;
- rzetelną metodologię benchmarkingu;
- rozróżnienie stabilności algorytmu od conditioning problemu;
- poprawność numeryczną;
- niewprowadzające w błąd porównania wydajności;
- reprodukowalne środowiska;
- spójność dydaktyczną Lesson 0–14.

---

## Pochodzenie materiałów i atrybucja

Historyczna baza części repozytorium wywodzi się z materiałów edukacyjnych JuliaAcademy / JuliaTutorials.

Obecna edycja **Julia od zera** została znacząco przebudowana i rozszerzona przez Cartesian School: zmieniono strukturę dydaktyczną, język, ćwiczenia, zakres tematyczny i organizację materiału, a także dodano nowe treści dotyczące wydajności, algebry liniowej, faktoryzacji, metod numerycznych i projektu końcowego.

Materiały zewnętrzne zachowują swoje pierwotne prawa autorskie, warunki licencyjne i wymagania atrybucji.

Repozytorium Cartesian School nie jest oficjalnym kursem projektu Julia ani oficjalnym produktem JuliaHub.

---

## Licencjonowanie

| Materiał | Licencja |
|---|---|
| Kod autorstwa Cartesian School | [MIT License](LICENSE) |
| Autorskie materiały dydaktyczne Cartesian School | [CC BY-NC-SA 4.0](LICENSE-CC-BY-NC-SA.md) |
| Materiały zewnętrzne | zgodnie z ich własnymi licencjami i wymaganiami atrybucji |

Licencja dotycząca materiałów Cartesian School nie zastępuje licencji materiałów stron trzecich.

---

## Współtworzenie projektu

Issues i pull requesty są mile widziane.

Przed wysłaniem zmian:

1. wykonaj zmieniony notebook od początku do końca;
2. sprawdź aktualność zapisanych wyników;
3. uruchom walidatory repozytorium;
4. zweryfikuj linki Markdown;
5. unikaj przypadkowych zmian formatowania JSON notebooków;
6. nie dodawaj lokalnych ścieżek, sekretów, tokenów ani danych uwierzytelniających.

---

## Kontakt

**Autor:** Siergej Sobolewski  
**Projekt:** Cartesian School  
**E-mail:** [s.sobolewski@hotmail.com](mailto:s.sobolewski@hotmail.com)

Repozytorium:

<https://github.com/Cartesian-School/Julia-from-zero>

Jeżeli znajdziesz błąd merytoryczny, techniczny, językowy lub numeryczny, możesz:

- utworzyć GitHub Issue;
- wysłać Pull Request;
- skontaktować się z autorem drogą e-mailową.

---

## Podziękowania

Dziękujemy:

- twórcom języka Julia;
- społeczności Julia;
- autorom oficjalnej dokumentacji i pakietów;
- autorom materiałów JuliaAcademy / JuliaTutorials, od których historycznie rozpoczęła się część tego repozytorium.

---

<div align="center">

### Cartesian School

**Learn Programming. Build Real Software. Master AI.**

[English](README.md) · [Русский](README.ru.md) · **Polski**

</div>
