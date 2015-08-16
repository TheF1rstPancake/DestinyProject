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

.. plot:: combatRatingDist Combat Rating Distribution Curve
    :dir: ../pages/fullPlots/combatRating/

As we can see fom that graph, the distribution of combat ratings looks pretty normally distributed, which is what we would expect from a metric like this.
Bungie needs a way to compare player skill level.  
The entire basis of a fair and balanced matchmaking system rests on the idea that there is a way to create teams such that each team has an equal chance at success.
By creating a metric that falls in line with the normal distribution, we can clearly see who the bad, the average and the good players are.
But these titles of "bad", "average" and "good" are all subjective.

What this analysis is going to try and do is **examine how Bungie determines player skill**.

-1s and 0s
------------
I did remove all players who had a combat rating of -1 or 0 when making that distribution graph.  This removes 4.4% of the total population but still leaves us with over 100,000 entries. These anomlous cases are interesting because they can tell us a few things about Combat Rating.

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

However, I ended up throwing out the all players with a combat rating less than *or equal to* 0.
The reason is that we know already know what causes them to be 0.
I don't want this group of players artificially decreasing or inflating the prediciton scores.

Moving forward, when I refer to *the dataset* I am talking about **all players in my dataset who had a combat rating greater than 0.**

First Predictions
-------------------
In order to do the first prediction, I tried to minimize the number of columns that I was looking at.
I narrowed it down to only columns with numerical data and tried to avoid columns that were subsets of other columns.
For example, I have a series of columns that are titled *weaponKills[WeaponType]* where *[WeaponType]* is something like *PulseRifle* or *Sniper*.
After all this, there were still 23 columns that I could use.

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

What I finally ended up with was a **variance score of 0.8668675** and a **r-sqaured score of 0.8459838**.
For both of those scores, a value of 1 indicates a perfect match.  

So, my first test using only 3 predictors had an accuracy of 85% with the following coeffecients
    - *kills*: -0.929154918057
    - *longestKillSpree*: 3.40214824993
    - *score*: 0.0311323984706

Giving us the grand equation:
    
    .. code-block:: python
        
        combat_rating = (-0.929154918057 * kills) + (3.40214824993 * longestKillSpree) + (0.0311323984706 * score)

It's interesting to note that *kills* has a negative coefficient.  That means that the more kills someone has, the *lower* their combat rating.
Logically, it makes very little sense.  Why punish people who have a higher number of kills?
1 kill is almost 1 less combat rating point.  But since (on average) players get **12 kills** in a given match, that means that this isn't dropping their combat rating by a lot.  

This decrease is also made up by the *longestKillSpree* variable.  The average player has a *longestKillSpree* value of 3.7.
Let's knock it down to 3 since you can't have .7 of a kill.  Let's plug the average player into this equation and see what we get.

.. code-block:: python
   
    combat_rating = (-0.929154918057 * 12) + (3.40214824993*3) + (0.0311323984706*score)
    combat_rating = -0.9434142668940009 + (0.0311323984706*score)

So the average player really only sees a knock down of less than a point to their combat rating under this model.
If we think about this setup a little bit more, it actually makes a lot of sense.
A player who runs around and gets a ton of kills but only gets 1 kill per life is maybe not as "good" as a player who has a lower number of kills, but never dies.

Let's take two test cases.  The standard deviation on *kills* is about 7, so let's go one standard deviation in either direction.

.. code-block:: python
   
    high_kills_cr = (-0.929154918057 * 19 ) + (3.40214824993 * 1) + (0.0311323984706 * score)
    high_kills_cr = -14.251795193153 + (0.0311323984706 * score)
    low_kills_cr = (-0.929154918057 * 5 ) + (3.40214824993 * 5) + (0.0311323984706 * score)
    low_kills_cr = 12.364966659364999 + (0.0311323984706 * score)

This extreme case helps illustrate the point that combat rating seems to favor you're ability to get a spree going.
The player who runs around and gets a lot of kills, but can't stay alive for more than 1 kill is going to be penalized.  But this does not mean that the player with the 5 kill streak *did not die*.  They could have died 15 times, but had one good streak.

But the real dominating factor is your score.  Score get's hit with a tiny coefficient, but score has the fastest growth.
Kills and longestKillSpree only increase in increments of 1, whereas score is increasing in a variety of increments, all of which are greater than 25.
Our cautious player with only 5 kills, but a 5 kill-streak, is not going to have as many points as our blood-lusting player with 19 kills with a longestKillSpree of 1.

So let's calculate this all the way to the end using some real player data.  I hand-picked these two players to compare.

.. code-block:: python
   
    high_kills_cr = (-0.929154918057 * 20) + (3.40214824993 * 2) + (0.0311323984706 * 4140)
    high_kills_cr =  117.109327807004
    low_kills_cr = (-0.929154918057 * 7) + (3.40214824993 * 5) + (0.0311323984706 * 1455)
    low_kills_cr =  55.804296597973995

So while the *low_kills* player may have had a greater boost from their longestKillSpree, their combat rating is still significantly lower because they do not have as high of a score.

In general, what this means is that score is the predominate factor in deciding your combat rating, but what differentiates players who a near equal score is the combination of their kills and their longestKillSpree.

