import configparser
import time

from TM1py import Dimension, Hierarchy, Cube, NativeView
from TM1py import TM1Service
from TM1py.Utils.Utils import CaseAndSpaceInsensitiveSet

from Samples.Cubank.cubank_loan import Loan

SKIP_RECORDS_TOP = 1
SKIP_RECORDS_BOTTOM = 5
EXPECTED_FIELDS = 151
MAX_RECORDS = 100_000
WRITE_BATCH_SIZE = 10_000

CUBE_NAME = "Loans"
DIMENSIONS = [
    "Time",
    "Loan",
    "LC Rating",
    "FICO Score",
    "Employment",
    "Term",
    "Income",
    "Purpose",
    "Loan Status",
    "State",
    "Home Ownership",
    "Application Type",
    "Delinquency Events",
    "Income To Loan Ratio",
    CUBE_NAME + " Measure"]
MEASURES = ["loan_amnt", "int_rate", "installment", "out_prncp", "total_pymnt", "last_pymnt_d", "last_pymnt_amnt",
            "emp_length", "num_personal_inquiries", "inquiries_in_last_12m", "mths_since_last_delinq",
            "mths_since_recent_bc_dlq", "mths_since_recent_inq", "mths_since_recent_revol_delinq"]

MDX_TEMPLATE = """
SELECT 
{rows} ON ROWS,
{columns} ON COLUMNS
FROM [{cube}]
"""

VIEW_FILES = ["cubank_view1.json", "cubank_view2.json"]


def read_loans_from_file(path) -> list:
    records_ignored = list()
    loans = list()

    with open(path, encoding="utf-8") as file:
        lines = file.readlines()
        for counter, line in enumerate(lines[SKIP_RECORDS_TOP:-SKIP_RECORDS_BOTTOM], start=1):
            if len(line) > 0:
                if "Loans that do not meet the credit policy" in line:
                    records_ignored += lines[counter:]
                    break
                if len(line.split(",")) != EXPECTED_FIELDS:
                    records_ignored.append(line)
                    continue
                loans.append(Loan(line=line))
    print("Records consumed: " + str(len(loans)))
    print("Records ignored: " + str(len(records_ignored)))
    return loans[:MAX_RECORDS]


def update_or_create_dimension(tm1: TM1Service, dimension: Dimension):
    if tm1.dimensions.exists(dimension.name):
        tm1.dimensions.update(dimension)
    else:
        tm1.dimensions.create(dimension)


