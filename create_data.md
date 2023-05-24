## Install fastcoref

1. clone full repo
2. copy training_thai.patch to fastcoref/
3. run apply patch

> git apply training_thai.patch

4. Install by

> pip install -e .

## Steps


1. label the data in data/, save as .txt file and add file to reqo.json
2. run
> python build.py

and fix the error

3. train the model by train____.py (Don't forget edit file dataset)