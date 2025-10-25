# ISS Orbit Tracker

Программа для получения координат Международной космической станции (МКС) и отображения её орбиты на карте Земли.

## Возможности
- Получение текущих координат МКС в реальном времени
- Получение времени следующих пролетов над текущей точкой
- Построение красивой карты с орбитой МКС

## Установка
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Использование
```bash
python main.py
```

## Зависимости
- requests — для получения данных по API
- matplotlib — для построения графиков
- cartopy — для отображения карты Земли

## Источники данных
- API [Open Notify](http://api.open-notify.org/)
