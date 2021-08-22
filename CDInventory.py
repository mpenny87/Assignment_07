#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# mpenny, 2021-Aug-13, Updated file by creating more functions and moving code into them
# mpenny, 2021-Aug-19, Updated file by adding error handling and binary file storage
#------------------------------------------#

import sys
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
#strFileName = 'CDInventory.txt'  # old data storage file
strDatName = 'CDInventory.dat'
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    '''Manipulating and processing data directly for various purposes'''
    
    @staticmethod
    def add_Dictionary(inputTpl, table):
        """Function used to create a dictionary object and append it to a list object

        Takes a tuple as output from another function and maps it to a dictionary object
        which is then added onto a 2d data structure (list of dicts)
        Args:
            inputTpl: a tuple that consists of an ID, Title, and Artist that is the product of another function
            table: 2D data structure (list of dicts) that holds the data during runtime and is added to. 

        Returns:
            None.
        """

        intID = int(inputTpl[0])
        dicRow = {'ID': intID, 'Title': inputTpl[1], 'Artist': inputTpl[2]}
        table.append(dicRow)
        IO.show_inventory(lstTbl)

    
    @staticmethod
    def Delete_CD(delInt, table):
        """Function used to delete an entry from a 2d data structure (list of dicts) based off user input

        Takes an interger based entry set by a user and then checks the list of dicts for it. If found, it
        removes the associated row with the matching ID and prints a confirmation. Else, it reports a not
        found message.
        Args:
            delInt: an interger entered by a user cooresponding to an item they want removed from the table.
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            and is removed from. 

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from binary file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.
        Method currently has a bug where it destroys file content upon load, then throws an
        EOF statement on the pickle.load(objFile) line. Otherwise, uses a try/except statement
        to see if the file exists before loading it.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            objFile = open(file_name, 'rb')
        except FileNotFoundError as e:
            print('The file was not found. Make sure it exists before running the program')
            print(e)
            sys.exit()
        pclObject = pickle.load(objFile)
        for line in pclObject:
            table.append(line)
        objFile.close()
        
    @staticmethod
    def write_file(file_name, table):
         """Function used to write data in a CD inventory list to a binary file using pickling
         also throws an OSerror if the file cannot be written to as part of a try/except statement

        Writes the data from the 2 dimensional data object (table) to a text file
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
    try:    
        with open(strDatName, 'wb') as objFile:
            print('opening file...')
    except OSError as e:
        print('Error writing to file. Ensure that the file is able to be written to.')
        print(e)  
        with open(strDatName, 'wb') as objFile:
            for row in lstTbl:
                lstValues = list(row.values())
                lstValues[0] = str(lstValues[0])
                pickle.dump(lstTbl, objFile)
            print('Data written to file!')
            objFile.close()
    
# -- PRESENTATION (Input/Output) -- #

class IO:
    
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def add_CD():
        """Used to interactively gather data from a user by presenting prompts and cleaning up data entered
        before it is returned as a tuple of three objects. Uses error handling to reject non-integer ID entries
        and will end program to prevent invalid entries which cause problems elsewhere


        Args:
            None.

        Returns:
            A tuple of three objects that the user entered during runtime of the function: ID, Title, and Artist

        """
        try:
            strID = int(input('Enter ID: ').strip())
        except ValueError as e:
            print('invalid entry - supply only an integer for a selection.')
            print(e)
            sys.exit()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, stArtist


# 1. When program starts, read in the currently saved Inventory
#Disabled - will always throw EOF error no matter the content of the file
#FileProcessor.read_file(strDatName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    #Invokes the read_file method - currently has a bug that destroys binary file content and produces an error
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strDatName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        usrInput = IO.add_CD()
        DataProcessor.add_Dictionary(usrInput,lstTbl)
        # 3.3.2 Add item to the table

        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        # try to cast input to int, break if exeception triggers
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print('invalid entry - supply only an integer for a selection.')
            print(e)
            break
        # 3.5.2 search thru table and delete CD
        DataProcessor.Delete_CD(intIDDel,lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            #Function doesn't work as expected, cloned code into main body and it works
            #FileProcessor.write_file(strDatName,lstTbl)
            try:    
                with open(strDatName, 'wb') as objFile:
                    print('opening file...')
            except OSError as e:
                print('Error writing to file. Ensure that the file is able to be written to.')
                print(e)  
            with open(strDatName, 'wb') as objFile:
                for row in lstTbl:
                    lstValues = list(row.values())
                    lstValues[0] = str(lstValues[0])
                    pickle.dump(lstTbl, objFile)
            objFile.close()
            print('Data written to file!')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




