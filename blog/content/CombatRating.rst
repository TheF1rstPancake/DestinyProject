Breaking Combat Rating
===============================================
:date: 2015-08-05
:modified: 2015-08-05
:tags: Crucible, combat rating
:authors: Giovanni Briggs
:summary: Examining how combat rating is calculated and how to exploit it.
:category: Stat Porn Sunday
:status: draft

What is Combat Rating
----------------------
Before we dive into the details, we need to establish what Combat Rating is and what it's purpose is.
Combat Rating is a metric that Bungie tags to each player.
In this context, combat ratings are given out at the end of each *game*.
This analysis is not trying to predict your combat rating over life.  It is a game by game prediction.
However, assuming the Bungie does aggregate combat rating in some form over time, then our overall combat rating is a direct result of our game by game combat ratings.

Let's look at the distribution of combat rating in order to better understand it's function.
For those of you who have been following Stat Porn Sundays in the past, this plot will look familiar.

.. html::
    <div class="plotContainer">
    <h4 class="text-center">Combat Rating Distribution Curve</h4>
    <div id="combatRatingDist">
        <svg></svg>
        <script src='../fullPlots/IronBanner/javascripts/combatRatingDist.js'></script>
    </div>
    </div>

As we can see fom that graph, the distribution of combat ratings looks pretty normally distributed, which is what we would expect from a metric like this.
Bungie needs a way to compare player skill level.  
The entire basis of a fair and balanced matchmaking system rests on the idea that there is a way to create teams such that each team has an equal chance at success.
By creating a metric that falls in line with the normal distribution, we can clearly see who the bad, the average and the good players are.
But these titles of "bad", "average" and "good" are all subjective.

What this analysis is going to try and do is **examine how Bungie determines player skill**.

-1s and 0s
------------
I did remove all players who had a combat rating of -1 or 0 when making that distribution graph.  This removes 4.4% of the total population but still leaves us with over 100,000 entries.These anomlous cases are interesting because they can tell us a few things about Combat Rating.

First, take the instances where combat rating is 0.  
I took this subset of data and then went and tried to find the columns that had a constant value.
I found 3 columns in which this was the case: *score*, *averageScorePerLife*, and *averageScorePerKill*.
Basically, if your score is 0, you're combat rating is 0 which is not suprising.  A score of 0 means the player didn't do anything during the game.

But that's where this gets interesting.  
Of all of the players who had a combat rating of 0, *4%* of them had at least 1 kill, *2.5%* had at least 1 assist, and *3.4%* of them had at least one zone capture.
All of these actions should have resulted in the player being awarded points and having some form of score.
However, it didn't and as a result they received a combat rating of 0.

This gives us two possibilities.  Option 1 is that combat rating is a *multiple* of score.  In other words, the equation looks like:
    
.. code-block:: python
    
    combat_rating = score * other_calculated_values

Where *other_calculated_values* is the output of some other function that takes into account game information to give you a score.
This would satisfy the condition that all players who receive a combat rating of 0 also have a score of 0.

The other possibility is that Combat Rating is actually not a strict mathematical equation but rather a block of code of the form:

.. code-block:: python
    
    if score == 0:
        return 0
    #{other logic preprocessing}#
    else:
        #do math
        return combatRating

It would make sense that Bungie does some pre-processing of the data before trying to calculate scores.
Since data can be lost and/or corrupted for a number of reasons, they would want to check the data before they process it or else face the wrath of angry computer messages telling you that you are a stupid and worthless human.
However, we have no way of knowing which one it is.  The pressence of other constant values would help to support the preprocessing theory.
Those constants stand in as flags and the preprocessing code-block checks for those flags and then makes a desicion, but the score variables are the only constants in this subset.

Fortunately, looking at the -1 case helps us out a bit.  These are a very, very smaller number of cases (76 total) but 19 columns had a constant value.

Many of these columns are infered off of others, so it really boils down to:
    - kills
    - deaths
    - assists
    - objectivesCompleted
    - zonesNeutralized
    - score
    - standing

Some interesting factoids here are that the standing value marks whether the player won or loss, with a 0 being a win and a 1 being a loss.
All of these players were marked with a 0 for standing.  In other words all were attributed with a win, but were still given a combat rating of 0.
Noticeably missing from this list is *completed* which marks whether or not a player completed the match (0 being yes, 1 being no).
So quitting does not give you a combat rating of -1 nor does it gaurantee you a combat rating of 0.

This leads me to believe that combat rating is being calculated in some sort of logic block.  Something goes awry, and Bungie's system picks up on it and gives all of these players a -1 value.  So the block looks something like this:

.. code-block:: python
    
    if score == 0 and kills == 0:
        return -1
    #{other preprocessing}#
    else:
        #do math
        return combatRating

Moving forward, when I refer to *the dataset* I am talking about all players in my dataset who had a combat rating of 0 or greater.
I leave the 0s in here because I cannot definitively tell if it is the result of a logic-block or if combat rating is a direct multiple of score.
However, I am certain that scores of -1 are a result of a pre-processing of the data.

First Predictions
-------------------
In order to do the first prediction, I tried to minimize the number of columns that I was looking at.
I narrowed it down to only columns with numerical data and tried to avoid columns that were subsets of other columns.
For example, I have a series of columns that are titled *weaponKills[WeaponType]* where *[WeaponType]* is something like *PulseRifle* or *Sniper*.
After all this, there were still 24 columns that I could use.

In order to predict combat rating, I am using a lot of modules from `scikit <http://scikit-learn.org/>`_.

Scikit comes with a bunch of modules designed to do regression and pre-processsing of data.
I used `SelectPercentile <http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.SelectPercentile.html>`_ with a `univariate linear regression test <http://scikit-learn.org/stable/modules/generated/sklearn.feature_selection.f_regression.html#sklearn.feature_selection.f_regression>`_ to try and find which columns make for the best predictors.

I started with only the predictors that scored in the top 10% (i.e. the top 3 predictors) which were:
    - score
    - kills
    - longestKillSpree

I then ran a `ridge regression <http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html>`_ to predict combat rating.
I sliced the dataset in 10 different ways, each time using 80% of the dataset for training, and 20% for testing and ran the ridge regression across each training/test pair.
Finally, I calculated several different scoring metrics and took the average of these across all of the runs.

What I finally ended up with was a **variance score of 0.8862443** and a **r-sqaured score of 0.8715312**.
For both of those scores, a value of 1 indicates a perfect match.  So, my first test using only 3 predictors had an accuracy of 88%.


