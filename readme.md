### 1. Системные требования:
* Linux(Debian based), Docker, Python 3.x, pip, Chrome browser. Всё, кроме Docker, можно установить запустив *install_dependencies.sh*:
``` sudo install_dependencies.sh ```
* Библиотеки python 3 из файла *requirements.txt*

### 2. Запуск
Строка запуска следующего вида:
```
python3 -m pytest --password %sudo passwd% --browser %browser% 
```
Где *%sudo passwd%* -- пароль root ( нужен для назначения портов gitea ) и *%browser%* -- название браузера ( chrome или firefox, по дефолту chrome)

### 3. Структура проекта
* При написании проекта вдохновлялся паттерном Page Object
* Базовые методы pageobject'ов реализованны через __getattr__ метод, где первая часть названия метода ( click_, get_value_, etc) -- это действие, а вторая -- это название записи в файле locators.ini где хранятся xpath для практически всех веб-элементов.