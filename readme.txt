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
# > models/*
python -m pip install -r requirements.txt
python trope2vec.py --references=./References.py.json --summaries=./Summaries.json
python
>>> from gensim.models.word2vec import Word2Vec
>>> model = Word2Vec.load("./models/t2v-retrofit.model")
>>> print(model.wv.most_similar("frog"))
[('Hector', 0.9999973773956299), ('Speed', 0.9999970197677612), ('Brad', 0.9999969005584717), ('conversation', 0.9999968409538269), ('Nebula', 0.9999967813491821), ('Lieutenant', 0.9999967217445374), ('loose', 0.9999967217445374), ('bought', 0.9999967217445374), ('Mung', 0.9999967217445374), ('IN', 0.9999966621398926)]
>>> # https://tvtropes.org/pmwiki/pmwiki.php/WesternAnimation/HectorsHouse
