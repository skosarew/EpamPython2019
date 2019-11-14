pizza = {"dough", "tomatoes", "pepperoni", "ground pepper", "sweet basil",
         "a lot of cheeeese", "onion", "garlic", "salt", "oregano"}
shaverma = {"lavash", "cucumbers", "tomatoes", "sauce", "fried chicken", "onion", "cabbage"}

print('pizza - shaverma:', pizza.difference(shaverma))
print('shaverma - pizza:', shaverma.difference(pizza))
print('intersection:', pizza.intersection(shaverma), '\n')

print('pizza is subset of shaverma:', pizza.issubset(shaverma))
print('shaverma is subset of pizza:', shaverma.issubset(pizza))
print('pizza is supperset of shaverma:', pizza.issuperset(shaverma))
print('shaverma is supperset of pizza:', shaverma.issuperset(pizza), '\n')

print('pizza | shaverma:', pizza | shaverma)
print('pizza ^ shaverma:', pizza ^ shaverma)
