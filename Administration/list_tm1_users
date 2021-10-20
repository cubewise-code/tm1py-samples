import os
import sys
from datetime import datetime
from typing import List, Dict

from TM1py.Services import TM1Service
from TM1py.Utils import get_all_servers_from_adminhost

# =============================================================================================================
# START of parameters and settings
# =============================================================================================================
RESULT_FILE = r'D:\tm1_users.txt'

HEADER_OR_CUSTOMER = 'UPDATE THE CONSTANT WITH A DESCRIPTIVE HEADER OF YOUR LIKING'

# TM1 connection settings (IntegratedSecurityMode = 1 for now)
ADDRESS = 'localhost'
USER = 'wim'
PWD = 'password'

# level of detail in the output ==> 'YYYYY':
# - character 1: whether adding a header section with information for each TM1 model (Y/N)
# - character 2: whether adding a section for an IBM user audit (Y/N)
# - character 3: whether adding a section to list the count of users in each TM1 model (Y/N)
# - character 4: whether adding a section to list the users in each TM1 model by their rights (Y/N)
# - character 5: whether adding a section to list all the users in each TM1 model (Y/N)
# - character 6: whether adding a section to list all the users in each TM1 model with their respective group memberships (Y/N)
OUTPUT_LEVEL = 'YYYYYY'
OUTPUT_LEVEL = OUTPUT_LEVEL.replace(' ', '').upper()

PORTS_TO_EXCLUDE = []

# use attributes (alias or text attribute or even numeric) to use 'better' user names for clients and/or groups
# note: in case of a text or numeric attribute, there is a responsibility to provide unique names
ATTRIBUTE_FOR_CLIENT_NAMES = '}TM1_DefaultDisplayValue'

PA_VERSIONS = {
    '11.8.00900.3': ['11.8.900.3', '11.8', '2.0.9.10', '14/09/2021'],
    '11.8.00800.5': ['11.8.800.5', '11.8', '2.0.9.9', '14/07/2021'],
    '11.8.00700.?': ['11.8.700.?', '11.8', '2.0.9.8', '26/05/2021'],
    '11.8.00600.?': ['11.8.600.?', '11.8', '2.0.9.7', '15/04/2021'],
    '11.8.00500.12': ['11.8.500.12', '11.8', '2.0.9.6', '16/03/2021'],
    '11.8.00400.7': ['11.8.400.7', '11.8', '2.0.9.5', '08/02/2021'],
    '11.8.00300.34': ['11.8.300.34', '11.8', '2.0.9.4', '17/12/2020'],
    '11.8.00300.33': ['11.8.300.33', '11.8', '2.0.9.4', '17/12/2020'],
    '11.8.00200.24': ['11.8.200.24', '11.8', '2.0.9.3', '09/10/2020'],
    '11.8.00100.13': ['11.8.100.13', '11.8', '2.0.9.2', '27/07/2020'],
    '11.8.00000.33': ['11.8.0.33', '11.8', '2.0.9.1', '21/05/2020'],
    '11.7.00000.42': ['11.7.0.42', '11.7', '2.0.9', '16/12/2019'],
    '11.6.00000.14': ['11.6.0.14', '11.6', '2.0.8', '17/07/2019'],
    '11.5.00000.23': ['11.5.0.23', '11.5', '2.0.7', '29/04/2019'],
    '11.4.00003.8': ['11.4.3.8', '11.4', '2.0.6 IF3', ''],
    '11.4.00000.21': ['11.4.0.21', '11.4', '2.0.6', '11/10/2018'],
    '11.3.00003.1': ['11.3.3.1', '11.3', '2.0.5 IF3', ''],
    '11.3.00000.27': ['11.3.0.27', '11.3', '2.0.5', '25/06/2018'],
    '11.2.00000.27': ['11.2.0.27', '11.2', '2.0.4', '16/02/2018'],
    '11.1.00004.2': ['11.1.4.2', '11.1', '2.0.3 (dec 2017)', '12/2017'],
    '11.1.00000.30': ['11.1.0.30', '11.1', '2.0.3', '19/09/2017'],
    '11.0.00204.1030': ['11.0.204.1030', '11.0', '2.0.2 IF4', ''],
    '11.0.00202.1014': ['11.0.202.1014', '11.0', '2.0.2 IF2', ''],
    '11.0.00200.998': ['11.0.200.998', '11.0', '2.0.2', '01/06/2017'],
    '11.0.00101.931': ['11.0.101.931', '11.0', '2.0.1 IF1', ''],
    '11.0.00100.927-0': ['11.0.100.927', '11.0', '2.0.1', '07/02/2017'],
    '11.0.00000.918': ['11.0.00000.918', '11.0', '2.0.0', '16/12/2016']}


# =============================================================================================================
# END of parameters and settings
# =============================================================================================================


