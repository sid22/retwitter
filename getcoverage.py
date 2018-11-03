import os
os.system("coverage erase")
print("\nInitiating test run\n")
os.system("coverage run --source='.' manage.py test")
os.system("coverage html")
print("\n\nCoverage report is:-\n")
os.system("coverage report")
