#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##################################################################################
# File: /mnt/c/Projects/ANGA UTM/src/applications/models.py                      #
# Project: /mnt/c/Projects/ANGA UTM/src/applications                             #
# Created Date: Tuesday, March 17th 2020, 11:12:27 pm                            #
# Author: Geoffrey Nyaga Kinyua ( <geoffrey@geoffreynyaga.com> )                 #
# -----                                                                          #
# Last Modified: Tuesday March 17th 2020 11:12:27 pm                             #
# Modified By:  Geoffrey Nyaga Kinyua ( <geoffrey@geoffreynyaga.com> )           #
# -----                                                                          #
# Apache License                                                                 #
# Version 2.0, January 2004                                                      #
# http://www.apache.org/licenses/                                                #
#                                                                                #
# TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION                   #
#                                                                                #
# 1. Definitions.                                                                #
#                                                                                #
# "License" shall mean the terms and conditions for use, reproduction, and       #
# distribution as defined by Sections 1 through 9 of this document.              #
#                                                                                #
# "Licensor" shall mean the copyright owner or entity authorized by the copyright#
# owner that is granting the License.                                            #
#                                                                                #
# "Legal Entity" shall mean the union of the acting entity and all other entities#
# that control, are controlled by, or are under common control with that entity. #
# For the purposes of this definition, "control" means (i) the power, direct or  #
# indirect, to cause the direction or management of such entity, whether by      #
# contract or otherwise, or (ii) ownership of fifty percent (50%) or more of the #
# outstanding shares, or (iii) beneficial ownership of such entity.              #
#                                                                                #
# "You" (or "Your") shall mean an individual or Legal Entity exercising          #
# permissions granted by this License.                                           #
#                                                                                #
# "Source" form shall mean the preferred form for making modifications, including#
# but not limited to software source code, documentation source, and             #
# configuration files.                                                           #
#                                                                                #
# "Object" form shall mean any form resulting from mechanical transformation or  #
# translation of a Source form, including but not limited to compiled object     #
# code, generated documentation, and conversions to other media types.           #
#                                                                                #
# "Work" shall mean the work of authorship, whether in Source or Object form,    #
# made available under the License, as indicated by a copyright notice that is   #
# included in or attached to the work (an example is provided in the Appendix    #
# below).                                                                        #
#                                                                                #
# "Derivative Works" shall mean any work, whether in Source or Object form, that #
# is based on (or derived from) the Work and for which the editorial revisions,  #
# annotations, elaborations, or other modifications represent, as a whole, an    #
# original work of authorship. For the purposes of this License, Derivative Works#
# shall not include works that remain separable from, or merely link (or bind by #
# name) to the interfaces of, the Work and Derivative Works thereof.             #
#                                                                                #
# "Contribution" shall mean any work of authorship, including the original       #
# version of the Work and any modifications or additions to that Work or         #
# Derivative Works thereof, that is intentionally submitted to Licensor for      #
# inclusion in the Work by the copyright owner or by an individual or Legal      #
# Entity authorized to submit on behalf of the copyright owner. For the purposes #
# of this definition, "submitted" means any form of electronic, verbal, or       #
# written communication sent to the Licensor or its representatives, including   #
# but not limited to communication on electronic mailing lists, source code      #
# control systems, and issue tracking systems that are managed by, or on behalf  #
# of, the Licensor for the purpose of discussing and improving the Work, but     #
# excluding communication that is conspicuously marked or otherwise designated in#
# writing by the copyright owner as "Not a Contribution."                        #
#                                                                                #
# "Contributor" shall mean Licensor and any individual or Legal Entity on behalf #
# of whom a Contribution has been received by Licensor and subsequently          #
# incorporated within the Work.                                                  #
#                                                                                #
# 2. Grant of Copyright License. Subject to the terms and conditions of this     #
# License, each Contributor hereby grants to You a perpetual, worldwide,         #
# non-exclusive, no-charge, royalty-free, irrevocable copyright license to       #
# reproduce, prepare Derivative Works of, publicly display, publicly perform,    #
# sublicense, and distribute the Work and such Derivative Works in Source or     #
# Object form.                                                                   #
#                                                                                #
# 3. Grant of Patent License. Subject to the terms and conditions of this        #
# License, each Contributor hereby grants to You a perpetual, worldwide,         #
# non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this  #
# section) patent license to make, have made, use, offer to sell, sell, import,  #
# and otherwise transfer the Work, where such license applies only to those      #
# patent claims licensable by such Contributor that are necessarily infringed by #
# their Contribution(s) alone or by combination of their Contribution(s) with the#
# Work to which such Contribution(s) was submitted. If You institute patent      #
# litigation against any entity (including a cross-claim or counterclaim in a    #
# lawsuit) alleging that the Work or a Contribution incorporated within the Work #
# constitutes direct or contributory patent infringement, then any patent        #
# licenses granted to You under this License for that Work shall terminate as of #
# the date such litigation is filed.                                             #
#                                                                                #
# 4. Redistribution. You may reproduce and distribute copies of the Work or      #
# Derivative Works thereof in any medium, with or without modifications, and in  #
# Source or Object form, provided that You meet the following conditions:        #
#                                                                                #
#      (a) You must give any other recipients of the Work or Derivative Works a  #
# copy of this License; and                                                      #
#                                                                                #
#      (b) You must cause any modified files to carry prominent notices stating  #
# that You changed the files; and                                                #
#                                                                                #
#      (c) You must retain, in the Source form of any Derivative Works that You  #
# distribute, all copyright, patent, trademark, and attribution notices from the #
# Source form of the Work, excluding those notices that do not pertain to any    #
# part of the Derivative Works; and                                              #
#                                                                                #
#      (d) If the Work includes a "NOTICE" text file as part of its distribution,#
# then any Derivative Works that You distribute must include a readable copy of  #
# the attribution notices contained within such NOTICE file, excluding those     #
# notices that do not pertain to any part of the Derivative Works, in at least   #
# one of the following places: within a NOTICE text file distributed as part of  #
# the Derivative Works; within the Source form or documentation, if provided     #
# along with the Derivative Works; or, within a display generated by the         #
# Derivative Works, if and wherever such third-party notices normally appear. The#
# contents of the NOTICE file are for informational purposes only and do not     #
# modify the License. You may add Your own attribution notices within Derivative #
# Works that You distribute, alongside or as an addendum to the NOTICE text from #
# the Work, provided that such additional attribution notices cannot be construed#
# as modifying the License.                                                      #
#                                                                                #
#      You may add Your own copyright statement to Your modifications and may    #
# provide additional or different license terms and conditions for use,          #
# reproduction, or distribution of Your modifications, or for any such Derivative#
# Works as a whole, provided Your use, reproduction, and distribution of the Work#
# otherwise complies with the conditions stated in this License.                 #
#                                                                                #
# 5. Submission of Contributions. Unless You explicitly state otherwise, any     #
# Contribution intentionally submitted for inclusion in the Work by You to the   #
# Licensor shall be under the terms and conditions of this License, without any  #
# additional terms or conditions. Notwithstanding the above, nothing herein shall#
# supersede or modify the terms of any separate license agreement you may have   #
# executed with Licensor regarding such Contributions.                           #
#                                                                                #
# 6. Trademarks. This License does not grant permission to use the trade names,  #
# trademarks, service marks, or product names of the Licensor, except as required#
# for reasonable and customary use in describing the origin of the Work and      #
# reproducing the content of the NOTICE file.                                    #
#                                                                                #
# 7. Disclaimer of Warranty. Unless required by applicable law or agreed to in   #
# writing, Licensor provides the Work (and each Contributor provides its         #
# Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY    #
# KIND, either express or implied, including, without limitation, any warranties #
# or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A    #
# PARTICULAR PURPOSE. You are solely responsible for determining the             #
# appropriateness of using or redistributing the Work and assume any risks       #
# associated with Your exercise of permissions under this License.               #
#                                                                                #
# 8. Limitation of Liability. In no event and under no legal theory, whether in  #
# tort (including negligence), contract, or otherwise, unless required by        #
# applicable law (such as deliberate and grossly negligent acts) or agreed to in #
# writing, shall any Contributor be liable to You for damages, including any     #
# direct, indirect, special, incidental, or consequential damages of any         #
# character arising as a result of this License or out of the use or inability to#
# use the Work (including but not limited to damages for loss of goodwill, work  #
# stoppage, computer failure or malfunction, or any and all other commercial     #
# damages or losses), even if such Contributor has been advised of the           #
# possibility of such damages.                                                   #
#                                                                                #
# 9. Accepting Warranty or Additional Liability. While redistributing the Work or#
# Derivative Works thereof, You may choose to offer, and charge a fee for,       #
# acceptance of support, warranty, indemnity, or other liability obligations     #
# and/or rights consistent with this License. However, in accepting such         #
# obligations, You may act only on Your own behalf and on Your sole              #
# responsibility, not on behalf of any other Contributor, and only if You agree  #
# to indemnify, defend, and hold each Contributor harmless for any liability     #
# incurred by, or claims asserted against, such Contributor by reason of your    #
# accepting any such warranty or additional liability.                           #
#                                                                                #
# END OF TERMS AND CONDITIONS                                                    #
#                                                                                #
# APPENDIX: How to apply the Apache License to your work.                        #
#                                                                                #
# To apply the Apache License to your work, attach the following boilerplate     #
# notice, with the fields enclosed by brackets "[]" replaced with your own       #
# identifying information. (Don't include the brackets!)  The text should be     #
# enclosed in the appropriate comment syntax for the file format. We also        #
# recommend that a file or class name and description of purpose be included on  #
# the same "printed page" as the copyright notice for easier identification      #
# within third-party archives.                                                   #
#                                                                                #
# Copyright [yyyy] [name of copyright owner]                                     #
#                                                                                #
# Licensed under the Apache License, Version 2.0 (the "License");                #
# you may not use this file except in compliance with the License.               #
# You may obtain a copy of the License at                                        #
#                                                                                #
# http://www.apache.org/licenses/LICENSE-2.0                                     #
#                                                                                #
# Unless required by applicable law or agreed to in writing, software            #
# distributed under the License is distributed on an "AS IS" BASIS,              #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.       #
# See the License for the specific language governing permissions and            #
# limitations under the License.                                                 #
# -----                                                                          #
# Copyright (c) 2020 ANGA UTM.                                                   #
##################################################################################

