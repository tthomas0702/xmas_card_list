#!/usr/bin/python3


'''
ver 0.0.1
Script to keep xmass list
'''


import os
import argparse
import sys
import pickle



### Arguments parsing section ###
def cmd_args():
    """Handles command line arguments given."""
    parser = argparse.ArgumentParser(description='This is a tool for resetting '
                                                 'a repro slot')
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        default=False,
                        help='enable debug')
    parser.add_argument('-n',
                        '--name',
                        action='store',
                        dest='repro_name',
                        #required=True,
                        default='none',
                        help='name used to distinguish the repro')
    parser.add_argument('-s',
                        '--slot',
                        type=int,
                        action='store',
                        dest='slot_number',
                        required=False,
                        #default='100',
                        help='repro slot to restore values 1-4 accepted')
    parser.add_argument('-u',
                        '--username',
                        action='store',
                        dest='username',
                        #required=True,
                        default='root',
                        help='root user name for devices')
    parser.add_argument('-p',
                        '--password',
                        action='store',
                        dest='password',
                        #required=True,
                        default='default',
                        help='root password to connect to devices')
    parser.add_argument('-U',
                        '--admin-Username',
                        action='store',
                        dest='admin_username',
                        #required=True,
                        default='admin',
                        help='admin user name for devices')
    parser.add_argument('-P',
                        '--admin-password',
                        action='store',
                        dest='admin_password',
                        #required=True,
                        default='admin',
                        help='admin password to connect to devices')
    parser.add_argument('-m',
                        '--map-update',
                        action='store_true',
                        default=False,
                        help='update SR Map ')
    parser.add_argument('-r',
                        '--remove',
                        action='store_true',
                        default=False,
                        help='remove slot from  SR Map ')


    parsed_arguments = parser.parse_args()

    # debug set print parser info
    if parsed_arguments.debug is True:
        print(parsed_arguments)


    return parsed_arguments

### END ARGPARSE SECTION ###


class XmasDict:
    'SR dict class'
    def __init__(self,):

        self.loaded_xmas_map = self.get_xmas_map_dict()


    def get_xmas_map_dict(self):
        'create if file is not existing and open file'
        try:
            xmas_map_dict = self.open_xmas_map_dict()
        except FileNotFoundError:
            print('** No config file found **\nCreating one...')
            self.create_xmas_dict_file()
            file_created = self.set_xmas_map_dict_file_location_var()
            print('created file {}'.format(file_created))
            xmas_map_dict = self.open_xmas_map_dict()

        return xmas_map_dict


    def open_xmas_map_dict(self):
        'open dict file'
        file_name = self.set_xmas_map_dict_file_location_var()
        infile = (open(file_name, 'rb'))
        xmas_map_dict = pickle.load(infile)
        infile.close()

        return xmas_map_dict


    def set_xmas_map_dict_file_location_var(self):
        'declare variable for xmas_map_dict'
        home = self.home_dir()
        xmas_map_dict_file_location = '{}/code/xmas_card_list/data/xmas_map.dict'.format(home)

        return xmas_map_dict_file_location


    def create_xmas_dict_file(self, new_dict={}):
        '''
        create a config dir and dict file in user dir to map current SR for slot
        /home/<USER>/.repro_slot_reset/xmas_map.dict
        '''
        xmas_map_dict = new_dict
        file_name = self.set_xmas_map_dict_file_location_var()
        # create dir if not exsts
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        outfile = open(file_name, 'wb')
        pickle.dump(xmas_map_dict, outfile)
        outfile.close()


    def home_dir(self):
        'returns the home dir'
        home = os.path.expanduser("~")

        return home


    def print_map(self):
        'print out current '
        #print('** Current Christmas List  **')
        for k in sorted(self.loaded_xmas_map.keys(), reverse=True):
           m = self.loaded_xmas_map[k]
           print('** {} **\n'.format(k))
           print('{}'.format(m['family_name']))
           print('{}'.format(m['address1']))        
           if m['address2']:
               print('{}'.format(m['address2']))
           print('{}'.format(m['city']))
           print('{}'.format(m['state']))
           print('{}'.format(m['zip_code']))
           print('\n*** END {} ***\n\n'.format(k))

    # add key:val to /home/<USER>/.repro_slot_reset/xmas_map.dict
    def update_xmas_map_dict(self, fam_key, family_name, address1, address2, city, state, zip_code ):
        'update xmas_dict'
        self.loaded_xmas_map[fam_key] = {'family_name': family_name,
                                             'address1': address1,
                                             'address2': address2,
                                             'city': city,
                                             'state': state,
                                             'zip_code': zip_code}
        self.save_current_xmas_map_dict_to_file()
        return self.loaded_xmas_map

    def save_current_xmas_map_dict_to_file(self):
        'save current xmas_dict to file'
        file_name = self.set_xmas_map_dict_file_location_var()
        outfile = open(file_name, 'wb')
        pickle.dump(self.loaded_xmas_map, outfile)
        outfile.close()

    def delete_key_xmas_map_dict(self, key=None):
        'remove entry from the SR list'
        if not key:
            sys.exit('goodbye')
        else:
            try:
                del self.loaded_xmas_map[key]
                self.save_current_xmas_map_dict_to_file()
            except KeyError:
                print('{} key not found'.format(key))
                sys.exit('Exiting')


if __name__ == "__main__":

    OPT = cmd_args()
    UPDATE = OPT.map_update
    REMOVE = OPT.remove
    SCRIPT_NAME = sys.argv[0]



    MAP = XmasDict()
    MAP.print_map()

    if UPDATE:
        FAM_KEY = input('Enter key for family: ')
        FAMILY_NAME = input('Enter blank to exit or family name you want to modify: ')
        #NAME_META = input('enter name meta: ')
        ADDY1 = input('Adress line 1 for: ')
        ADDY2 = input('Adress line 2 for: ')
        CITY = input('City: ')
        STATE = input('State: ')
        ZIP = input('zip code: ')

        MAP.update_xmas_map_dict(FAM_KEY, FAMILY_NAME, ADDY1, ADDY2, CITY, STATE, ZIP)
        MAP.save_current_xmas_map_dict_to_file()
        print('Saving xmas_dict...')
        MAP.print_map()

    if REMOVE:
        FAMILY_NAME = input('Enter the family name you want to remove: ')
        MAP.delete_key_xmas_map_dict(FAMILY_NAME)
        MAP.save_current_xmas_map_dict_to_file()
        print('Saving xmas_dict...')
        MAP.print_map()
