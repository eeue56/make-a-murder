#!/usr/bin/python2

import subprocess as sp
from subprocess import PIPE
import os
import shutil


folder = 'sausage'
my_name = 'Robot Dog'
my_first_names = ['James', 'Robert', 'Rupe', 'Thomas']
my_second_names = ['Davies', 'Doge', 'Butcher', 'Newson']

def minimal(command):
    MIN_LENGTH = 1
    name = sp.check_output(command, stderr=PIPE)

    assert len(name.split()) > 1, "Names should have two parts!"
    assert all(len(part) > MIN_LENGTH 
        for part in name.split()), "Each part should be longer than %d!" % MIN_LENGTH
    
def with_random(command):
    names = []

    for _ in xrange(100):
        names.append(sp.check_output(command, stderr=PIPE))
        if len(set(names)) > 1: break
    else:
        assert len(set(names)) > 1, "Names should be generated at random!"


def with_files(command):
    names = []

    for _ in xrange(100):
        names.append(sp.check_output(command, stderr=PIPE))
        if len(set(names)) > 1: break
        assert names[-1].split()[0] in my_first_names, "First name should be taken from file."
        assert names[-1].split()[1] in my_second_names, "Second name should be taken from file."
    else:
        assert len(set(names)) > 1, "Names should be generated at random!"


def initials(command):
    name = sp.check_output(command, stderr=PIPE)

    assert name != my_name, 'A new name must be generated!'
    assert name.split()[0][0] == my_name.split()[0][0], 'Initials must be the same!'
    assert name.split()[-1][0] == my_name.split()[-1][0], 'Initials must be the same!'

def main(files):
    file = files[0]

    first_names_file = folder + '/first_names'
    second_names_file = folder + '/second_names'

    command = ['./' + file]

    os.mkdir(folder)

    with open(first_names_file, 'w') as f:
        f.write('\n'.join(my_first_names))

    with open(second_names_file, 'w') as f:
        f.write('\n'.join(my_second_names))


    command.append(first_names_file)
    command.append(second_names_file)
    command.append(my_name)
    

    checks = [minimal, initials, with_random, with_files]
    
    for check in checks:
        try:
            check(command)
        except Exception as e:
            print e.message


if __name__ == '__main__':
    import sys

    try:
        main(sys.argv[1:])
    except:
        raise
    finally:
        shutil.rmtree(folder)
