# Installation

Build a virtualenv (python 3)

```
mkdir -p ~/ve/
cd ~/ve/
virtualenv -p python3 indexelect
source ~/ve/indexelect/bin/activate
```

Get code:
```
cd ~/workspace/
git clone https://github.com/matanz144/IndeXelect.git
```

Install dependencies:

```
cd ~/workspace/indexelect
pip install -r requirements.txt
```

Build basic database:

`./manage.py migrate`

# Testing

`./manage.py test indexelect_app.tests`