def build_dimensions(tm1: TM1Service, loans: list):
    dimension_name = "Time"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for year in range(2005, 2020, 1):
        hierarchy.add_element(element_name=str(year), element_type="Consolidated")
        hierarchy.add_edge(parent=total_element, component=str(year), weight=1)
        for month in ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"):
            hierarchy.add_element(element_name="{}-{}".format(month, str(year)), element_type="Numeric")
            hierarchy.add_edge(parent=str(year), component="{}-{}".format(month, str(year)), weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Loan"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    dimension.add_hierarchy(hierarchy)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    element_names = [loan.loan_id for loan in loans]
    # send elements and edges separately to avoid strange firewall connection abortion from server side
    for element_name in element_names:
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
    update_or_create_dimension(tm1, dimension)

    for element_name in element_names:
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "LC Rating"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for rating in ("A", "B", "C", "D", "E", "F", "G"):
        element_name = rating
        hierarchy.add_element(element_name=element_name, element_type="Consolidated")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
        for sub_rating in ("1", "2", "3", "4", "5"):
            element_name = rating + sub_rating
            hierarchy.add_element(element_name=element_name, element_type="Numeric")
            hierarchy.add_edge(parent=rating, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "FICO Score"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in range(300, 851, 1):
        hierarchy.add_element(element_name=str(element_name), element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=str(element_name), weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Employment"
    if tm1.dimensions.exists(dimension_name=dimension_name):
        dimension = tm1.dimensions.get(dimension_name=dimension_name)
    else:
        dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    if hierarchy_name in dimension:
        hierarchy = dimension.get_hierarchy(hierarchy_name=hierarchy_name)
    else:
        hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
        dimension.add_hierarchy(hierarchy)
    total_element = "Total " + dimension_name
    if total_element not in hierarchy.elements:
        hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    employments = CaseAndSpaceInsensitiveSet()
    for loan in loans:
        employments.add(loan.emp_title)
    employments.add("None")
    for employment in employments:
        if employment and employment not in hierarchy.elements:
            employment = employment.strip()
            hierarchy.add_element(element_name=employment, element_type="Numeric")
            hierarchy.add_edge(parent=total_element, component=employment, weight=1)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Term"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in ("36 months", "60 months"):
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Income"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in ("10000", "20000", "30000", "40000", "50000", "60000", "70000", "80000", "90000", "100000",
                         "110000", "120000", "130000", "140000", "150000", "160000", "170000", "180000", "190000"):
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Purpose"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in ("other", "debt_consolidation", "medical", "major_purchase", "home_improvement", "credit_card",
                         "vacation", "house", "car", "small_business", "moving", "renewable_energy", "wedding",
                         "educational"):
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Loan Status"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in ("Current", "Fully Paid", "Late (31-120 days)", "Late (16-30 days)", "Charged Off",
                         "In Grace Period", "Default"):
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "State"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    states = CaseAndSpaceInsensitiveSet()
    for loan in loans:
        states.add(loan.addr_state)
    states.add("None")
    for state in states:
        if state:
            state = state.strip()
            hierarchy.add_element(element_name=state, element_type="Numeric")
            hierarchy.add_edge(parent=total_element, component=state, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Home Ownership"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in ("Rent", "Own", "Mortgage", "Any", "None"):
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Application Type"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in ("Individual", "Joint App"):
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Income To Loan Ratio"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for counter in range(0, 100000, 1):
        dti = counter / 100
        element_name = "%.2f" % dti
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=element_name, weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = "Delinquency Events"
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    total_element = "Total " + dimension_name
    hierarchy.add_element(element_name=total_element, element_type="Consolidated")
    for element_name in range(0, 51):
        hierarchy.add_element(element_name=str(element_name), element_type="Numeric")
        hierarchy.add_edge(parent=total_element, component=str(element_name), weight=1)
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    dimension_name = " ".join([CUBE_NAME, "Measure"])
    dimension = Dimension(name=dimension_name)
    hierarchy_name = dimension_name
    hierarchy = Hierarchy(name=hierarchy_name, dimension_name=dimension_name)
    for element_name in ("loan_amnt", "int_rate", "installment", "out_prncp", "total_pymnt", "last_pymnt_amnt",
                         "total_pymnt_by_loan_amnt", "emp_length", "num_personal_inquiries", "inquiries_in_last_12m",
                         "mths_since_last_delinq", "mths_since_recent_bc_dlq", "mths_since_recent_inq",
                         "mths_since_recent_revol_delinq", "defaulted", "defaulted_or_delayed"):
        hierarchy.add_element(element_name=element_name, element_type="Numeric")
    for element_name in ("last_pymnt_d",):
        hierarchy.add_element(element_name=element_name, element_type="String")
    hierarchy.add_element_attribute(name="Description", attribute_type="Alias")
    dimension.add_hierarchy(hierarchy)
    update_or_create_dimension(tm1, dimension)

    attributes = {
        ("loan_amnt", "Description"): "Listed amount of the loan",
        ("int_rate", "Description"): "Interest rate",
        ("installment", "Description"): "Monthly payment",
        ("out_prncp", "Description"): "Remaining outstanding amount",
        ("total_pymnt", "Description"): "Payments received to date",
        ("total_pymnt_by_loan_amnt", "Description"): "Total Payments devided by total Loan",
        ("last_pymnt_amnt", "Description"): "Last payment amount received",
        ("last_pymnt_d", "Description"): "Last month payment was received",
        ("defaulted", "Description"): "Loan is defaulted"}
    tm1.cubes.cells.write_values(cube_name="}ElementAttributes_" + dimension_name, cellset_as_dict=attributes)


def build_cube(tm1: TM1Service):
    rules = """
    SKIPCHECK;
    ['{cube} Measure':'defaulted', 'Loan Status':'Default'] = N: 1; 
    ['{cube} Measure':'defaulted', 'Loan Status':'Charged Off'] = N: 1; 
    ['{cube} Measure':'total_pymnt_by_loan_amnt'] = N: ['{cube} Measure':'total_pymnt'] \\ ['{cube} Measure':'loan_amnt'];
    FEEDERS;
    ['{cube} Measure':'loan_amnt'] => ['{cube} Measure':'defaulted'], ['{cube} Measure':'total_pymnt_by_loan_amnt'];
    """.format(cube=CUBE_NAME)
    cube = Cube(name=CUBE_NAME, dimensions=DIMENSIONS, rules=rules)
    if not tm1.cubes.exists(cube.name):
        tm1.cubes.create(cube)
    else:
        tm1.cubes.update(cube)


def build_views(tm1: TM1Service):
    for file_name in VIEW_FILES:
        with open(file_name, "r", encoding="utf-8") as file:
            view = NativeView.from_json(file.read(), CUBE_NAME)
            if tm1.cubes.views.exists(CUBE_NAME, view.name, False):
                tm1.cubes.views.update(view, False)
            else:
                tm1.cubes.views.create(view, False)


def load_data(tm1: TM1Service, loans: list):
    for start, end in zip(
            range(0, len(loans), WRITE_BATCH_SIZE),
            range(WRITE_BATCH_SIZE, len(loans), WRITE_BATCH_SIZE)):
        write(tm1, loans[start:end])


def write(tm1: TM1Service, chunk: list):
    mdx_rows = list()
    values = list()

    for loan in chunk:
        if loan.dti:
            mdx_rows.append("("
                            "[{dim1}].[{elem1}], "
                            "[{dim2}].[{elem2}], "
                            "[{dim3}].[{elem3}], "
                            "[{dim4}].[{elem4}], "
                            "[{dim5}].[{elem5}], "
                            "[{dim6}].[{elem6}], "
                            "[{dim7}].[{elem7}], "
                            "[{dim8}].[{elem8}], "
                            "[{dim9}].[{elem9}], "
                            "[{dim10}].[{elem10}], "
                            "[{dim11}].[{elem11}], "
                            "[{dim12}].[{elem12}], "
                            "[{dim13}].[{elem13}], "
                            "[{dim14}].[{elem14}])".format(
                dim1=DIMENSIONS[0], elem1=loan.issue_d,
                dim2=DIMENSIONS[1], elem2=loan.loan_id,
                dim3=DIMENSIONS[2], elem3=loan.sub_grade,
                dim4=DIMENSIONS[3], elem4=loan.determine_fico_score(),
                dim5=DIMENSIONS[4], elem5=loan.emp_title if loan.emp_title else "None",
                dim6=DIMENSIONS[5], elem6=loan.term,
                dim7=DIMENSIONS[6], elem7=loan.determine_income_class(),
                dim8=DIMENSIONS[7], elem8=loan.purpose,
                dim9=DIMENSIONS[8], elem9=loan.loan_status,
                dim10=DIMENSIONS[9], elem10=loan.addr_state,
                dim11=DIMENSIONS[10], elem11=loan.home_ownership,
                dim12=DIMENSIONS[11], elem12=loan.application_type,
                dim13=DIMENSIONS[12], elem13=str(int(float(loan.delinq_2yrs))),
                dim14=DIMENSIONS[13], elem14="%.2f" % float(loan.dti)))

            values += [
                loan.loan_amnt,
                float(loan.int_rate) / 100,
                loan.installment,
                loan.out_prncp,
                loan.total_pymnt,
                loan.last_pymnt_d,
                loan.last_pymnt_amnt,
                ''.join(filter(lambda x: x.isdigit(), loan.emp_length)) or 0,
                loan.inq_fi,
                loan.inq_last_12m,
                loan.mths_since_last_delinq if loan.mths_since_last_delinq else 240,
                loan.mths_since_recent_bc_dlq if loan.mths_since_recent_bc_dlq else 240,
                loan.mths_since_recent_inq if loan.mths_since_recent_inq else 240,
                loan.mths_since_recent_revol_delinq]

    mdx_columns = [
        "[" + DIMENSIONS[-1] + "].[" + element + "]"
        for element
        in MEASURES]

    mdx = MDX_TEMPLATE.format(
        rows="{" + ",".join(mdx_rows) + "}",
        columns="{" + ",".join(mdx_columns) + "}",
        cube=CUBE_NAME)

    tm1.cubes.cells.write_values_through_cellset(mdx, values)


if __name__ == "__main__":
    start = time.time()

    config = configparser.ConfigParser()
    config.read(r'..\..\config.ini')
    loans = read_loans_from_file(path="cubank_loans.csv")

    with TM1Service(**config['tm1srv01']) as tm1:
        build_dimensions(tm1, loans)
        build_cube(tm1)
        build_views(tm1)
        load_data(tm1, loans)

    end = time.time()
    print("Total execution time in seconds: " + str(end - start))
