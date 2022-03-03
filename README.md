## Readme

# 3. Ergebnisse

## 3.1 Johanns Plot


```
# We import our data from a csv file
# We order by sigmas
# We capitalize the names of our subjects 

df = pd.read_csv('result_final.csv', encoding='utf-8')
df['sigma'] = pd.Categorical(df['sigma'], ["4", "7", "12", "20", "original"])
df['proband'] = df['proband'].apply(lambda x: x.capitalize())


#catplot alle
g = sns.catplot(x='sigma', y='response', data=df, col ='category', row='rotation',
                kind='point', ci='sd',
                palette='inferno', hue='proband', estimator=np.mean)

g.set_titles('rotation:{row_name} | {col_name}')
g.fig.set_size_inches(20, 10)
plt.subplots_adjust(hspace=0.2)
g.fig.set_dpi(300)
g.set(ylim =(0, 5.5))
g.set(yticks=np.arange(0,6,1))
for ax in g.axes_dict.values():
    ax.axline((0, 1.15),(4,5), ls="--", zorder=100, linewidth=4, color='grey')
sns.move_legend(g, "lower center", bbox_to_anchor=(0.5, -0.1), ncol=7,title='Proband', frameon=True)
```


![Plot_Johann](https://user-images.githubusercontent.com/57091589/156608281-ab36d8a7-e1da-473a-849c-2b114fdb4ff3.png)


## 3.1 Witeks Plot

# 4. Diskussion
