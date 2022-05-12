# > Media.html
curl https://tvtropes.org/pmwiki/pmwiki.php/Main/Media --output Media.html
# > Media.html.json
python Media.py Media.html
# > Media.json
python -m json.tool Media.html.json > Media.json
# > Tropes.py.d & Tropes.py.d.json
python Tropes.py
# > Tropes.json
python -m json.tool Tropes.py.d.json > Tropes.json
# > Media.json.json
python MediaUrls.py Media.json Tropes.py
# > Media.d.json
python -m json.tool Media.json.json > Media.d.json
# > Media.d.json.d
python Downloader.py Media.d.json
# > Tropes.json.d
python Downloader.py Tropes.json
# > Media.d.json.d.json & Media.d.json.d.map.json
python SubPages.py Media.d.json.d Tropes.json
# > SubPages.json
python -m json.tool Media.d.json.d.json > SubPages.json
# > SubPages.json.d
python Downloader.py SubPages.json
# > MediaTropes.json
python -m json.tool Media.d.json.d.map.json > MediaTropes.json
# > MediaTropes.json.json
python Expander.py MediaTropes.json Tropes.json SubPages.json.d
# > Expansion.json
python -m json.tool Expander.py.json > Expansion.json
# > Final.json
python -m json.tool MediaTropes.json.json > Final.json
# > References.py.json & References.py.map.json & Summaries.py.json
python References.py Final.json Media.d.json Tropes.json Subpages.json.d
# > Summaries.json
python -m json.tool Summaries.py.json > Summaries.json
# > models
python -m pip install -r requirements.txt
python trope2vec.py --references=./References.py.json --summaries=./Summaries.json
