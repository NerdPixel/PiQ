## Readme

# 3. Ergebnisse

## 3.1 Johanns Plot
In der folgenden Abbildung sind auf der x-Achse die Verzerrungsstufen abgebildet und der y-Achse die einzelnen Antwortmöglichkeiten. Die einzelnen Diagramme sind nach Rotation und Bildkategorie aufgeteilt. Es wird also die durchschnittliche Antwort pro Verzerrungsgrad abgebildet, getrennt nach Rotation und Bildkategorie. Die einzelnen farblich getrennten Linien sind das Antwortverhalten jeweils eines Probanden.
Bei perfektem Antwortverhalten würden wir diese alle auf der grau gestrichelten Linie erwarten.

Die Streuung der Probanden von der optimalen Linie bei Portraits fällt deutlich geringer aus als bei den anderen beiden Kategorien. Besonders gut ist dies an den Extremwerten zu sehen. Es lässt sich jedoch kein Unterschied zwischen den Kurvenverläufen in Abhängigkeit von der Rotation erkennen. Daraus schließen wir, dass die Rotation keinen Einfluss auf die erkennbarkeit von Verzerrungen hat.


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
In der folgenden Abbildung sind Histogramme über die einzelnen Antwortmöglichkeiten dargestellt. Jeder einzelne Plot stellt eine mögliche Verzerrungsstufe, von links stärkster zu rechts schwächster. Die einzelnen Balken sind farblich nach Kategorien getrennt.
Die Erwartung bei dieser Darstellung ist durch die grau gestrichelte Linie markiert. Die Kategorie Portraits folgt am stärksten diesem Schema. Im Gegensatz dazu werden die ungeläufigeren Kategorien (Art, Nature) schlechter bewertet. Daraus folgt, dass Verzerrungen von inhaltlich geläufigen Bildern besonders stark auffallen.


```
# catplot für alle probanden
g = sns.catplot(x='response', data=df, hue='category', kind='count',
                palette='inferno', col='sigma')
g.set(xlabel='Response', ylabel='#Response')
plt.tight_layout()
g.fig.set_dpi(300)
x_axis = np.arange(-0.5, 4.5, 0.001)
for ax, sigma in zip(g.axes_dict.values(), sorted(list(df['response'].unique()))):
    ax.plot(x_axis, norm.pdf(x_axis,sigma-1,0.8)*200+3, ls="--", zorder=100, linewidth=4, color='grey')
sns.move_legend(g, "center left", bbox_to_anchor=(-0.1, 0.6), ncol=1, title='Category', frameon=True)
```
![Plot_Witek](https://user-images.githubusercontent.com/57091589/156609290-058902b3-a186-4b51-8bdc-6a5c5b977c5d.png)

## Qualitative Beobachtungen
Bei den Portraits haben Probanden berichtet, dass die Kompressionsstufe sehr gut am Hintergrunde erkennbar war. Es bildeten sich schon bei niedrigen Kompressionsstufen für JPEG typische Artefakte.

# 4. Diskussion
Bezogen auf die Fragestellung: _"Haben Menschen für die Beurteilung von Bildern eine interne Referenz?"_ heißt das, dass Menschen eine innere Referenz für die Beurteilung von Bildern zu besitzen scheinen. Bezogen auf die Hypothese: _"Wenn Menschen bei der Bildbeurteilung eine interne Referenz benutzen, dann fallen Verzerrungen von Bildern eher bei geläufigen als bei unbekannten Bildern auf."_, lässt sich schließen: Verzerrungen inhaltlich geläufiger Bilder wurden von den Probanden eher erkannt, als Verzerrungen inhaltlich unbekannter Bilder. Das gleiche lässt sich nicht zu geometrischer Geläufigkeit sagen.
Es gibt also Evidenz dafür, dass die Hypothese stimmt.

## Mögliche Probleme
Eine Kalibrierung des Experiments hätte Ausreißer wie Philipp vorbeugen können.
Zudem hätten wir mehr Probanden suchen können um mehr Daten zu erheben und so die Aussagekraft des Experiments zu steigern.
Zu guter letzt könnten die JPEG-Stufen bessere Abstände zueinander haben, so dass einer eindeutigere Zuordnung der Bewertungstufen zu erleichtern.


## Offene Fragen
