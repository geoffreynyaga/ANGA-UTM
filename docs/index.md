# ANGA UTM

[![Netlify Status](https://api.netlify.com/api/v1/badges/983d87b3-d3db-4930-bb69-df26e1c444a7/deploy-status)](https://app.netlify.com/sites/competent-wescoff-227917/deploys)

> `This is a LAANC (Low Altitude Authorization and Notification Capability) to UTM (UAV Traffic Management) implemetation for drones / UAS / RPAS. It includes drone Registrations, drone flight plans, drone Geofences and drone approvals`

`It is a PWA (Progressive Web App) purely done in Django/python`

![Anga UTM](screenshots/main.png)

## Overview

> The software is a LAANC implementation..
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

- `log in to the admin and under "Authentication and Authorization" create a group called CAA and give the group the relevant permissions that Civil Aviation requires e.g. changing reserved airspaces, adding/changing NOTAMs`

- `One more thing... By default, the application is country-specific, and the default country is Kenya, but this constraint can be removed.`

`If you log in the app, the map will awlays be bound to Kenyan borders. To cahnge this to another country, draw a box on Google maps/earth that covers the entire country of your choice. Then get the North East lattitude/longitude as well as South Eastern lat/long of the bounding box`

`An example for Kenya can be seen in the image below`

![Anga UTM country box](screenshots/bounds.png)

- Finally, take those values and insert them in `applications/templates/applications/airspaces.html` in this line

```javascript
bounds = new L.LatLngBounds(new L.LatLng(<northEastLatitude>,<northEastLongitude>), new L.LatLng(<southWestlattitude>,  <southWestLongitude>));
```

> Now the app should be working well. However, you will realise that you can not create a reserve airspace yet, and that you have to have an RPAS registered, which when you attempt does not go through because you are not registered to any organisation.
>
> This is a deliberate design choice, you have to register an organisation on the admin page `http://localhost:8000/admin` and add the user to that organisation. This is the supposed role that Civil Aviation bodies will have to play.
>
> Finally, you can create a user in the admin page and make sure to assign them to the `CAA` group that we created in on of the steps above. If you now login with this user on the site, you should have additional features such as `Approve Flight Plans`, `Create Notams` etc.
