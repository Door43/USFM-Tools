doc: clean_doc
	# NOT UPDATED/CHECKED YET
	echo 'building docs...'
	cd docs && sphinx-apidoc --force -M -P -e -o source/ ../usfm_tools
	cd docs && make html

clean_doc:
	# NOT UPDATED/CHECKED YET
	echo 'cleaning docs...'
	cd docs && rm -f source/src.rst
	cd docs && rm -f source/src.*.rst

#load:
#	python usfm_tools/transform.py

test:
	python tests/singlehtml_renderer_tests.py
	#python usfm_tools/support/test/all_test.py

dependencies:
	pip install -r requirements.txt
