# Foodtrack

Foodtrack is a simple tool to track the food you eat and how it influences
your body. Its aim is to help in analysis against which kind of food you
might have an intolerance.

In its first state, I will only define the data format. Later I will add some
simple scripts to aid in analysis.

## Data Format

Foodtrack is based on eating lists and symptoms. Everything you eat and
all symptoms get labeled with a timestamp. There are three main folders:

- `meals`: Contains one file per meal, each file uses a timestamp as
  filename
- `templates`: Contains one file per dish that consists of multiple
  ingredients
- `symptoms`: Contains symptons in files, filenames are timestamps when the
  symptom first occured

You can use foodtrack with only `meals` and `symptoms`, `templates` are
optional.

Meals are simply a list of its ingredients. If you want to clarify that you
ate one meal consisting of many ingredients, you can use dashes. These are
not required, however. The following is an example of a meal with coffee
and cake consumed on February 5th at 16:13:

```
# filename: 20210205-1613
coffee
milk
sugar
cherrycake
- wheatflour
- butter
- milk
- sugar
- egg
- cherry
```

There currently is no way to define amounts of ingredients.

Now let's imagine you bake this cake quite often and don't want to re-type
the ingredients all the time. In this case you can create a template called
`cherrycake` in the folder `templates`:


```
wheatflour
butter
milk
sugar
egg
cherry
```

Whenever you list `cherrycake` in your food lists then, it will be
automatically augmented with the ingredients.

If you then feel unwell with digestive problems on 5th February at 19:00
you could add a file called `20210205-1900` with the following contents:

```
digestion
```

### Extensions

It's possible to specify how strong the symptoms are with a suffix to the
symptom name in the symptom file, either `low` or `high`. E.g. if your
digestion problems are only mild, you could add:

```
digestion low
```

This has the effect that it will give a slightly less negative rating to food
you consumed in advance to the symptons, while a rating of `high` would give
a very bad rating to the food consumed.

Sometimes it can also happen that the kind of preparation of food might have
an influence. For example (to my knowledge) when you cook wine, most (or all?)
of its alcohol vanishes. Also canned fruits are different from raw fruits.
For such situations, you can add the sub type into brackets. E.g. for
canned plums you could write:

```
plum[canned]
```

This will allow the system to both consider the plums as plums, but also as
canned plums - which might influence your body differently.
