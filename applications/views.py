#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##################################################################################
# File: /mnt/c/Projects/ANGA UTM/src/applications/views.py                       #
# Project: /mnt/c/Projects/ANGA UTM/src/applications                             #
# Created Date: Tuesday, March 17th 2020, 11:20:17 pm                            #
# Author: Geoffrey Nyaga Kinyua ( <geoffrey@geoffreynyaga.com> )                 #
# -----                                                                          #
# Last Modified: Saturday March 28th 2020 2:16:33 pm                             #
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

from datetime import datetime

from django.shortcuts import render

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from decouple import config

# TODO: What is the diffrence between this import and the above?
from djgeojson.views import GeoJSONLayerView


from rpas.models import Rpas
from .forms import (
	ReserveAirspaceForm,
	AppliedReserveAirspaceUpdateForm,
	CAAAppliedReserveAirspaceUpdateForm,
)
from .models import ReserveAirspace


class ReserveAirspaceMainView(TemplateView):
	template_name = "applications/includes/reserve_main.html"


class OldReserveAirspaceCreateView(CreateView):
	""" TO DO: Restrict Pending Flights to 10 to reduce spamming
		--FIXED by queryset count and if-else in templates
	"""

	form_class = ReserveAirspaceForm
	model = ReserveAirspace
	template_name = "applications/create_reserve.html"
	success_url = "/applications/airspace"

	def form_valid(self, form):
		reserveairspace = form.save(commit=False)
		reserveairspace.created_by = User.objects.get(
			username=self.request.user
		)  # use your own profile here
		reserveairspace.save()
		return HttpResponseRedirect(self.success_url)

	def get_form_kwargs(self):
		kwargs = super(OldReserveAirspaceCreateView, self).get_form_kwargs()
		kwargs["user"] = self.request.user
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(OldReserveAirspaceCreateView, self).get_context_data(
			*args, **kwargs
		)

		my_pending_airspaces = ReserveAirspace.objects.filter(
			created_by=self.request.user
		).filter(status=0)

		context["my_pending_approval_airspaces"] = my_pending_airspaces.order_by("-id")[
			:10
		]
		context["my_pending_approval_airspaces_count"] = my_pending_airspaces.count()
		# context['myflightlogs'] = FlightLog.objects.filter(user=thisuser)
		return context


class ReserveAirspaceCreateView(CreateView):
	""" TO DO: Restrict Pending Flights to 10 to reduce spamming
		--FIXED by queryset count and if-else in templates
	"""

	form_class = ReserveAirspaceForm
	model = ReserveAirspace
	template_name = "applications/create_reserve.html"
	# success_url = "/applications/airspace"

	def form_valid(self, form):
		reserveairspace = form.save(commit=False)
		reserveairspace.created_by = User.objects.get(
			username=self.request.user
		)  # use your own profile here
		reserveairspace.save()
		return HttpResponseRedirect(self.success_url)

	def get_form_kwargs(self):
		kwargs = super(ReserveAirspaceCreateView, self).get_form_kwargs()
		kwargs["user"] = self.request.user
		return kwargs

	def get_context_data(self, *args, **kwargs):
		context = super(ReserveAirspaceCreateView, self).get_context_data(
			*args, **kwargs
		)

		my_pending_airspaces = ReserveAirspace.objects.filter(
			created_by=self.request.user
		).filter(status=0)

		org = self.request.user.userprofile.organization

		context["my_pending_approval_airspaces"] = my_pending_airspaces.order_by("-id")[
			:10
		]
		context["my_pending_approval_airspaces_count"] = my_pending_airspaces.count()
		# context['myflightlogs'] = FlightLog.objects.filter(user=thisuser)

		context["my_rpas"] = Rpas.objects.filter(organization=org)

		context["AIRMAP_API_KEY"] = config("AIRMAP_API_KEY")
		context["MAPBOX_ACCESS_TOKEN"] = config("MAPBOX_ACCESS_TOKEN")

		return context


class ReserveAirspaceListView(ListView):
	context_object_name = "my_reserves"
	template_name = "applications/my_reserve_list.html"

	def get_queryset(self):
		return ReserveAirspace.objects.filter(created_by=self.request.user)


class ReserveAirspaceDetailView(DetailView):
	model = ReserveAirspace
	template_name = "applications/reserveairspace_detail.html"


