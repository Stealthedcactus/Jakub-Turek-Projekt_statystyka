# Projekt_statystyka

Aby uruchomić serwer w dockerze należy wykonać polecenia:
1. docker build --tag flask-server .
2. docker run --name server -d -p 5000:5000 flask-server


# Opis plików
1. Model.py - główny skrypt, wczytuje nauczony model oraz obsługuje serwer Flask wraz z zapytaniami o płeć
2. Model_train.py - skrypt który pobiera listę polskich imion, trenuje model typu DecisionTreeClassifier oraz zapisuje go do pliku
3. model_trained.pkl - zapisany model za pomocą pakietu Pickle
4. database.db - baza danych sqlite, w której przechowywane są logi zapytań systemu - imię, płeć oraz data zapytania
5. templates - folder zawierający statyczne pliki .html
