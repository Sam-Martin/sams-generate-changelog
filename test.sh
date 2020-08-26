/usr/local/bin/pip3.7 uninstall samsgeneratechangelog -y
/usr/local/bin/python3.7 setup.py sdist
/usr/local/bin/pip3.7 install dist/samsgeneratechangelog-0.0.1.tar.gz  --ignore-installed