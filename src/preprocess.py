'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN


def summarize_lines(my_df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PlayerPercent'

        Args:
            my_df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # TODO : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act

    # On enlève les colonnes inutiles
    my_df=my_df.drop(columns=['Line','Scene'])
    # Comptage des lignes par acte et joueur
    my_df = my_df.groupby(['Act', 'Player']).count().reset_index()
    # Ajout des pourcentages
    my_df['PercentCount'] = my_df['PlayerLine'] / my_df.groupby('Act')['PlayerLine'].transform('sum') * 100
    
    return my_df


def replace_others(my_df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other plyaers
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    # TODO : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage

    # On récupère le nom des 5 personnages avec le plus lignes 
    nom=my_df.groupby(['Player']).sum().sort_values(['PlayerLine']).tail(5).index

    #On regroupe touts les autres personnages dans OTHER
    my_df['Player'] = my_df['Player'].apply(lambda x: 'OTHER' if x not in nom else x)
    my_df = my_df.groupby(['Act', 'Player']).sum().reset_index()
    my_df['PercentCount'] = my_df['PlayerLine'] / my_df.groupby('Act')['PlayerLine'].transform('sum') * 100
    my_df=my_df.rename(columns={'PlayerLine':'LineCount','PercentCount':'LinePercent'})

    return my_df


def clean_names(my_df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # TODO : Clean the player names
    # On utilise title pour clean
    my_df['Player']=my_df['Player'].str.title()
    return my_df