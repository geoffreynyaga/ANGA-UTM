## Install Instructions

> The new version of the app works best on linux/MacOS environment. For windows installation, kindly check out the official Django documentation to install GEOS and GDAL libraries and how to configure them.

#### Steps

- Clone the repo
  ```bash
  git clone https://github.com/geoffreynyaga/ANGA-UTM.git
  ```
- create a python virtualenvironment
  ```bash
  virtualenv venv
  ```
- activate the virtualenvironment
  ```bash
  source venv/bin/activate
  ```
- install python packages

  ```bash
  pip install -r requirements.txt
  ```

- install geojango Geospatial Libraries packages

  ```bash
  sudo apt-get install binutils libproj-dev gdal-bin
  ```

- create a postgres database on called "anga_utm" or equivalently, give it a custom name and make sure to change the value in the local2.py settings file

- run migrations

  ```python
  python manage.py migrate
  ```

- create superuser
  ```python
  python manage.py createsuperuser
  ```
- log in to the admin and under "Authentication and Authorization" create a group called KCAA and give the group the relevant permissions that Civil Aviation requires e.g. changing reserved airspaces, adding/changing NOTAMs
