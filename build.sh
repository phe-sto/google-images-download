echo "########## BUILD DOCUMENTATION ##########"
make clean
make html
echo "########## BUILD DISTANT WHEELgoog ##########"
python3 setup.py bdist_wheel