# Software Engineering(Team 00-zero)

### Positions:
* President - Jacob Lebowitz
* Scrum Master - Luke
* Market Analyst - Chael
* Requirement Analyst - Rabah
* Developer - Jared
* Developer - Abbey
* Developer - Nick
* Developer - Jake
* Tester - Ryan K
* Tester - Ryan #2
* Operations Engineer - Kane

# Info
[Flask docs](http://exploreflask.com/en/latest/index.html)

[Flask tutorials](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

# Setup
Depending on your system you may need to use py or python3 instead of python
```
cd OOZero
pip install -r requirements.txt
python setup.py develop
or
python setup.py install
```
```
Windows Powershell: $env:FLASK_APP = "run"
Windows CMD: set FLASK_APP=run
Linux Bash: export FLASK_APP=run

flask run
```

# Testing
Automated unit tests are put in the OOZero/tests directory and should be named test____.py to be found by automatic test discovery. Use -b to suppress print statements
```
python setup.py test
```

# Maintance
New exteral library dependencies from PyPI must be added to requirements.txt on there own line