class ReserveAirspaceUpdateView(UpdateView):
	template_name = "applications/update_my_airspace.html"
	model = ReserveAirspace
	form_class = AppliedReserveAirspaceUpdateForm
	success_url = "/applications/myreserve/"

	def form_valid(self, form):
		reserveairspace = form.save(commit=False)
		reserveairspace.created_by = User.objects.get(
			username=self.request.user
		)  # use your own profile here
		reserveairspace.save()
		return HttpResponseRedirect(self.success_url)

	def get_form_kwargs(self):
		kwargs = super(ReserveAirspaceUpdateView, self).get_form_kwargs()
		kwargs["user"] = self.request.user
		return kwargs


##############################################################################################


# this one will just output all User datasets to template
def my_reserve_datasets(request):
	airspace = serialize(
		"geojson", ReserveAirspace.objects.filter(created_by=request.user)
	)
	return HttpResponse(airspace, content_type="json")


def all_reserve_datasets(request):
	airspace = serialize("geojson", ReserveAirspace.objects.filter(expiry=False))
	return HttpResponse(airspace, content_type="json")


# this one you have to pass on a pk in template to access a single instance
def my_airspace_datasets(request, pk):
	my_reserve_airspace = ReserveAirspace.objects.filter(pk=pk)
	path = serialize("geojson", my_reserve_airspace)
	return HttpResponse(path, content_type="json")


################################################################################################


def view_airspace(request):
	# from applications import bounding

	# import json

	# print(type(bounding.bounding_boxes), "should be dict")
	# print(type(json.dumps(bounding.bounding_boxes)), "should be str")

	airspaces = ReserveAirspace.objects.all()
	AIRMAP_API_KEY = config("AIRMAP_API_KEY")
	MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

	return render(
		request,
		"applications/airspaces.html",
		{
			"airspaces": airspaces,
			"AIRMAP_API_KEY": AIRMAP_API_KEY,
			"MAPBOX_ACCESS_TOKEN": MAPBOX_ACCESS_TOKEN,
			# "bounding_boxes": json.dumps(bounding.bounding_boxes),
		},
	)


class MyModelLayer(GeoJSONLayerView):
	def get_queryset(self):
		a = ReserveAirspace.objects.exclude(expiry=True)
		# a = ReserveAirspace.objects.all()
		for x in a:
			t = datetime.combine(x.start_day, x.end) - datetime.now()
			d = t.total_seconds()
			if (d / 3600) < 0:
				x.expiry = True
				x.save()
		context = a.filter(expiry=False)
		return context


#######################################################

# CAA JUNK

# TO DO: CAA LOGIN REQUIRED MIXIN
# --FIXED: templates has_group=='CAA'
class AppliedReserveAirspaceListView(ListView):
	context_object_name = "applied_reserves"
	template_name = "applications/applied_reserve_list.html"

	def get_queryset(self):
		return ReserveAirspace.objects.filter(status=0)

	def get_context_data(self, **kwargs):
		context = super(AppliedReserveAirspaceListView, self).get_context_data(**kwargs)

		# TODO: Commercial Flights Pending Approvals

		# TODO: Private Flights Pending Approvals

		# TODO: Clubs Flights Pending Approvals

		approved_airspaces = ReserveAirspace.objects.filter(status=2).order_by("-id")

		rejected_airspaces = ReserveAirspace.objects.filter(status=1).order_by("-id")

		context["approved_airspaces"] = approved_airspaces
		context["approved_airspaces_count"] = approved_airspaces.count()

		context["rejected_airspaces"] = rejected_airspaces
		context["rejected_airspaces_count"] = rejected_airspaces.count()
		return context


class AppliedReserveAirspaceDetailView(DetailView):
	model = ReserveAirspace
	template_name = "applications/includes/detail.html"


class AppliedReserveAirspaceUpdateView(UpdateView):
	form_class = CAAAppliedReserveAirspaceUpdateForm
	model = ReserveAirspace
	template_name = "applications/approve.html"
	success_url = "/applications/applied-reserves"


##########################################################
class MyApprovalLettersListView(ListView):
	context_object_name = "my_approval_letters"
	template_name = "applications/my_approval_letters_list.html"

	def get_queryset(self):
		return ReserveAirspace.objects.filter(created_by=self.request.user, status=2)


class MyApprovalLettersDetailView(DetailView):
	model = ReserveAirspace
	template_name = "applications/appoval-letter.html"


########################################################################################
# class LogsUploadCreateView(CreateView):
#     form_class = LogsUploadForm
#     template_name = 'applications/create_log_upload.html'
#     success_url = '/applications/airspace'


# class LogsUploadListView(ListView):
#     model = LogsUpload
#     template_name = 'applications/log_uploads_list.html'
#     context_object_name = 'logs'
