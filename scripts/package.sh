read -p "Increment version number now. Press any key to continue or ctrl + c to exit.. " 
vim ../setup.py
rm ../dist/*
python ../setup.py sdist
twine upload ../dist/*

