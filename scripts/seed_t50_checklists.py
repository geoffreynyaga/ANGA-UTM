import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANGA_UTM.settings.local')
django.setup()

from flight_plans.models import ChecklistItem, ChecklistGroup, ChecklistTemplate

def seed_checklists():
    # Helper to get or create item
    def add_item(code, title, desc, category, optional=False):
        item, _ = ChecklistItem.objects.get_or_create(
            item_code=code,
            defaults={
                'item_title': title,
                'description': desc,
                'category': category,
                'is_optional': optional
            }
        )
        return item

    # 1. PRE-FLIGHT CHECKLIST
    preflight_template, _ = ChecklistTemplate.objects.get_or_create(
        id="agras-t50-preflight",
        defaults={
            'title': "AGRAS T50 Pre-Flight",
            'checklist_type': "Pre-Flight"
        }
    )

    # Groups for Pre-Flight
    groups_data = [
        {
            "title": "Approvals & Mission Authorization",
            "items": [
                ("1.4", "Regulatory Approvals", "Confirm approvals from KCAA, Company, and Site Owner.", "Approvals", False),
                ("1.6", "KCAA Documentation", "Verify KCAA documentation and insurance onsite.", "Approvals", False),
            ]
        },
        {
            "title": "Hazard Check & Safety",
            "items": [
                ("2.1", "Job-Site Hazards", "Identify powerlines, obstacles, persons, public roads, and mitigation steps.", "Hazard Check", False),
                ("2.2", "Crew Briefing", "Conduct full briefing: objectives, hazards, emergency plan, roles.", "Safety", False),
                ("2.3", "PPE Verification", "Verify all Personal Protective Equipment for PIC and VO.", "Safety", False),
                ("2.4", "Weather Minimums", "Wind <=18 mph, visibility >=3 SM, ceiling >=500 ft AGL.", "Safety", False),
                ("2.5", "Emergency Plan", "Confirm emergency response contacts and action plan.", "Safety", False),
                ("2.6", "Launch Area Clearance", "Area cleared of personnel, livestock, and vehicles.", "Hazard Check", False),
            ]
        },
        {
            "title": "Ground Checks - Structure & Propellers",
            "items": [
                ("3.1", "Airframe & Arms", "Check for cracks, corrosion, delamination, and loose bolts.", "Ground Checks", False),
                ("3.3", "Locking Mechanism", "Ensure all arms and frame components are securely locked.", "Ground Checks", False),
                ("3.4", "Propellers & Hubs", "Inspect for cracks, chips, imbalance, and verify correct mounting.", "Ground Checks", False),
                ("3.5", "Motors & ESCs", "Smooth rotation, no unusual friction or noise.", "Ground Checks", False),
            ]
        },
        {
            "title": "Ground Checks - Batteries & RC",
            "items": [
                ("4.1", "Battery Compartment", "Clean terminals, locked battery, no corrosion.", "Ground Checks", False),
                ("4.2", "Aircraft Batteries", "No swelling, cell terminals", "Ground Checks", False),
                ("4.3", "RC Batteries & Terminals", "Check remote controller battery level", "Ground Checks", False),
                ("4.4", "Generator Check", "Verify fuel levels, oil.", "Ground Checks", True),
            ]
        },
        {
            "title": "Ground Checks - Spray System",
            "items": [
                ("5.1", "Spray/spreading Tank", "No leaks, cracks, secure mount.", "Ground Checks", False),
                ("5.3", "Nozzles", "Firmly intact", "Ground Checks", False),
            ]
        },
        {
            "title": "Ground Checks - Systems & Vision",
            "items": [
                ("6.4", "Firmware & Software", "Confirm no warnings.", "Ground Checks", False),
                ("6.5", "Failsafe / RTH", "RTH altitude is correct (think about trees and obstacles)", "Ground Checks", False),
                ("6.6", "Battery Settings", "RTH on battery low (at 30%)", "Ground Checks", False),
            ]
        },
        {
            "title": "Flight Operations",
            "items": [
                ("7.5", "Separation and segmentation", "Ensure separation between aircraft and ground crew.", "Flight Ops", False),
            ]
        }
    ]

    for g in groups_data:
        group, _ = ChecklistGroup.objects.get_or_create(
            title=g["title"],
            checklist_type="PRE"
        )
        for item_data in g["items"]:
            item = add_item(*item_data)
            group.checklists.add(item)
        preflight_template.groups.add(group)

    # 2. POST-FLIGHT CHECKLIST
    postflight_template, _ = ChecklistTemplate.objects.get_or_create(
        id="agras-t50-postflight",
        defaults={
            'title': "AGRAS T50 Post-Flight",
            'checklist_type': "Post-Flight"
        }
    )

    post_groups_data = [
        {
            "title": "Post-Flight Procedures",
            "items": [
                ("8.2", "Battery Inspection", "Check for heat, swelling, damage", "Post-Flight", False),
                ("8.3", "System Flush", "Flush spray system with clean water until lines run clear.", "Post-Flight", False),
                ("8.4", "Cleaning", "Clean airframe and remove chemical residue.", "Post-Flight", False),
                ("8.7", "Crew Debrief", "Conduct post-mission crew debrief.", "Post-Flight", False),
            ]
        },
        {
            "title": "Administrative Requirements",
            "items": [
                ("9.1", "Performance Metrics", "Record key metrics: area treated, bags spread etc", "Admin", False),
                ("9.3", "Whatsapp updates", "Update any necessary Whatsapp groups", "Admin", False),
            ]
        }
    ]

    for g in post_groups_data:
        group, _ = ChecklistGroup.objects.get_or_create(
            title=g["title"],
            checklist_type="POS"
        )
        for item_data in g["items"]:
            item = add_item(*item_data)
            group.checklists.add(item)
        postflight_template.groups.add(group)

    print("Successfully seeded AGRAS T50 Checklists!")

if __name__ == "__main__":
    seed_checklists()
