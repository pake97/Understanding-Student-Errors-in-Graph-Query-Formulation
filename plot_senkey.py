import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib import rcParams
import plotly.graph_objects as go
from collections import Counter
rcParams['axes.titlepad'] = 20 

def getColor(label):
    if("Correct" in label):
        return "#469c75"
    if("SyntaxError" in label):
        return "#939393"
    if("Return" in label):
        return "#d39334"
    if("Where" in label):
        return "#c19469"
    if("Pattern" in label):
        return "#c66626"
    if("Complication" in label):
        return "#6fb1e4"
    if("No" in label or '.' in label):
        return "black"
    if("Absent" in label):
        return "darkgray"
    if("Other" in label):
        return "#3171ad"


class Node():       
         def __init__(self, name,parent):
              self.name = name
              self.children = []
              self.weights = []
              self.parents = parent
              self.index=-1
       
def printTree(node, level):
    print('  ' * level + node.name)
    for child in node.children:
        printTree(child, level + 1)

labels=[]
source=[]
target=[]
weights=[]
def traversal(node):
       for child in node.children:
              labels.append(node.name)
              for count,ch in enumerate(child.children):
                     print(child.name, ch.name)
                     source.append(len(labels)-1)
                     labels.append(ch.name)
                     target.append(len(labels)-1)
                     weights.append(child.weights[count])
              traversal(child)
    
    
    
df = pd.read_csv('Total/Category-Total.csv', delimiter=';')

df = df[['Q1','Q2','Q3','Q4','Q6','Q7','Q8','Q9','Q10','Q11','Q12','Q13',"Q14",'Q15']]
df['Q1']=df['Q1'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q2']=df['Q2'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q3']=df['Q3'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q4']=df['Q4'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q6']=df['Q6'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q7']=df['Q7'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q8']=df['Q8'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q9']=df['Q9'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q10']=df['Q10'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q11']=df['Q11'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q12']=df['Q12'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q13']=df['Q13'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q14']=df['Q14'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
df['Q15']=df['Q15'].fillna('Absent').apply(lambda x: x.split("|")[0].strip(' '))
# melted_error_category_df = df[['Q1','Q2','Q3','Q4','Q6','Q7','Q8','Q9','Q10','Q11','Q12','Q13','Q14','Q15']].melt( var_name='Query', value_name='Label')
# melted_error_category_df=melted_error_category_df.fillna('Absent')

# melted_error_category_df['Label'] =melted_error_category_df['Label'].str.split(',')

# # Explode the DataFrame to create new rows
# melted_error_category_df = melted_error_category_df.explode('Label')
# melted_error_category_df['Label'] = melted_error_category_df['Label'].apply(lambda x: x.strip(' '))
# Display the resulting DataFrame

lista=df.to_numpy().tolist()
Qs=[[] for i in range(14)]
for el in lista:
    for i in range(14):
        label = el[i]
        for lab in label.split(","):
            Qs[i].append(lab)
        

lista2 = [list(set(Q)) for Q in Qs]
combinations =[[] for i in range(14)]
counts = [[] for i in range(14)]


for i in range(14):
    for el in lista:
        if(i<13):
            labels1 = el[i].split(",")
            labels2 = el[i+1].split(",")
            for lab1 in labels1:
                for lab2 in labels2:    
                    if(lab1+"-"+str(i)+";"+lab2+"-"+str(i+1) not in combinations[i]):
                        combinations[i].append(lab1+"-"+str(i)+";"+lab2+"-"+str(i+1))
                        counts[i].append(1)
                    else:
                        index = combinations[i].index(lab1+"-"+str(i)+";"+lab2+"-"+str(i+1))
                        counts[i][index]+=1
                        
print(combinations) 
lista3 = []            
for i in range(len(lista2)):
    for el in lista2[i]:
        lista3.append(el+"-"+str(i))
print(lista3)
print(counts)


values =[]
for count in counts:
    for c in count:
        values.append(c)

sources = []
targets=[]

for combin in combinations:
    for comb in combin:
        labels = comb.split(";")
        sources.append(lista3.index(labels[0]))
        targets.append(lista3.index(labels[1]))

print(sources)
print(targets)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = [lab.split("-")[0] for lab in lista3],
      color = [getColor(lab) for lab in lista3]
    ),
    link = dict(
      source = sources,
      target = targets,
      value = values,
  ))])

fig.update_layout(title_text="Error flow through queries", font_size=20, width=4000,
    height=1500,title_x=0.5)

fig.write_image("fig1.png")
   