def inspect_users():
    # sanity checks
    if len(OUTPUT_LEVEL) != 6:
        sys.exit('Level of output should contain 6 characters, with either Y or N. You now have: ' + OUTPUT_LEVEL)

    if len(OUTPUT_LEVEL.replace('Y', '').replace('N', '')) != 0:
        sys.exit('Level of output should contain 6 characters, with either Y or N. You now have: ' + OUTPUT_LEVEL)

    log_lines = []

    if len(HEADER_OR_CUSTOMER):
        log_lines.append('\n{}\n'.format(HEADER_OR_CUSTOMER))

    # get TM1 models registered with the admin server
    tm1_instances_on_server = get_all_servers_from_adminhost(ADDRESS, None, True)
    for tm1_instance in tm1_instances_on_server:

        # get TM1 server information
        port = tm1_instance.http_port_number
        if port in PORTS_TO_EXCLUDE:
            continue

        ssl = tm1_instance.using_ssl

        tm1 = TM1Service(address=ADDRESS, port=port, user=USER, password=PWD, namespace='', gateway='', ssl=ssl)

        active_configuration = tm1.server.get_active_configuration()

        log_lines.append('\n=============  ' + tm1_instance.name + '  =============\n')

        # get user types
        users = tm1.security.get_all_users()

        if OUTPUT_LEVEL[0] == 'Y':
            log_lines.append("Current time: " + datetime.now().strftime("%x %X"))
            version = tm1.server.get_product_version()
            try:
                log_lines.append(
                    'PA version information: ' + version + ' (' + (' | '.join(PA_VERSIONS[version])).strip(' | ') + ')')
            except KeyError:
                log_lines.append('Unknown software version: ' + version)

            log_lines.append('Base TM1 REST API URL: ' + 'http' + ('s' if ssl else '') + '://' + ADDRESS + ':' + str(
                port) + '/api/v1/$metadata')
            log_lines.append('TM1 data directory: ' + os.path.abspath(tm1.server.get_data_directory()))
            log_lines.append('TM1 logging directory: ' + os.path.abspath(
                active_configuration["Administration"]["DebugLog"]["LoggingDirectory"]))
            log_lines.append('')
            log_lines.append('')

        if OUTPUT_LEVEL[1] == 'Y' or OUTPUT_LEVEL[2] == 'Y' or OUTPUT_LEVEL[3] == 'Y' or OUTPUT_LEVEL[4] == 'Y' or OUTPUT_LEVEL[5] == 'Y':
            admin_users = []
            full_admin_users = []
            security_admin_users = []
            data_admin_users = []
            operations_admin_users = []
            non_admin_users = []
            authorized_users = []
            write_users = []
            read_users = []
            disabled_users = []
            all_users = []
            all_users_with_groups = []

            # get read-only users
            read_only_users = tm1.security.get_read_only_users()
            # custom security groups in TM1
            custom_groups = tm1.security.get_custom_security_groups()

            for user in users:
                user_name = str(user.name)
                all_users.append(user_name)
                all_users_with_groups.append(user_and_groups(tm1, user_name))
                if not user.enabled:
                    disabled_users.append(user_name)
                elif str(user.user_type) == 'Admin':
                    admin_users.append(user_name)
                    full_admin_users.append(user_name)
                elif str(user.user_type) == 'SecurityAdmin':
                    admin_users.append(user_name)
                    security_admin_users.append(user_name)
                elif str(user.user_type) == 'DataAdmin':
                    admin_users.append(user_name)
                    data_admin_users.append(user_name)
                elif str(user.user_type) == 'OperationsAdmin':
                    admin_users.append(user_name)
                    operations_admin_users.append(user_name)
                else:
                    non_admin_users.append(user_name)
                    authorized_users.append(user_name)
                    if user_name in read_only_users:
                        read_users.append(user_name)
                    else:
                        client_access_level = determine_client_access_level_with_cube_security(tm1, user_name)
                        if client_access_level == 'W':
                            write_users.append(user_name)
                        else:
                            read_users.append(user_name)

            # output
            if OUTPUT_LEVEL[1] == 'Y':

                log_lines.append('User audit:')
                log_lines.append('----------')
                log_lines.append('')

                output_count('Users', users, 0, log_lines)
                output_count('Full admin users (\'Administrator\')', full_admin_users, 1, log_lines)
                output_count('Read/write users (\'Authorized User\')', authorized_users, 1, log_lines)
                output_count('Read-only users (\'Explorer\')', read_only_users, 1, log_lines)
                output_count('Disabled users', disabled_users, 1, log_lines)
                if len(security_admin_users) > 0:
                    output_count('Security admin users', security_admin_users, 1, log_lines)
                if len(data_admin_users) > 0:
                    output_count('Data admin users', data_admin_users, 1, log_lines)
                if len(operations_admin_users) > 0:
                    output_count('Operations admin users', operations_admin_users, 1, log_lines)
                log_lines.append('')
                log_lines.append('')

            if OUTPUT_LEVEL[2] == 'Y':
                log_lines.append('User count:')
                log_lines.append('-----------')
                log_lines.append('')

                output_count('Users', users, 0, log_lines)
                output_count('Admin users', admin_users, 1, log_lines)
                output_count('Full admin users', full_admin_users, 2, log_lines)
                output_count('Security admin users', security_admin_users, 2, log_lines)
                output_count('Data admin users', data_admin_users, 2, log_lines)
                output_count('Operations admin users', operations_admin_users, 2, log_lines)
                log_lines.append('')
                output_count('Non-admin users', non_admin_users, 1, log_lines)
                output_count('Read/write users', authorized_users, 2, log_lines)
                output_count('Write users', write_users, 3, log_lines)
                output_count('Read users', read_users, 3, log_lines)
                output_count('Read-only users', read_only_users, 2, log_lines)
                log_lines.append('')
                output_count('Disabled users', disabled_users, 1, log_lines)
                log_lines.append('')
                output_count('Custom TM1 security groups', custom_groups, 0, log_lines)
                log_lines.append('')
                log_lines.append('')

        if OUTPUT_LEVEL[3] == 'Y':
            # get attribute values for the users
            users_dictionary = build_users_attribute_dictionary(tm1)

            # output lists of usernames in the various lists
            log_lines.append('User lists:')
            log_lines.append('-----------')
            log_lines.append('')

            output_list('Admin users', admin_users, users_dictionary, log_lines)
            output_list('Full admin users', full_admin_users, users_dictionary, log_lines)
            output_list('Security admin users', security_admin_users, users_dictionary, log_lines)
            output_list('Data admin users', data_admin_users, users_dictionary, log_lines)
            output_list('Operations admin users', operations_admin_users, users_dictionary, log_lines)
            output_list('Non-admin users', non_admin_users, users_dictionary, log_lines)
            output_list('Read/write users', authorized_users, users_dictionary, log_lines)
            output_list('Write users', write_users, users_dictionary, log_lines)
            output_list('Read users', read_users, users_dictionary, log_lines)
            output_list('Read-only users', read_only_users, users_dictionary, log_lines)
            output_list('Disabled users', disabled_users, users_dictionary, log_lines)

            output_list('Custom TM1 security groups', custom_groups, dict(), log_lines)

        if OUTPUT_LEVEL[4] == 'Y':
            # output list of all usernames
            output_list('All users', all_users, users_dictionary, log_lines)

        if OUTPUT_LEVEL[5] == 'Y':
            # output list of all usernames with their group memberships
            output_list('All users and their groups', all_users_with_groups, None, log_lines)

    with open(RESULT_FILE, 'w', encoding='utf-8') as file:
        file.write("\n".join(log_lines))
        file.close()


