## Dokumentacja użytkowa aplikacji

Aplikacja implementuje operacje związane z zarządzaniem wypożyczyalnią samochodów z perspektywy kierownika/pracownika obsługi klienta

### Aplikacja umożliwia poprzez poszczególne podstrony następne operacje :
#### Część operacyjna:
- Dodanie samochodu:
  - Wybór segmentu, producenta oraz modelu z dostępnych w bazie danych
  - Należy podać: rok produkcji, przebieg, vin oraz numer rejestracyjny pojazdu
- Przegląd samochodów posiadanych przez wypożyczalnię wraz z ich stanem wypożyczenia
- Zarządzanie danymi samochodu, można zmienić przebieg, numer rejestracyjny oraz vin
- Wypożyczenie samochodu klientowi:
  - Z listy samochodów należy wybrać dostępny samochód
  - Następnie należy podać pesel (w przypadku osoby fizycznej) lub nip (w przypadku firmy) klienta oraz przewidywany czas zakończenia wypożyczenia
- Zwrócenie wypożyczenia:
  - Należy podać dane klienta
  - Następnie należy wybrać samochód spośród wypożyczonych przez klienta
- Utworzenie faktury dla klienta za okres 
  - Należy podać dane klienta oraz okres za który chcemy rozliczyć klienta
  - Aplikacja wygeneruje fakturę sumującą zakończone wypożyczenia klienta z tego okresu
- Przegląd faktur klienta
  - Należy podać dane klienta, aplikacja wyświetli wszystkie faktury wystawione na klienta 
- Zarządzanie cenami
  - Należy wybrać model samochodu 
  - Należy podać cenę za wypożyczenie samochodu na jeden dzień 
- Zarządzanie klientami
  - Umożliwia zmianę danych klientów obecnych w bazie poprzez wybór z listy
  - Umożliwia dodanie nowego klienta przez podanie jego danych

#### Część analityczno-raportowa:
- Raporty miesięczne 
  - Należy podać miesiąc oraz rok 
  - Aplikacja wyświetli sumę z wystawionych w tym miesiącu faktur
- Raporty roczne
  - Analogicznie jak miesięczne
- Raporty odnośnie wypożyczeń poszczególnych samochodów (ile razy, suma dni, zysk)