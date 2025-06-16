import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages



df = pd.read_csv('data/20240401_20250401.csv')
targets = ['pale_ale', 'lager', 'ipa', 'white_beer', 'dark_beer', 'fruit_beer']
variables = [col for col in df.columns if col not in targets + ['date']]

with PdfPages('data/correlations.pdf') as pdf:
    for target in targets:
        n_vars = len(variables)
        cols = 4
        rows = (n_vars + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(25, 5 * rows))
        axes = axes.flatten()

        for i, var in enumerate(variables):
            ax = axes[i]
            sns.scatterplot(x=df[var], y=df[target], ax=ax)
            corr = df[[var, target]].corr().iloc[0, 1]
            ax.set_title(f'Corr: {corr:.2f}')
            ax.set_xlabel(var)
            ax.set_ylabel(target)

        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)
