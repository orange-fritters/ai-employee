import os

for filename in os.listdir('data/articles'):
    title = filename.split('_')[0]
    number = filename.split('_')[1].split('.')[0]
    if len(number) == 1:
        number = '0' + number
    new_filename = title + '_' + number + '.html'
    os.rename('data/articles/' + filename, 'data/articles/' + new_filename)
