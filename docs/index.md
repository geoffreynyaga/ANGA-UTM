#ANGA UTM

[![Netlify Status](https://api.netlify.com/api/v1/badges/983d87b3-d3db-4930-bb69-df26e1c444a7/deploy-status)](https://app.netlify.com/sites/competent-wescoff-227917/deploys)

> `This is a LAANC (Low Altitude Authorization and Notification Capability) to UTM (UAV Traffic Management) implemetation for drones / UAS / RPAS. It includes drone Registrations, drone flight plans, drone Geofences and drone approvals`

![Anga UTM](screenshots/main.png)

## Overview

> The software is a LAANC implementation. LAANC is Low Altitude Airspace Authorization and Notifications.
>
> 1. Registration
> 2. Flight Plans submission and Authorization.
> 3. Geofences.
> 4. NOTAM and Notifications

## [Full Documentation ↗️🔗](https://competent-wescoff-227917.netlify.com/)

- [Registration](registration.md)


    - [RPAS/UAS Registration](registration.md#rpas-registration)

    - [Payload Registration](registration.md#payload-registration)

    - [Personnel Registration and Profiles](registration.md#personnel-registration-and-profiles)

    - [Organisation Registration](registration.md#organization-registration)

- [Flight Plans](flight-plans.md)


    - [Geofences](flight-plans.md#geofences)

    - [Flight Areas](flight-plans.md#flight-areas)

    - [NOTAMS](flight-plans.md#notams)

    - [RPAS/UAS Selection](flight-plans.md#rpasuas-selection)

- [Messages and Notifications](messages.md)
- [Civil Aviation Approvals](approvals.md)


    - [Approved Flights](approvals.md#requested-flight-approvals-list)

    - [Pending Approvals](approvals.md#requested-flight-details-page)

    - [Approval Section](approvals.md#approval-section)

- [Company Management](company.md)


    - [Postholds](company.md#my-postholds)

    - [Flight Logs](company.md#flight-logs)

## Install Instructions

> The new version of the app works best on linux/MacOS environment. For windows installation, kindly check out the official [Django documentation](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/#windows) to install GEOS and GDAL libraries and how to configure them. Alternatively, I can recommend you install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) and use the Ubuntu environment inorder to install the dependacies using the steps below

#### Steps

- `Clone the repo`

```bash
git clone https://github.com/geoffreynyaga/ANGA-UTM.git
```

- `create a python virtualenvironment`

```bash
virtualenv venv
```

- `activate the virtualenvironment`

```bash
source venv/bin/activate
```

- `install python packages`

```bash
pip install -r requirements.txt
```

- `install geojango Geospatial Libraries packages`

```bash
sudo apt-get install binutils libproj-dev gdal-bin
```

- `create a postgres database on called "anga_utm" or equivalently give it a custom name and make sure to change the value in the local.py settings file`

- `run migrations`

```bash
python manage.py migrate
```

- `create superuser`

```bash
  python manage.py createsuperuser
```

- `log in to the admin and under "Authentication and Authorization" create a group called KCAA and give the group the relevant permissions that Civil Aviation requires e.g. changing reserved airspaces, adding/changing NOTAMs`
