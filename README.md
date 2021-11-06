# Kanban board

## Description

A Kanban board is a simple form of task management. Every task that you add can
be in one of three states:

1. To do
2. Doing
3. Done

The kanban board allows a personalized board for unique users. A user can only see and move their personalized tasks on the board. 

### Implementation

This web app was developed with Flask and SQLAlchemy. The content of pages are stored in templates folder, and the stylings are stored in static folder. 

### Signup

To sign up, you need to provide following information:

1. Username (unique)
2. Email (unique)
3. Password (min.length(4), max.length(50))


#### macOS
```python3
python3.6 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3.6 app.py
```

#### Windows
```python3
python3.6 -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3.6 app.py
```

#### Testing (not implemented yet)

```python3
python3.6 -m unittest discover test
```
