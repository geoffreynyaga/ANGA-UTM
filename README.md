# ANGA UTM

![Build Status](https://github.com/geoffreynyaga/ANGA-UTM/workflows/Anga%20UTM%20CI/badge.svg)

[![Netlify Status](https://api.netlify.com/api/v1/badges/983d87b3-d3db-4930-bb69-df26e1c444a7/deploy-status)](https://app.netlify.com/sites/competent-wescoff-227917/deploys)

> `This is a LAANC (Low Altitude Authorization and Notification Capability) to UTM (UAV Traffic Management) implementation for drones / UAS / RPAS. It includes drone Registrations, drone flight plans, drone Geofences and drone approvals`

`It is a PWA (Progressive Web App) purely done in Django/python`

![Anga UTM](docs/screenshots/main.png)

> ## [Click here for a DEMO](https://anga-utm.herokuapp.com)
>
> NB: `To login as a normal user/pilot/ drone company staff use the following credentials to sign in`
>
> - username: `pilot`
> - password: `anga2020`
>
> `To login as a Civil Aviation staff use the following credentials to sign in`
>
> - username: `admin`
> - password: `aviation2020`
>
> Keep in mind the map is bound to Kenya and to change it see the end of this page

## Overview

> The software is a LAANC implementation.
>
> 1. Registration
> 2. Flight Plans submission and Authorization.
> 3. Geofences.
> 4. NOTAM and Notifications

## [Full Documentation ↗️🔗](https://competent-wescoff-227917.netlify.com/)

- [Registration](docs/registration.md)


    - [RPAS/UAS Registration](docs/registration.md#rpas-registration)

    - [Payload Registration](docs/registration.md#payload-registration)

    - [Personnel Registration and Profiles](docs/registration.md#personnel-registration-and-profiles)

    - [Organisation Registration](docs/registration.md#organization-registration)

- [Flight Plans](docs/flight-plans.md)


    - [Geofences](docs/flight-plans.md#geofences)

    - [Flight Areas](docs/flight-plans.md#flight-areas)

    - [NOTAMS](docs/flight-plans.md#notams)

    - [RPAS/UAS Selection](docs/flight-plans.md#rpasuas-selection)

- [Messages and Notifications](docs/messages.md)
- [Civil Aviation Approvals](docs/approvals.md)


    - [Approved Flights](docs/approvals.md#requested-flight-approvals-list)

    - [Pending Approvals](docs/approvals.md#requested-flight-details-page)

    - [Approval Section](docs/approvals.md#rapproval-section)

- [Company Management](docs/company.md)


    - [Postholds](docs/company.md#my-postholds)

    - [Flight Logs](docs/company.md#flight-logs)

## Install Instructions 📥

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

- `log in to the admin and under "Authentication and Authorization" create a group called CAA and give the group the relevant permissions that Civil Aviation requires e.g. changing reserved airspaces, adding/changing NOTAMs`

- `One more thing... By default, the application is meant to be country-specific, and the default country is Kenya (if you disable location on the browser), but this constraint can be removed.`

  #### MAP BOUNDS

  `If you log in the and not grant the location permission, the map will ALWAYS be bound to Kenyan borders. To change this to another country, accept the location on the browser and the map will be bound to your specific country`

  `An example for the extent on coverage if you are in Kenya can be seen in the image below`

  ![Anga UTM country box](docs/screenshots/bounds.png)

> Now the app should be working well. However, you will realise that you can not create a reserve airspace yet, and that you have to have an RPAS registered, which when you attempt does not go through because you are not registered to any organisation.
>
> This is a deliberate design choice, you have to register an organisation on the admin page `http://localhost:8000/admin/` and add the user to that organisation. This is the supposed role that Civil Aviation bodies will have to play.
>
> Finally, you can create a user in the admin page and make sure to assign them to the `CAA` group that we created in on of the steps above. If you now login with this user on the site, you should have additional features such as `Approve Flight Plans`, `Create Notams` etc.
