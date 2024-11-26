import matplotlib.pyplot as plt
import config
import numpy as np
import pandas as pd
import seaborn as sns

from utils.dataframe_utils import drop_unknown, drop_indexes


def get_visualization(filepath):
    """
    Fetch a visualization file.
    """
    with open(filepath, 'reports/charts') as f:
        return f.read()


def plot_stacked_bar_chart(expenditure_df):
    """
    Plots a stacked bar chart representing Statewise Average Expenditure by item category

    Parameters
    ----------
    expenditure_df : Dataframe
        The expenditure data to be plotted
    """

    # Calculate plot values
    statewise_avg_exp_by_category = expenditure_df.groupby(['State', 'Item_Group_Srl_No'])[
        'Value_of_Consumption_Last_30_Day'].mean().reset_index()
    pivot_df = statewise_avg_exp_by_category.pivot(
        index="State", columns="Item_Group_Srl_No", values="Value_of_Consumption_Last_30_Day").fillna(0)
    states = pivot_df.index
    categories = pivot_df.columns
    values = [pivot_df[cat] for cat in categories]

    # Plot the chart
    fig, ax = plt.subplots(figsize=(12, 7))

    ax.bar(states, values[0], label=categories[0], width=0.4)
    for i in range(1, len(categories)):
        ax.bar(states, values[i], bottom=np.sum(
            values[:i], axis=0), label=categories[i], width=0.4)

    # Add titles and labels
    ax.set_title(
        "Average Monthly Expenditure by State and Item Group", fontsize=16)
    ax.set_xlabel("States", fontsize=12)
    ax.set_ylabel("Value of Consumption (Last 30 Days)", fontsize=12)
    ax.legend(title="Item Groups", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Layout adjustment
    plt.tight_layout()
    plt.savefig(config.CHARTS_DIR+'/statewise-expenditure-stacked-bar.png')
    plt.close(fig)


def plot_grouped_bar_chart(demographic_df):
    """
    Plots a grouped bar chart representing Genderwise Education Level

    Parameters
    ----------
    demographic_df : Dataframe
        The demographic data to be plotted
    """
    # Calculate plot values
    sex_education_df = demographic_df[['Sex', 'General_Education']].copy()
    sex_education_df = pd.crosstab(
        sex_education_df.General_Education, sex_education_df.Sex).reset_index()

    # Plot the chart
    fig, ax = plt.subplots(figsize=(6, 5))
    sex_education_df.plot(x='General_Education', kind='barh', stacked=False,
                          title='Gender and Education Level', ax=ax, colormap='icefire')

    # Add title and labels
    ax.legend(title="Genders", bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.set_xlabel("No of Individuals", fontsize=12)
    ax.set_ylabel("Education Level", fontsize=12)
    plt.savefig(config.CHARTS_DIR +
                '/genderwise-educationlevel-grouped-bar.png', bbox_inches='tight')
    plt.close(fig)


def plot_pie_charts(demographic_df):
    """
    Plots pie charts representing Statewise MGNREG data

    Parameters
    ----------
    demographic_df : Dataframe
        The demographic data to be plotted
    """

    # Calculate plot values for MGNREG_jobcard
    state_mgnreg_jobcard_df = demographic_df[[
        'State', 'MGNREG_jobcard']].copy()
    state_mgnreg_jobcard_df = drop_unknown(state_mgnreg_jobcard_df)
    state_mgnreg_jobcard_df = pd.crosstab(
        state_mgnreg_jobcard_df.State, state_mgnreg_jobcard_df.MGNREG_jobcard).reset_index()

    # Plot separate pie charts for each state
    for ind in range(len(state_mgnreg_jobcard_df)):

        # Calculate plot values
        state = state_mgnreg_jobcard_df.loc[ind].values[0]
        mgnreg_jobcard_data = state_mgnreg_jobcard_df.loc[ind].values[1:]
        chart_labels = state_mgnreg_jobcard_df.columns[1:]

        # Plot pie chart
        wp = {'linewidth': 2, 'edgecolor': 'white'}
        plt.figure(figsize=(3, 3))
        plt.pie(mgnreg_jobcard_data, autopct='%1.0f%%', labels=chart_labels,
                wedgeprops=wp, colors=sns.color_palette('viridis'))

        # Set title and layout
        plt.title('Registered in MGNREG Jobcard - '+state, wrap=True)
        plt.tight_layout()
        plt.savefig(config.CHARTS_DIR+'/MGNREG-registered-'+state+'-pie.png')
        plt.close()

    # Calculate plot values for MGNREG_worked
    statewise_mgnreg_worked = demographic_df[['State', 'MGNREG_work']].copy()
    statewise_mgnreg_worked = drop_unknown(statewise_mgnreg_worked)
    statewise_mgnreg_worked = pd.crosstab(
        statewise_mgnreg_worked.State, statewise_mgnreg_worked.MGNREG_work).reset_index()

    # Plot separate pie charts for each state
    for ind in range(len(statewise_mgnreg_worked)):

        # Calculate plot values
        state = statewise_mgnreg_worked.loc[ind].values[0]
        mgnreg_worked_data = statewise_mgnreg_worked.loc[ind].values[1:]
        chart_labels = statewise_mgnreg_worked.columns[1:]

        # Plot pie chart
        wp = {'linewidth': 2, 'edgecolor': 'white'}
        plt.figure(figsize=(3, 3))
        plt.pie(mgnreg_worked_data, autopct='%1.0f%%', wedgeprops=wp,
                colors=sns.color_palette('viridis'))

        # Set title and layout
        plt.title('Found Work Through MGNREG - '+state, wrap=True)
        plt.legend(loc='lower center', labels=chart_labels,
                   bbox_to_anchor=(0.5, -0.2))
        plt.tight_layout(pad=0.1)
        plt.savefig(config.CHARTS_DIR+'/MGNREG-worked-'+state+'-pie.png')
        plt.close()


def plot_stacked_histogram(demographic_df):
    """
    Plots stacked histogram representing age distribution and education level.

    Parameters
    ----------
    demographic_df : Dataframe
        The demographic data to be plotted
    """

    # Calculate plot data
    age_education_df = demographic_df[['Age', 'General_Education']].copy()
    bins = range(0, 100, 10)
    age_education_df['Age_Bin'] = pd.cut(
        age_education_df['Age'], bins=bins, right=False)
    grouped = age_education_df.groupby(
        ['Age_Bin', 'General_Education'], observed=False).size().unstack(fill_value=0)
    grouped = grouped[['Not literate', 'Literate without formal schooling:  EGS/ NFEC/ AEC',
                       'Literate:  below primary', 'Literate:  primary', 'Literate:  middle',
                       'Literate:  secondary', 'Literate:  higher secondary', 'Literate:  graduate',
                       'Literate:  diploma/certificate course']]

    # Plot the chart
    grouped.plot(kind='bar', stacked=True,
                 colormap='viridis',    figsize=(10, 6))

    # Customize plot
    plt.title('Age Distribution by Literacy Level', fontsize=14)
    plt.xlabel('Age Range', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Literacy Level')
    plt.tight_layout()
    plt.savefig(config.CHARTS_DIR+'/age-educationlevel-stacked-histogram.png')
    plt.close()


def plot_heatmap(expenditure_df):
    """
    Plots a heatmap representing statewise expenditure per item category.

    Parameters
    ----------
    demographic_df : Dataframe
        The demographic data to be plotted
    """

    # Process the data to be plotted
    state_category_exp_df = expenditure_df[[
        'State', 'Item_Group_Srl_No', 'Value_of_Consumption_Last_30_Day']]
    state_category_exp_df = pd.crosstab(state_category_exp_df.Item_Group_Srl_No, state_category_exp_df.State,
                                        values=state_category_exp_df.Value_of_Consumption_Last_30_Day,
                                        aggfunc=np.average).round(2)
    state_category_exp_df = drop_indexes(
        state_category_exp_df, ['monthly', 'Monthly', 'Sub-total']).reset_index()
    state_category_exp_df.set_index('Item_Group_Srl_No', inplace=True)
    state_category_exp_df.fillna(0, inplace=True)

    # Create the heatmap
    plt.figure(figsize=(10, 15))
    sns.heatmap(state_category_exp_df, annot=True,
                fmt=".2f", cmap="YlGnBu", linewidths=0.5)

    # Add labels and title
    plt.title('Average Expenditure by State and Category', fontsize=16)
    plt.xlabel('State', fontsize=12)
    plt.ylabel('Category', fontsize=12)
    plt.tight_layout()
    plt.savefig(config.CHARTS_DIR+'/statewise-expenditure-heatmap.png')
    plt.close()
