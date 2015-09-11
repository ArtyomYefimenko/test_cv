1 Installation:

1) $ cd test_cv

2) $ virtualenv .env

3) $ source .env/bin/activate

4) $ cd app

5) $ pip install -r requirements.txt

6) $ ./manage.py collectstatic

7) $ ./manage.py runserver


P.S. To install PIL:

sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
sudo pip install Pillow
