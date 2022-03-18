# 1. Einleitung

Die menschliche Bildwahrnehmung lässt sich nicht klar dem Full-Reference oder dem No-Reference Modell nach Wang & Bovik [1] zuweisen. Die gestellte Forschungsfrage lautet: _"Haben Menschen für die Beurteilung von Bildern eine interne Referenz?"_. Eine Ableitung der Forschungsfrage ist folgende Hypothese: _"Wenn Menschen bei der Bildbeurteilung eine interne Referenz benutzen, dann fallen Verzerrungen von Bildern eher bei geläufigen als bei unbekannten Bildern auf."_ Die nachfolgende Dokumentation beschreibt den Vorgang wie die Hypothese getestet und die Forschungsfrage beantwortet wurde.

# 2. Experimentelles Design

Bei unserem [Experiment](https://github.com/NerdPixel/PiQ/blob/cc3c3b79f3a0d35dc361841364cd1d36b6f7e2d9/rating_experiments/rating_experiment_single.py) haben wir uns für das Mean Opinion Score (MOS) Verfahren entschieden.
Insgesamt haben wir drei Kategorien an Bildern, pro Kategorie haben wir zehn Beispielbilder, jedes Bild haben wir fünf mal Verzerrt und einmal rotiert und einmal nicht rotiert.
Daraus ergibt sich also 3 * 10 * 5 * 2  = 300. Im Vorfeld haben wir die Bilder per Hand auf 1200x1200 Pixel zugeschnitten.

Für die JPG-Kompression haben wir die Implementation der PIL Libary für Python genutzt.
Als Parameter für die Komprimierung haben wir uns für 20, 12, 7, 4 und Original entschieden. Die Probanden benötigten zwischen 9 bis 21 Minuten für einen gesamten Durchlauf. Insgesamt hatten wir sieben Probanden.
```
def generate_imgs(f: dict):
    #f dict of (filename, loaded image)
    sigmas = [20, 12, 7, 4]
    size = 1200, 1200
    logging.debug(f"sigmas: {sigmas}")
    
    # generate dir name
    sigmas_str = map(str, sigmas)
    sigmas_str = '_'.join(sigmas_str)
    logging.debug(f"sigmas_str: {sigmas_str}")
    
    # create dir
    path = "./img_out/"+sigmas_str
    if os.path.isdir(path):
        os.rmdir(path)
    os.mkdir(path)
    
    # generate jpgs
    f_jpg = generate_jpg(f.copy(), sigmas)
    logging.debug("saved files")
    
    # save jpgs to file
    i = 0
    for file_name, file in f_jpg.items():
        logging.debug(f'./img_out/{sigmas_str}/'+file_name)
        im = Image.fromarray(file)
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(f'./img_out/{sigmas_str}/'+file_name)
        i += 1
    logging.debug(f"saved images #{i}")
```

```
def generate_jpg(f, sigmas):
    f_jpg = f.copy()
    logging.debug("generating jpgs...")
    i = 0
    for sigma in sigmas:
        for file in f.keys():
            logging.debug(f"generate {file} with quality {int(sigma)}")
            im = f[file].copy()
            buffer = BytesIO()
            Image.fromarray(im).save(buffer , 'jpeg', quality=int(sigma))
            im = Image.open(buffer)
            im = np.array(im)
            filename = rename_file(file, '_'+str(sigma))
            f_jpg[filename] = im
            logging.debug(f"source file: {file}")
            logging.debug(f"dest file:   {filename}")
            i += 1
                      
    logging.debug(f"generated images #{i}")
    return f_jpg
```
Die generierten Bilder sind [hier](img_out/final_20_12_7_4) zu finden. Die nachfolgenden Bilder sind repräsentativ für die drei Inhaltskategorien Portrait, Nature und Art. [Hier](images.md) sind die original Bilder.

<img width="1358" alt="Screenshot 2022-03-13 at 16 13 07" src="https://user-images.githubusercontent.com/57091589/158066579-cbf58a8b-cb67-435d-9455-6e3898257397.png">


# 3. Ergebnisse
To do: hyperlinks zu notebooks

To do: Plot Namen ändern

To do: Kommentare im Code englisch _oder_ deutsch

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

## Referenzen
[1]	Z. Wang and A. C. Bovik, “Modern image quality assessment,” Synth. Lect. Image Video Multimed. Process., vol. 2, no. 1, p. 12, 2006.

