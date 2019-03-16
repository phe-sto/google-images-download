echo "########## TOX REVIEW          ##########"
tox
echo "########## PYLINT REVIEW       ##########"
pylint google_images_download/google_images_download.py
echo "########## COVERAGE AND PYTEST ##########"
coverage run --branch --source=google_images_download -m py.test tests -vv --html=docs/build/html/test/index.html --self-contained-html
coverage xml -i
coverage html -i -d docs/build/html/coverage