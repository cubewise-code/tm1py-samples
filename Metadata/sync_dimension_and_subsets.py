import time

from TM1py import TM1Service

ADDRESS = "localhost"
SSL = True
USER = "admin"
PASSWORD = "apple"

tm1_master = TM1Service(address=ADDRESS, port=12354, ssl=SSL, user=USER, password=PASSWORD)
tm1_other = TM1Service(address=ADDRESS, port=12297, ssl=SSL, user=USER, password=PASSWORD)

while True:
    dimension_master = tm1_master.dimensions.get(dimension_name="Region")
    dimension_other = tm1_other.dimensions.get(dimension_name="Region")

    if dimension_master != dimension_other:
        print(f"Recognized changes. Updating dimension: '{dimension_master.name}'")
        tm1_other.dimensions.update(dimension_master)

    subsets_names = tm1_master.subsets.get_all_names("Region")
    for subsets_name in subsets_names:
        subset_master = tm1_master.subsets.get(subsets_name, dimension_name="Region")

        subset_other = tm1_other.subsets.get(subsets_name, dimension_name="Region")
        if subset_master != subset_other:
            print(f"Recognized changes. Updating Subset: '{subsets_name}'")
            tm1_other.subsets.update(subset_master)

    time.sleep(2)
