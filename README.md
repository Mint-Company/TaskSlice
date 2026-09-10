# TaskSlice

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-PySide6-41CD52?style=flat-square&logo=qt&logoColor=white" alt="PySide6">
  <img src="https://img.shields.io/badge/Mobile-Flet-00B4AB?style=flat-square" alt="Flet">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/version-1.0.0-blue?style=flat-square" alt="Version">
</p>

<p align="center">
  <b>🇬🇧 <a href="#english">English</a> &nbsp;|&nbsp; 🇷🇺 <a href="#русский">Русский</a></b>
</p>

---

## English

### About

**TaskSlice** is a personal task planner focused on cutting big goals into small, manageable steps. The idea behind the project: procrastination and burnout usually come from vague, oversized tasks — TaskSlice helps you slice them down, track progress, and stay motivated with a lightweight leveling system.

The project has two independent implementations living side by side in this repository:

| Folder | Platform | Stack |
|---|---|---|
| [`TaskSlice-PC.V.P`](./TaskSlice-PC.V.P) | Desktop (Windows/Linux/macOS) | Python + PySide6 |
| [`TaskSlice-MD.V.F`](./TaskSlice-MD.V.F) | Mobile | Python + Flet |

Both versions share the same core idea and a SQLite database for local storage.

### Features

- ✅ Create, search, and delete tasks
- 📅 Separate views for **today**, **tomorrow**, and **general** tasks
- 🎯 Priority levels — low / medium / high
- 🔎 Full-text search across all task tables
- ⌨️ Keyboard shortcut for quick task creation (`Ctrl+N`)
- 🏆 A small gamification layer: earn EXP and level up as you complete tasks
- 💾 Local SQLite storage — no account, no cloud, your data stays on your device

### Screenshots

> `![Main window(PC)](docs/screenshots/screenshots1.png)`
> `![Main window(MD)](docs/screenshots/screenshots2.png)`

### Installation — Desktop version (PySide6)

```bash
git clone https://github.com/Mint-Company/TaskSlice.git
cd TaskSlice/TaskSlice-PC.V.P
pip install -r requirements.txt
python main.py
```

> Adjust the entry-point filename and `requirements.txt` path above if they differ in your project layout.

### Installation — Mobile version (Flet)

```bash
git clone https://github.com/Mint-Company/TaskSlice.git
cd TaskSlice/TaskSlice-MD.V.F
pip install -r requirements.txt
flet run main.py
```

### License

This project doesn't yet declare a license. Until one is added, all rights are reserved by the author — consider adding a `LICENSE` file (e.g. MIT) if you want others to freely reuse the code.

### Author

Developed by [Mint-Company](https://github.com/Mint-Company).

---

## Русский

### О проекте

**TaskSlice** — персональный планировщик задач, построенный вокруг простой идеи: любую большую цель можно и нужно "нарезать" на маленькие, понятные шаги. Прокрастинация и выгорание чаще всего возникают из-за расплывчатых и слишком крупных задач — TaskSlice помогает разбить их, отслеживать прогресс и не терять мотивацию за счёт лёгкой системы уровней.

В репозитории живут две независимые версии приложения:

| Папка | Платформа | Стек |
|---|---|---|
| [`TaskSlice-PC.V.P`](./TaskSlice-PC.V.P) | Десктоп (Windows/Linux/macOS) | Python + PySide6 |
| [`TaskSlice-MD.V.F`](./TaskSlice-MD.V.F) | Мобильные устройства | Python + Flet |

Обе версии используют общую идею и локальную базу данных SQLite.

### Возможности

- ✅ Создание, поиск и удаление задач
- 📅 Отдельные вкладки для задач на **сегодня**, **завтра** и **общих** задач
- 🎯 Приоритеты — низкий / средний / высокий
- 🔎 Поиск по всем таблицам задач
- ⌨️ Быстрое создание задачи по горячей клавише (`Ctrl+N`)
- 🏆 Лёгкая геймификация: за выполненные задачи начисляется EXP и растёт уровень
- 💾 Локальное хранение в SQLite — без аккаунта и облака, данные остаются на устройстве

### Screenshots

> `![Главное окно(ПК)](docs/screenshots/screenshots1.png)`
> `![Главное окно(МБ](docs/screenshots/screenshots2.png)`


### Установка — Десктопная версия (PySide6)

```bash
git clone https://github.com/Mint-Company/TaskSlice.git
cd TaskSlice/TaskSlice-PC.V.P
pip install -r requirements.txt
python main.py
```


### Установка — Мобильная версия (Flet)

```bash
git clone https://github.com/Mint-Company/TaskSlice.git
cd TaskSlice/TaskSlice-MD.V.F
pip install -r requirements.txt
flet run main.py
```

### Лицензия

Проект пока не имеет объявленной лицензии. До её добавления все права сохраняются за автором.

### Автор

Разработано [Mint-Company](https://github.com/Mint-Company).