Predictions Round 2
-------------------------
Noticeably absent from this conversation is any mention of objectives.
The first round of predictions used only 3 variables all of which were related to a player's ability to kill oponents.
Score takes into account everything you do though, which is part of the reason why it's probably one of the best predictors.

For the second round of predictions, I used *all* 24 columns.
It gave me a **R-Squared value of 0.9272879** and a **Variance score of 0.9322257**.
Below is a table of the coeffeicients for each variable.

.. html::
    <table class="table table-bordered">
      <tr>
        <th class="tg-031e">variable</th>
        <th class="tg-031e">coeffecient</th>
      </tr>
      <tr>
        <td class="tg-031e">assists</td>
        <td class="tg-031e">-0.927857209</td>
      </tr>
      <tr>
        <td class="tg-031e">averageLifespan</td>
        <td class="tg-031e">-0.500777443</td>
      </tr>
      <tr>
        <td class="tg-031e">averageScorePerKill</td>
        <td class="tg-031e">0.008664059</td>
      </tr>
      <tr>
        <td class="tg-031e">averageScorePerLife</td>
        <td class="tg-031e">0.070264954</td>
      </tr>
      <tr>
        <td class="tg-031e">completed</td>
        <td class="tg-031e">23.25449517</td>
      </tr>
      <tr>
        <td class="tg-031e">deaths</td>
        <td class="tg-031e">-1.825502308</td>
      </tr>
      <tr>
        <td class="tg-031e">defensiveKills</td>
        <td class="tg-031e">-0.59322549</td>
      </tr>
      <tr>
        <td class="tg-031e">kills</td>
        <td class="tg-031e">-0.610896445</td>
      </tr>
      <tr>
        <td class="tg-031e">killsDeathsAssists</td>
        <td class="tg-031e">3.782712579</td>
      </tr>
      <tr>
        <td class="tg-031e">killsDeathsRatio</td>
        <td class="tg-031e">-2.160936885</td>
      </tr>
      <tr>
        <td class="tg-031e">longestKillSpree</td>
        <td class="tg-031e">-0.278656088</td>
      </tr>
      <tr>
        <td class="tg-031e">objectivesCompleted</td>
        <td class="tg-031e">-1.29637071</td>
      </tr>
      <tr>
        <td class="tg-031e">offensiveKills</td>
        <td class="tg-031e">0.468470248</td>
      </tr>
      <tr>
        <td class="tg-031e">orbsDropped</td>
        <td class="tg-031e">-0.159636889</td>
      </tr>
      <tr>
        <td class="tg-031e">orbsGathered</td>
        <td class="tg-031e">0.011888818</td>
      </tr>
      <tr>
        <td class="tg-031e">playerCount</td>
        <td class="tg-031e">1.239542562</td>
      </tr>
      <tr>
        <td class="tg-031e">precisionKills</td>
        <td class="tg-031e">-0.184764911</td>
      </tr>
      <tr>
        <td class="tg-031e">score</td>
        <td class="tg-031e">0.029872563</td>
      </tr>
      <tr>
        <td class="tg-031e">standing</td>
        <td class="tg-031e">-0.048855635</td>
      </tr>
      <tr>
        <td class="tg-031e">teamScore</td>
        <td class="tg-031e">-0.000288886</td>
      </tr>
      <tr>
        <td class="tg-031e">zonesNeutralized</td>
        <td class="tg-031e">-0.059174631</td>
      </tr>
      <tr>
        <td class="tg-031e">dominationKills</td>
        <td class="tg-031e">1.649904316</td>
      </tr>
      <tr>
        <td class="tg-031e">place</td>
        <td class="tg-031e">-0.107990814</td>
      </tr>
    </table>

A few notes about this:
    1) *standing* is 0 if the player **won** the game, 1 if they lost it.  That's why standing has a negative coefficient.  Player's are penalized for losing.
    2) *place* is a value that I calculated.  It is the player's place on the leaderboard at the end of the game.  1 is for the best player, and continues increasing from there.  It is essentially another way of looking at score.  But it has a negative coefficient because as a player falls down the leaderboard, they lose combat rating.

But some of these values make **no sense** whatsoever.  Why would player's be penalized for getting precisionKills?  If you look carefully, you will also see that *longestKillSpree* now has a negative coefficient so player's are being penalized for having large sprees.  And why are all of the objective related coefficients negative? While this gave us a high accuracy, the equation itself makes no (intuitive) logical sense which then makes it difficult to further analyze.

So what I did is I started back at the top 3 and added features in one at a time to see how it changed the relationship between all the variables.
This process took *five-ever*.  I

Another thing to consider is how *standing* and *completed* are represented.  With *standing* a 1 is a loss; 0 a win.  With *completed* it's the other way around - 1 is completed; 0 is quit.
When doing a linear regression though each variable is given   



If kills and score are 0 you get -1.  The only reason you would try and catch that here is if the it would produce some form of NaN value.
In other words, if it would break your system.  If kills and score are both 0, averageScorePerKill will be 0/0 = NaN. Whereas if score is just 0, then you get 0/#ofkills which is 0.  This is also just a random fluke that cause the system to record your score as zero even though you really should have registered some points.