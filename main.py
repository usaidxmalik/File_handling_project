from pathlib import Path
import os


def createfile():
    name = input('Enter Name of file: ')
    path = Path(name)
    try:
        if not path.exists():
            with open(path, 'w') as f:
                data = input('Enter Data to write in file: ')
                f.write(data)
        else:
            print('Error: File already exists!')
    except Exception as err:
        print(f'Error Occured: {err}')

def readfile():
    name = input('Tell your file name to read: ')
    path = Path(name)
    try:    
        if path.exists():
            with open(path, 'r') as f:
                data = f.read()
                print(f'File Data: {data}')
        else:
            print('Error: File does not exist!')
    except Exception as err:
        print(f'Error Occured: {err}')

def writefile():
    name = input('Tell file name to write: ')
    path = Path(name)
    try:
        if path.exists():
                print('Operations:\n')
                print('1. Rename file')
                print('2. Append Data')
                print('3. Overwrite file')
                choice = int(input('Enter your choice: '))
                if choice == 1:
                    newname = input('Enter new Name of file: ')
                    newpath = Path(newname)
                    if not newpath.exists():
                        path.rename(newpath)
                        print('File renamed successfully!')
                    else:
                        print('Error: File already exists!')

                elif choice == 2:
                    with open(path, 'a') as f:
                        data = input('Enter Data to append in file: ')
                        f.write('\n' + data)
                    print('Data appended successfully!')

                elif choice == 3:
                    with open(path, 'w') as f:
                        data = input('Enter Data to overwrite in file: ')
                        f.write(data)
                    print('Data overwritten successfully!')

        else:
            print('Error: File does not exists!')
    except Exception as err:
        print(f'Error Occured: {err}')

def deletefile():
    name = input('Tell file name to delete: ')
    path = Path(name)
    try:
        if path.exists():
            path.unlink()
            print('File deleted successfully!')
        else:
            print('Error: File does not exists!')
    except Exception as err:
        print(f'Error Occured: {err}')

print('Press-1 for creating a file')
print('Press-2 for reading a file')
print('Press-3 for writing to a file')
print('Press-4 for deleting a file')


choice = int(input('\nEnter your choice: '))

if choice == 1:
    createfile()
elif choice == 2:
    readfile()
elif choice == 3:
    writefile()
elif choice == 4:
    deletefile()    