from datetime import datetime, date, timedelta

from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models

# from django.contrib.gis.db.models import GeoManager
from django.db.models import Manager as GeoManager
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.utils.safestring import mark_safe


from maps.models import GeofenceLocations, LocationPoints

from notifications.send_a_notification import send_a_notification
from rpas.models import Rpas

from .logs import mission_planner_logs
from .validators import validate_start_date


class LogsUpload(models.Model):

    name = models.CharField(max_length=240)
    geom = gis_models.GeometryField(blank=True, null=True)
    log = models.FileField(upload_to="mission-planner-logs/", blank=True, null=True)

    def save(self, *args, **kwargs):
        super(LogsUpload, self).save(*args, **kwargs)

        if self.log:
            from django.contrib.gis.geos import LineString, MultiLineString

            url = self.log.path
            DATA = mission_planner_logs(url)
            line = LineString(DATA)
            multi_line = MultiLineString(line)

            self.geom = multi_line

        super(LogsUpload, self).save(*args, **kwargs)


class ReserveAirspace(gis_models.Model):
    """
    This is the main model class to create reserve airspace
    it inherits from the following models
    from django.contrib.gis.db import models as gis_models
    the geom extends the models' PolgonField. Thus we can only draw polygons
    A multipolygonField would have given us ability to draw lines as well
    """

    geom = gis_models.PolygonField(blank=True, null=True)

    """
         #FIX ME: Why THE FUCK DID I do blank and null?
        --FIXED: So that If log you can either upload a log or a geom
        TODO: NB:This is why documentation is very vital!!!! I'm not paid enought to write
        all the docstrings :)
    """

    log = models.FileField(upload_to="mission-planner-logs/", blank=True, null=True)
    """
    The log field enables users to upload a Mission Planner log with extension ".waypoints"
    blank=True and null=True makes sure that user can either draw or upload a flight log.
    This is ensured in the class' clean nethod
    """
    # objects = gis_models.GeoManager()
    objects = GeoManager()

    """
    The objects field is a modelclass manager that inherits from Geodjango's default manager
    NB: This is slightly diffrent for Django 2+ users
    """
    rpas = models.ForeignKey(Rpas, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    start_day = models.DateField(default=date.today, validators=[validate_start_date])
    start_time = models.TimeField(help_text="HH:MM:SS")
    end = models.TimeField(help_text="HH:MM:SS")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    PENDING = 0
    DENIED = 1
    APPROVED = 2
    STATUS = ((PENDING, "PENDING"), (DENIED, "DENIED"), (APPROVED, "APPROVED"))

    OBJECTIVE = (
        ("TRAIN", "Training"),
        ("MAPP", "Mapping"),
        ("3DM", "3D Mapping"),
        ("DELV", "Delivery"),
        ("INSP", "Inspection"),
        ("SURV", "Surveillance"),
        ("REC", "Recreational"),
        ("OTH", "Other"),
    )
    mission_type = models.CharField(
        max_length=5, choices=OBJECTIVE, null=False, default="OTH"
    )

    application_number = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0, choices=STATUS, blank=True, null=True)
    reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="If Rejected: Reason for Rejecting",
    )
    comments = models.TextField(
        blank=True, null=True, help_text="Additional Comments, if any "
    )
    centroid = gis_models.PointField(blank=True, null=True)
    expiry = gis_models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if self.geom:
            self.centroid = self.geom.centroid

        super(ReserveAirspace, self).save(*args, **kwargs)

        if self.log:
            from django.contrib.gis.geos import LineString, MultiLineString

            url = self.log.path
            DATA = mission_planner_logs(url)
            line = LineString(DATA)
            multi_line = MultiLineString(line)
            multi_line_to_polygon = multi_line.convex_hull
            # print(multi_line, "this is the multi line ")   Returns a multilinestring
            # print(multi_line.convex_hull, "this is the convex ")  Converts the multilinestring to polygon
            self.geom = multi_line_to_polygon
            # TODO: LOG UPLOAD: still retain the main log upload or merge the polygon to multiline string in detail_view

            self.centroid = self.geom.centroid

        if self.created_by.userprofile.organization.organization_type == "ROC":
            x = "FP/CAA/ROC/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == "REC":
            x = "FP/CAA/REC/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == "PVT":
            x = "FP/CAA/PVT/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == "ATO":
            x = "FP/CAA/ATO/"
            y = self.pk
            self.application_number = x + str(y)

        elif self.created_by.userprofile.organization.organization_type == "CLB":
            x = "FP/CAA/CLB/"
            y = self.pk
            self.application_number = x + str(y)

        # Putting saving time to be less than 6 minutes, after that model cant even add a flightlog
        saving_time = self.date_modified - self.date_created
        saving_time_seconds = saving_time.total_seconds()

        # TO DO: Questions: what if you create and save and edit in the 6 minutes?
        """ Turns out it does save two Flight Logs
        --FIXED by checking if the log is already created
        TODO: perhaps put this in properties? but can i access model properties in the clean?
        """
        if (saving_time_seconds / 60) < 6:
            from flight_plans.models import FlightLog

            get_log = FlightLog.objects.filter(reserve_airspace=self.pk)
            if not get_log:
                x = FlightLog.objects.create(
                    reserve_airspace_id=self.pk, user_id=self.created_by.pk
                )
                x.save()

        # if self.status == 1:
        #     from notifications.send_a_notification import send_a_notification
        #     send_a_notification(self.created_by,"Your flight has been Rejected Flight",str(self.comments))
        #     print("should have sent a notification")
        # elif self.status == 2:
        #     from notifications.send_a_notification import send_a_notification
        #     x = mark_safe('<a href="/applications/airspace/"> Go To Airspace</a>')
        #     send_a_notification(self.created_by, x, str(self.comments))

        # super(ReserveAirspace, self).save(*args, **kwargs)
        super(ReserveAirspace, self)

    def clean(self):

        super(ReserveAirspace, self).clean()
        """ Do i really need the super method above?
        """

        # Checking to see if user is registered to any organisation before allowing creation

        # FIXED: This is solved in the forms.py as the rpas dropdown is filtered by the users organisation first
        # Recreational users will have to be registered by a Club

        # try:
        #     organization = self.created_by.userprofile.organization
        #     print(organization, "organization in save()")
        # except Exception as e:
        #     print(e, "user is not attached to any organisation")
        #     print(self.created_by, "xxxxxxxxxxxxxx")

        #     raise ValidationError(
        #         "You are not registered under any organisation, you can not apply for reserve airspace"
        #     )

        if not (self.geom or self.log):
            raise ValidationError(
                "Your Geometry can't be blank. Draw an area or upload a log"
            )

        if self.start_time and self.end:
            booking_time = datetime.combine(date.min, self.end) - datetime.combine(
                date.min, self.start_time
            )
            c = booking_time.total_seconds()
            if (c / 3600) > 3:
                raise ValidationError("Cannot book airspace for more three hours!")
            elif (c / 3600) < 0:
                raise ValidationError(
                    "Cmon man!! You can not start a flight at "
                    "{:%H:%M:%S}".format(self.start_time)
                    + " and then GO BACK IN TIME to "
                    + "{:%H:%M:%S}".format(self.end)
                    + " to end your flight"
                )

            booking_schedule = (
                datetime.combine(self.start_day, self.start_time) - datetime.now()
            )
            d = booking_schedule.total_seconds()
            if (d / 3600) < 4:
                four_hours_from_now = datetime.now() + timedelta(hours=4)
                raise ValidationError(
                    "Cannot book airspace less than four hours to take-off! Try from "
                    "{:%H:%M:%S}".format(four_hours_from_now)
                )

        if self.geom:
            from notams.models import NotamAirspace

            reserve_qs = (
                ReserveAirspace.objects.all()
                .exclude(pk=self.pk)
                .filter(geom__intersects=self.geom)
            )
            geo_qs = GeofenceLocations.objects.filter(geom__intersects=self.geom)
            airports_qs = LocationPoints.objects.filter(geom__intersects=self.geom)
            notams_qs = NotamAirspace.objects.filter(expiry=False).filter(
                geom__intersects=self.geom
            )
            """
                #TODO:
                    1. ADD TIME CHECKING TO THE NOTAMS ABOVE
                    2. ADD TIME CHECK TO RESERVE_QS so that we can alert people already in flight to land,
                        and notify those just about to fly
                        to postpone
            """
            if reserve_qs or geo_qs or airports_qs or notams_qs:
                e = []
                for qs in reserve_qs:
                    if self.start_time and self.end:
                        booking_time_start = datetime.combine(
                            self.start_day, self.start_time
                        )
                        booking_time_end = datetime.combine(self.start_day, self.end)

                        booking_time_qs_start = datetime.combine(
                            qs.start_day, qs.start_time
                        )
                        booking_time_qs_end = datetime.combine(qs.start_day, qs.end)

                        if (
                            booking_time_qs_start
                            < booking_time_start
                            < booking_time_qs_end
                        ):
                            error = str(
                                qs.get_name
                                + "'s"
                                + " "
                                + "Airspace"
                                + ""
                                + "(Kindly  book after the current mission ends, try from "
                                + qs.get_start_day
                                + "  "
                                + booking_time_qs_end.strftime("%H:%M:%S")
                            )
                            e.append(error)

                for qs in geo_qs:
                    error = str(qs.name)
                    e.append(error)

                for qs in airports_qs:
                    error = str(qs.name)
                    e.append(error)

                for qs in notams_qs:
                    error = str("Notam Number" + qs.notam_number)
                    e.append(error)

                if e:
                    raise ValidationError(
                        (
                            (
                                mark_safe(
                                    "Cannot book airspace in this zone!!"
                                    + "You have violed the folowing Airspace(s)"
                                    + "<hr>"
                                    + "<p></p>"
                                    + "<b>"
                                    + str(e)
                                    + "<br> "
                                    + "<hr>"
                                    + '<a href="/applications/airspace/">Go To Airspace</a>'
                                )
                            )
                        )
                    )
            x = self.geom.area * 12365.1613
            # geom_area = loc_obj.area_ * 12365.1613 * 10**6
            if x > 9:
                raise ValidationError(
                    "This Airspace is greater than the recommended value of 9sq km"
                )
            # TODO: BVLOS CERTIFICATION EXEMPT

    def dist_from_airports(self):
        dis = GeofenceLocations.objects.all()
        fin = {}
        for x in dis:
            y = self.centroid.distance(x.centroid) / 111 * 10000
            if y < 15:
                fin.update({x.name: y})
        return fin

    def get_area(self):
        x = self.geom.area * 12365.1613
        return round(x, 3)  # sq km

    def get_perimeter(self):
        x = self.geom.length * 111
        return round(x, 2)  # km

    def __str__(self):
        return str(self.application_number)

    def get_start_datetime(self):
        booking_schedule = datetime.combine(self.start_day, self.start_time)
        return booking_schedule

    def get_absolute_url(self):
        return reverse("view_airspace")

    @property
    def get_rpas(self):
        return str(self.rpas.rpas_model.model_name)

    @property
    def get_name(self):
        return "%s %s" % (self.created_by.first_name, self.created_by.last_name)

    @property
    def get_phone_number(self):
        return str(self.created_by.userprofile.phone_number)

    @property
    def get_organization(self):
        return str(self.created_by.userprofile.organization.organization_details.name)

    @property
    def get_rpas_pic(self):
        return str(self.rpas.rpas_pic.url)

    @property
    def get_start_day(self):
        from django.contrib.humanize.templatetags.humanize import naturalday

        natural_day = naturalday(self.start_day)
        return str(natural_day)

    @property
    def get_airframe_type(self):
        return str(self.rpas.rpas_model.rpas_model_type)

    @property
    def get_log_completion_deadline(self):
        end_datetime = datetime.combine(self.start_day, self.end)
        deadline = end_datetime + timedelta(days=2)
        return deadline

    @property
    def get_user_profile_pic(self):
        return str(self.created_by.userprofile.profile_pic.url)
