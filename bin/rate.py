#!/usr/bin/env python3

import datetime
import collections
import glob
from pathlib import Path
import sys
from typing import List, Tuple


def read_ingredients(
        file: Path, template_folder: Path, date: datetime.datetime = None) \
        -> Tuple[datetime.datetime, List[str]]:
    ingredients = []

    if not date:
        date = datetime.datetime.strptime(file.name, '%Y%m%d-%H%M%S')

    with open(file) as f:
        for line in f:
            ingredient = line.strip('-').strip()

            if (template_folder / ingredient).is_file():
                ingredients_sub = read_ingredients(
                    template_folder / ingredient, template_folder, date=date)
                ingredients += ingredients_sub[1]
            else:
                ingredients.append(line.strip('-').strip())

    return date, ingredients


def read_symptoms(file: Path):
    rates = {
        'low': 1,
        'medium': 2,
        'high': 3,
    }
    symptoms = []

    with open(file) as f:
        for line in f:
            symptom_level = line.strip()
            if ' ' in symptom_level:
                symptom, level = symptom_level.split(' ')
            else:
                symptom = symptom_level
                level = 'medium'

            symptoms.append((symptom, rates[level]))

    return datetime.datetime.strptime(file.name, '%Y%m%d-%H%M%S'), symptoms


def has_relevant_date(date, dates_list):
    for date_compare in dates_list:
        if date < date_compare and date + datetime.timedelta(days=2) > date_compare:
            return True

    return False


if __name__ == '__main__':
    # ugly, but does the job

    folder = sys.argv[1]

    food_dates = {}
    food_counts = collections.Counter()
    for mealfile in glob.glob(f'{folder}/meals/*'):
        date, ingredients = read_ingredients(Path(mealfile), Path(folder) / 'templates')
        food_dates[date] = ingredients
        food_counts.update(ingredients)

    symptoms_dates = collections.defaultdict(list)
    for symptomfile in glob.glob(f'{folder}/symptoms/*'):
        date, symptoms = read_symptoms(Path(symptomfile))
        for symptom, level in symptoms:
            symptoms_dates[symptom].append((date, level))

    food_ratings_no_effect = collections.defaultdict(int)
    for date, ingredients in food_dates.items():
        flat_symptom_dates = [date for sublist in symptoms_dates.values() for (date, _) in sublist]
        if not has_relevant_date(date, flat_symptom_dates):
            for ingredient in ingredients:
                food_ratings_no_effect[ingredient] += 2

    for symptom, dates_levels in symptoms_dates.items():
        print(f'== {symptom} ==')
        food_ratings = collections.defaultdict(int)
        food_rating_weighted = []

        for symptom_date, symptom_level in dates_levels:
            # TODO: Would be much better with a search tree, but this also works
            # for now
            for food_date, ingredients in food_dates.items():
                if symptom_date > food_date and symptom_date < food_date + datetime.timedelta(days=2):
                    for ingredient in ingredients:
                        food_ratings[ingredient] += symptom_level

        for food in food_counts.keys():
            rating_weighted = (-food_ratings[food] + food_ratings_no_effect[food]) / food_counts[food]
            food_rating_weighted.append((rating_weighted, food))

        food_rating_weighted = sorted(food_rating_weighted)

        for weighted_rating, food in food_rating_weighted:
            if food_counts[food] > 10:
                print(f'{food}: -{food_ratings[food]}/+{food_ratings_no_effect[food]}/t{food_counts[food]} {round(weighted_rating, 2)}')