def build_users_attribute_dictionary(tm1: TM1Service) -> Dict[str, str]:
    users_dictionary = dict()
    mdx = f"""
        SELECT
        {{Tm1SubsetAll([}}Clients])}} ON ROWS,
        {{[}}ElementAttributes_}}Clients].[{ATTRIBUTE_FOR_CLIENT_NAMES}]}} ON COLUMNS
        FROM [}}ElementAttributes_}}Clients]
    """

    rows_and_values = tm1.cells.execute_mdx_rows_and_values(mdx=mdx, element_unique_names=False)
    for row_elements, values in rows_and_values.items():
        user = row_elements[0]
        value = values[0]
        if value:
            users_dictionary[user] = value

    return users_dictionary


def determine_client_access_level_with_cube_security(tm1: TM1Service, user_name: str):

    cube_security_exists = ("}CubeSecurity" in tm1.cubes.get_all_names())
    if not cube_security_exists:
        return 'W'
    else:
        # loop over all application cubes
        groups = tm1.security.get_groups(user_name)
        cubes = tm1.cubes.get_model_cubes()
        for cube in cubes:
            for group in groups:
                value = tm1.cells.get_value('}CubeSecurity', cube.name + ',' + str(group))
                if value not in ['', 'None', 'Read']:
                    return 'W'

def user_and_groups(tm1: TM1Service, user_name: str):
    
    groups = tm1.security.get_groups(user_name)
    if groups:
        return user_name + ' (' + str(len(groups)) + '): ' + ', '.join(groups)
    else:
        return user_name + ' (0)'


def output_count(text: str, lst: List, indent: int, log_lines: List[str]):
    text = adapt_grammar_in_text(text, len(lst) == 1)
    log_lines.append("\t" * indent + str(len(lst)) + " " + text)


def output_list(text: str, users_list: List[str], users_dictionary: Dict[str, str], log_lines: List[str]):
    if not users_list:
        return

    if users_dictionary:
        users_list = replace_username_in_list(users_list, users_dictionary)

    users_list.sort()

    text = adapt_grammar_in_text(text, len(users_list) == 1)

    log_lines.append(text + " (" + str(len(users_list)) + "):\n\t" + "\n\t".join(users_list) + "\n")


def replace_username_in_list(users_list: List[str], users_dict: Dict[str, str]) -> List[str]:
    if len(users_list) * len(users_dict) == 0:
        return users_list
    else:
        return [users_dict.get(user_name, user_name) for user_name in users_list]


def adapt_grammar_in_text(text: str, exactly_one: bool) -> str:
    if exactly_one:
        text = text.replace('Users', 'User')
        text = text.replace('users', 'user')
        text = text.replace('groups', 'group')

    # convert the first character to lowercase
    return text[0].lower() + text[1:] if text else ''


if __name__ == "__main__":
    inspect_users()
