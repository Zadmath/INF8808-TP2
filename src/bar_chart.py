'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio

from hover_template import get_hover_template
from modes import MODES, MODE_TO_COLUMN


def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = go.Figure()

    # TODO : Update the template to include our new theme and set the title

    fig.update_layout(
        template=pio.templates['simple_white+custom_template'],  # Utilisation du thème personnalisé
        title="Line per act",
        title_x=0,
        xaxis_title="Act",
        yaxis_title="Line Count",
        dragmode=False,
        barmode='stack'
    )

    return fig


def draw(fig, data, mode):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    # TODO : Update the figure's data according to the selected mode

    #Récupération de la colonne appropriée en fonction du mode sélectionné
    column=MODE_TO_COLUMN[mode]

    # Ajout des barres pour chaque joueur
    for player in data['Player'].unique():
        player_data = data[data['Player'] == player]  # Filtre par joueur
        if not player_data.empty:
            fig.add_trace(go.Bar(
                x=[f'Act {act}' for act in player_data['Act']],  # Axe X : actes
                y=list(player_data[column]),  # Axe Y : données en fonction du mode
                name=player,  # Nom du joueur pour la légende
                hovertemplate=get_hover_template(player, mode)  # Info-bulle personnalisée
            ))

    # Mise à jour de la mise en page
    fig.update_layout(
        xaxis_title="Act",  # Titre de l'axe X
        yaxis_title="Lines (%)" if mode == MODES['percent'] else "Lines (Count)",  # Axe Y selon le mode
        barmode='stack',  # Mode empilé
        legend_title="Player"  # Titre de la légende
    )

    return fig


def update_y_axis(fig, mode):
    '''
        Updates the y axis to say 'Lines (%)' or 'Lines (Count) depending on
        the current display.

        Args:
            mode: Current display mode
        Returns: 
            The updated figure
    '''
    # TODO : Update the y axis title according to the current mode
    fig = go.Figure(fig) 
    y_axis_title = "Lines (%)" if mode == MODES['percent'] else "Lines (Count)"
    fig.update_layout(yaxis_title=y_axis_title)  # Mise à jour du titre de l'axe Y
    return fig