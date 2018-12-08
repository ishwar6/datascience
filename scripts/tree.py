from sklearn import tree


x = [[180, 111, 21], [111, 111, 33]]


y = ['male', 'female']


clf = tree.DecisionTreeClassifier()

clf = clf.fit(x, y)

prediction = clf.predict([[122, 232, 44]])

print(prediction)
