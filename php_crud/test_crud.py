# Run this as:
#  python3 -m pytest -v -s test_crud.py
#
# TODO: parametrize url with host paramter, do not use hardcoded "localhost"

import pytest
import json
import random
import string
import subprocess

def random_string(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

tname=random_string()
tsurname=random_string()
tuid=None

@pytest.fixture
def name():
    return tname

@pytest.fixture
def surname():
    return tsurname

@pytest.fixture
def uid():
    return tuid

def test_create(name, surname):
    result = subprocess.run(['curl', 'localhost/crud.php?method=create&name={}&surname={}'.format(name, surname)], stdout=subprocess.PIPE, shell=False, check=True, universal_newlines=True)
    assert result.returncode == 0, "Unexpected return code. {}".format(result)
    assert result.stdout == '', "Unexpected stdout. {}".format(result)

def test_read(name, surname):
    global tuid
    result = subprocess.run(['curl', 'localhost/crud.php?method=read'], stdout=subprocess.PIPE, shell=False, check=True, universal_newlines=True)
    assert result.returncode == 0, "Unexpected return code. {}".format(result)
    stdout_lines = result.stdout.splitlines()
    new_user = [ json.loads(line) for line in stdout_lines if name in line and surname in line]
    assert len(new_user) == 1 , "User name: {}, surname: {}, not present in the db: {}".format(name, surname, result.stdout)
    tuid = new_user[0]['uid']
    print(new_user)

def test_update(uid, name, surname):
    assert uid != None , "Error: Unable to delete user wit uid: {}".format(uid)
    new_name = random_string()
    new_surname = random_string()
    result_u = subprocess.run(['curl', 'localhost/crud.php?method=update&uid={}&name={}&surname={}'.format(uid, new_name, new_surname)], stdout=subprocess.PIPE, shell=False, check=True, universal_newlines=True)
    assert result_u.returncode == 0, "Unexpected return code. {}".format(result_u)
    assert result_u.stdout == '', "Unexpected stdout. {}".format(result)
    result = subprocess.run(['curl', 'localhost/crud.php?method=read'], stdout=subprocess.PIPE, shell=False, check=True, universal_newlines=True)
    stdout_lines = result.stdout.splitlines()
    new_user = [ json.loads(line) for line in stdout_lines if new_name in line and new_surname in line]
    assert len(new_user) == 1 , "User name: {}, surname: {}, not present in the db: {}".format(new_name, new_surname, result.stdout)
    odl_user = [line for line in stdout_lines if name in line and surname in line]
    assert len(odl_user) == 0 , "User name: {}, surname: {}, still present in the db: {}".format(name, surname, result.stdout)

def test_delete(uid):
    assert uid != None , "Error: Unable to delete user wit uid: {}".format(uid)
    result_d = subprocess.run(['curl', 'localhost/crud.php?method=delete&uid={}'.format(uid)], stdout=subprocess.PIPE, shell=False, check=True, universal_newlines=True)
    assert result_d.returncode == 0, "Unexpected return code. {}".format(result_u)
    assert result_d.stdout == '', "Unexpected stdout. {}".format(result)
    result = subprocess.run(['curl', 'localhost/crud.php?method=read'], stdout=subprocess.PIPE, shell=False, check=True, universal_newlines=True)
    stdout_lines = result.stdout.splitlines()
    user = [line for line in stdout_lines if uid == json.loads(line)['uid']]
    assert len(user) == 0 , "User uid: {}, still present in the db: {}".format(uid, result.stdout)

