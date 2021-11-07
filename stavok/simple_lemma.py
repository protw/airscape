import simplemma, re

langdata=simplemma.load_data('uk')

word='Під час робочої поїздки до Запоріжжя провів робочий ланч з головами дипломатичних представництв країн «Великої сімки» #G7. Обговорили питання мирного врегулювання на Донбасі, реформи та трансформацію України.'
tokens = [simplemma.lemmatize(t, langdata) for t in word.split(' ')]

word1=re.sub('[\,\.A-z0-9#«»]','',word)
pat=re.compile("[ ]+")
tokens1 = [simplemma.lemmatize(t, langdata) for t in pat.split(word1)]
