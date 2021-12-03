import os
from os.path import join
import random
cwd = os.getcwd()
VAL_PART = 0.15
try:
    os.mkdir(join(cwd, 'dataset'))
    os.mkdir(join(cwd, 'dataset', 'tmp'))
    os.mkdir(join(cwd, 'dataset', 'images'))
    os.mkdir(join(cwd, 'dataset', 'labels'))
    os.mkdir(join(cwd, 'dataset', 'images', 'train'))
    os.mkdir(join(cwd, 'dataset', 'images', 'val'))
    os.mkdir(join(cwd, 'dataset', 'labels', 'train'))
    os.mkdir(join(cwd, 'dataset', 'labels', 'val'))
except:
    pass


counter = 0
for folder in [f for f in os.listdir(join(cwd, 'trash')) if not os.path.isfile(join(join(cwd, 'trash'), f))]:
    folder = join(cwd, 'trash', folder)
    for file in [f for f in os.listdir(folder) if os.path.isfile(join(folder, f)) and os.path.splitext(f)[-1] == ".txt"]:
        filename, _ = os.path.splitext(file)
        os.replace(join(folder, filename + '.txt'), join(cwd, 'dataset', 'tmp', str(counter) + '.txt'))
        os.replace(join(folder, filename + '.png'), join(cwd, 'dataset', 'tmp', str(counter) + '.png'))
        counter += 1

filenames = [f for f in range(counter)]
random.shuffle(filenames)
val_len = int(len(filenames) * VAL_PART)
train_len = len(filenames) - val_len
train_files = filenames[:train_len]
val_files = filenames[train_len:]
for file in train_files:
    file = str(file)
    os.replace(join(cwd, 'dataset', 'tmp', file + '.txt'), join(cwd, 'dataset', 'labels', 'train', file + '.txt'))
    os.replace(join(cwd, 'dataset', 'tmp', file + '.png'), join(cwd, 'dataset', 'images', 'train', file + '.png'))
for file in val_files:
    file = str(file)
    os.replace(join(cwd, 'dataset', 'tmp', file + '.txt'), join(cwd, 'dataset', 'labels', 'val', file + '.txt'))
    os.replace(join(cwd, 'dataset', 'tmp', file + '.png'), join(cwd, 'dataset', 'images', 'val', file + '.png'))

