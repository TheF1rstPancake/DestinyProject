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

Bungie's Definition of Combat Rating
-------------------------------------
When I originally set out to do this post, I thought I was going to be defining what Combat Rating is, but Bungie actually has public defined Combat Rating as: 

  "An assessment of your skill and teamwork.  It factors in your score compared to others in each match and penalizes you for quitting."

That gives us something more to work with.  
Looking at the last table in light of this definition, you see that a lot of those coefficients don't make sense.
For example, *completed* has a positive coefficient.
The model we currently have adds 22 times *completed* to the equation.  
This means that player's are *rewarded* for completing a match because a 1 means the player successfully completed the match.
However, Bungie's definition clearly says that players are *penalized* for not completing a match.  
So, what we need to do is actually flip the representation of *completed* around so that 1 is quit, and 0 is completed.
This causes the trending algorithm to give *completed* a negative coefficient.

This creates a way for us to describe the different variables:
  - **reward variables**:   variables that have a *positive* cofficient.  The *greater* the value, the *higher* your combat rating should be.
  - **penalty variables**:  variables that have a *negative* coefficient.  The *greater* the value, the *lower* your combat rating should be.

We have to define all of our variables in light of this framework, especially variables that are boolean or discrete in nature.

The variables that are most affected by this are:
  - **standing**: 0 is victory, 1 is loss, but I think it makes more sense to reward people for winning than penalizing them for losing.  So standing is flipped before the trending algorithm runs.
  - **place**:  this variable ranks you against everyone else in the match.  1 means you were the highest scoring player, and it continuous to decrease.  But, this creates a *penalty* variable where lower ranked players are penalized more for doing worse.  To recity this I created a new variable named *rank* which is: 1.0-(place/number_of_players_in_game).  This creates a value between 0 and 1.  The closer you are to 1, the greater your score was relative to everyone else.

After applying these changes, the accuracy of the prediciton did not change, and the coefficients made no more sense than they had initially.
I felt like I had hit a pretty serious road block at this point because not only did the model create an equation that made no sense with amazing accuracy, it also didn't stay true to Bungie's definition of combat rating.  
I decided to step away from doing actual predicitons to instead look at what the *goal* of Combat Rating is.
And in order to do that, I took a trip down memory lane and went back to TrueSkill.

Microsoft's TrueSkill
----------------------
TrueSkill is Microsoft's algorithm for ranking player's in online matchmaking.

There are a lot of good resources for understanding TrueSkill:
  - http://trueskill.org/ :   a Python implementation of the TrueSkill ranking system
  - `TrueSkill(TM): A Bayesian Skill Rating System <http://research.microsoft.com/apps/pubs/default.aspx?id=67956>`_: Microsoft's published account of how TrueSkill works.
  - `TrueSkill(TM) Homepage <http://research.microsoft.com/en-us/projects/trueskill/default.aspx>`_: The TrueSKill homepage with links to all of Microsoft's TrueSkill publications along with detailed explanations for how TrueSkill works.
  - `Computing Your Skill <http://www.moserware.com/2010/03/computing-your-skill.html>`_: a *very* well done explanation for the stats behind TrueSkill and the other ranking systems that it is based on.

Each of those links will take you on a long winded tangent about how TrueSkill and other ranking systems function.
But the essence of TrueSkill is that it predicts your chances of winning based on your TrueSkill level relative to everyone else,
then it modifies player's TrueSkill levels based on whether they beat the odds or not.
A player who is predicted to lose but wins will have a greater increase in their TrueSkill level than someone who is predicted to win and wins.
TrueSkill was also designed to lock players into a skill level quickly.
The Microsoft report uses numbers from Halo 2 to show that TrueSkill can lock in on a player's skill level in approximately *10 games* for 4 vs 4 gamemodes.
Note however, that a player is only evaluated based on whether they won or lost the game.

This fast convergence actually became a problem in Halo 3 where we saw the birth of the infamous *Second Accounters*.
These were players who felt like TrueSkill had unfairly locked them into a certain rank and that they could actually acheive higher.
So, they created entirely new accounts.  
These new accounts were set at an average level, and since these were usually players who had been playing for a while their actual skill level was much higher.
The trick to a second account was to have high ranked friends who would then go into matchmaking with you.  
TrueSkill would say that the new second accounter had a very low chance of success, and when they would win, their skill level would be jump drastically allowing them to reach the highest level possible (50) in a short amount of time.

TrueSkill's purpose is to rank players in order to preform better matchmaking.  
Matchmaking under TrueSkill is done by trying to find players that you are most likely to *tie* with.
That is, the odds for winning or losing are as close to 50% as possible.

This makes sense in a 1v1 context, but not so much sense in a team setting.  There are very few players in the low buckets and even fewer in the high buckets, so how do you let these player's find matches?  Ideally, you would only pair high level players with other high level players, but there may not be enough high level players to support that.  This would result in slow matchmaking for higher tier players and they would probably being playing with the same group of players over and over again.

The natural inclination is to say that teams are nothing more than the sum of their parts.
Team matchmaking is then about finding two groups where the *average* combat rating for each team is relatively close.

.. plot:: combatRatingDistTeamBased Team Based Combat Rating Distribution Curve
    :dir: ../pages/fullPlots/combatRating/

.. html::
  <table class="table table-bordered">
    <tr>
      <th>Variable</th>
      <th>Value</th>
    </tr>
    <tr>
      <td class="tg-031e">count</td>
      <td class="tg-031e">22543.000000</td>
    </tr>
    <tr>
      <td class="tg-031e">mean</td>
      <td class="tg-031e">95.371748</td>
    </tr>
    <tr>
      <td class="tg-031e">std</td>
      <td class="tg-031e">23.118979</td>
    </tr>
    <tr>
      <td class="tg-031e">min</td>
      <td class="tg-031e">6.531070</td>
    </tr>
    <tr>
      <td class="tg-031e">25%</td>
      <td class="tg-031e">80.609082</td>
    </tr>
    <tr>
      <td class="tg-031e">50%</td>
      <td class="tg-031e">95.655659</td>
    </tr>
    <tr>
      <td class="tg-031e">75%</td>
      <td class="tg-031e">110.429940</td>
    </tr>
    <tr>
      <td class="tg-031e">max</td>
      <td class="tg-031e">187.468461</td>
    </tr>
  </table>

This curve is **much** more normally distributed than the player based combat rating distribution curve.
What we see here is that the mean is almost right on the 50% mark which is a strong indication that the curve is normally distributed.  
70.23% of values lie within 1 standard deviation of the mean.  
With a perfectly normally distributed curve, that value should be 68%, so we are very close here.
The reason that finding a normally distributed curve is so important is that it is what TrueSkill had other skill ranking systems use, so it allows us to compare Combat Rating to these other skill ranking systems.  
It also strongly indicates to us Combat Rating is a part of the system that Bungie is using to rank players **and** to establish fair matchmaking.

Matchmaking
------------
The claim I made can further be backed up by looking at the *difference* in Combat Rating between teams.

.. plot:: combatRatingDiff Distribution of Difference in Combat Rating between Teams 
  :dir: ../pages/fullPlots/combatRating

It is important to understand that the Combat Rating for each team is the *average* of all the players on the team.
Also, the Combat Rating values I am using are caluclated *postgame*.  
It is not the difference going into the game, but the difference at the end of the game.

So what that graph really shows us is how well Bungie's matchmaking creates "fair" matches.
51% of matches end with the two teams being within 2 standard deviations of eachother.
That's not too bad.  What is bad is that means that 49% of matches are outside of 2 standard deviations.
In other words, 49% of matches are pretty definitive with one team clearly being the winner over the other.

.. plot:: scoreDiff Distribution of Difference in Score between Teams
  :dir: ../pages/fullPlots/combatRating

The other way to see this "fairness" in play is to look at the difference in score at the end of a match.
The shape of this curve is *very* similar to the difference in Combat Rating between teams.
The score graph gives us some more perspective.  
39% of games end with the two teams being within 4461 points from one another.
I would say that this reprents our fair group.  However, that means that 61% of games end with a point difference greter than 4461.
About 10% of games end with a team winning by over 11,000.

The point of this is to show that score and Combat Rating are closely related (as Bungie's definition stated).
It also shows us that the current matchmaking system is not necessarily ideal.  
There are *likely* many factors that go into determing what makes a "good" match.  
Such factors could be network connectivity, fireteam size, and combat rating.

Predictions Round 3
----------------------
I've spent a considerable amount of text here convincing you that Bungie's definition of Combat Rating lines up with it's implementation.
However, using score with all of the other variables completely throws off the prediciton. While we get a *very* good prediciton, the equation doesn't make any sense.
That's because, score is already a linear combination of the components that measure player performance. 
For example, assists are worth half that of kills, so player's are rewarded for assists, but are rewarded even more for kills.  

Makes sense.

When we remvoe score from the prediction and try to use all of the components that make up score we get an **R-Squared value of 0.883** and a **Variance score of 0.894**.
Not as high as when we included score, but it is still a strong score, and all of our coefficients make sense.

.. html::
  <table class="table table-bordered">
    <tr>
      <th class="tg-031e">Variable</th>
      <th class="tg-031e">Coefficient</th>
    </tr>
    <tr>
      <td class="tg-031e">completed</td>
      <td class="tg-031e">-21.966525</td>
    </tr>
    <tr>
      <td class="tg-031e">deaths</td>
      <td class="tg-031e">-1.383680</td>
    </tr>
    <tr>
      <td class="tg-031e">zonesNeutralized</td>
      <td class="tg-031e">-0.044273</td>
    </tr>
    <tr>
      <td class="tg-031e">averageScorePerLife</td>
      <td class="tg-031e">0.036985</td>
    </tr>
    <tr>
      <td class="tg-031e">averageScorePerKill</td>
      <td class="tg-031e">0.046020</td>
    </tr>
    <tr>
      <td class="tg-031e">longestKillSpree</td>
      <td class="tg-031e">0.199851</td>
    </tr>
    <tr>
      <td class="tg-031e">assists</td>
      <td class="tg-031e">0.427323</td>
    </tr>
    <tr>
      <td class="tg-031e">objectivesCompleted</td>
      <td class="tg-031e">0.490707</td>
    </tr>
    <tr>
      <td class="tg-031e">defensiveKills</td>
      <td class="tg-031e">1.046707</td>
    </tr>
    <tr>
      <td class="tg-031e">offensiveKills</td>
      <td class="tg-031e">1.208658</td>
    </tr>
    <tr>
      <td class="tg-031e">standing</td>
      <td class="tg-031e">1.766655</td>
    </tr>
    <tr>
      <td class="tg-031e">rank</td>
      <td class="tg-031e">2.719212</td>
    </tr>
    <tr>
      <td class="tg-031e">kills</td>
      <td class="tg-031e">5.012036</td>
    </tr>
    <tr>
      <td class="tg-031e">dominationKills</td>
      <td class="tg-031e">10.015568</td>
    </tr>
  </table>

I'm more or less satisified with this model.  
It makes sense, as a high level of accuracy, but it doesn't necessarily stick with the definition Bungie gave us.
This does not take score into account directly.
It instead makes use of most of the factors that create a player's score and it even takes into account some factors that don't.
Deaths is the biggest part of that.  Deaths are not taken into your score as a player, but this model penalizes player's for dying.
This is a logical thing to do, but no where in Bungie's definition does it say anything about taking into account player deaths.
It explicitly states that score is the determining factor.
This model also doesn't have a very good way of comparing different players in each game.
The rank variable does in some respects, but it doesn't take into account that in some games, everyone performs very well.

Predicitons Round 4
-----------------------
What we need is a better way to implement Bungie's actual definition and have it potentially break our R-Squared score of 0.92.

We know that score is a big component, and so is penalizing players for quitting.
The last part of this is to take into account the *relativity* aspect.
A player needs to be ranked according to how other players in the game performed.  Doing the ranking from 1 to *num_players* is one way to do that, but it assumes that the difference between the top player and the second place player is extremely significant.
While that can be the case, it is not always true. We should instead come up with a way to standardize score such that score is a reflection of how well that player did compared to other players in a given game.

This can be done with some simple math:
  >>> standard_score = (score - mean(score))/(max(score) - min(score))

This will generate a value between -1 and 1.  
Negative values are for players who performed below the mean, and positive values for those that performed above the mean.
Dividing that number by the range makes sure that everyone has a value  between -1 and 1.  

We can also use this value to view "fairness" in matchmaking.  
A fair match would be one where everyone is perfomring as close to the mean as possible.
It is improbable that all 12 players in a game receive the exact same score, but the fluctuations around the positive and negatives should be minimal.

Using the *standard_score* variable along with *completed* and *score* resulted in an R-Squared value of 0.8655 and a Variance score of 0.8809.  

There is a flaw in *standard_score* though.  It really doesn't handle close game situations very well.
If everyone is doing very well, then those who fall even slightly below average are still having points deducted from their combat rating.
It is not fair to do this to them.

What was really helpful for me at this point was to look at the extreme cases.
The highest combat rating in the dataset is 457.807919.  This came with an associated score of 9700.
The lowest combat rating in the dataset is 0.721582 with an associated score of 25.
These numbers mean nothing without some context of how everyone else in that game performed.

In the game with the highest combat rating, there were 4 players who quit and had a score of 0, earning them a combat rating on 0.  The second highest combat rating in that game is a 152.209334 with an associated score of 3225. 

In the game with the lowest combat rating there were no players that quit.  The highest combat rating in that game though is a 170.536264 with an associated score of 5900.

The reason I bring this up is because there appears to be a **direct** relationship between combat rating and score in a given game.  Look at the game with the top score again.  If we divide each score by the max score, and then divide each combat rating by the max combat rating we get the following table.

.. html::
  <table class="table table-bordered">
    <tr>
      <th class="tg-031e">score</th>
      <th class="tg-031e">combatRating</th>
      <th class="tg-031e">relativeScore</th>
      <th class="tg-031e">relativeCR</th>
    </tr>
    <tr>
      <td class="tg-031e">0</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
    </tr>
    <tr>
      <td class="tg-031e">0</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
    </tr>
    <tr>
      <td class="tg-031e">0</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
    </tr>
    <tr>
      <td class="tg-031e">0</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
    </tr>
    <tr>
      <td class="tg-031e">0</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
      <td class="tg-031e">0.000000</td>
    </tr>
    <tr>
      <td class="tg-031e">300</td>
      <td class="tg-031e">14.159008</td>
      <td class="tg-031e">0.030928</td>
      <td class="tg-031e">0.030928</td>
    </tr>
    <tr class="warning">
      <td class="tg-031e">160</td>
      <td class="tg-031e">18.979633</td>
      <td class="tg-031e">0.016495</td>
      <td class="tg-031e">0.041458</td>
    </tr>
    <tr>
      <td class="tg-031e">450</td>
      <td class="tg-031e">21.238512</td>
      <td class="tg-031e">0.046392</td>
      <td class="tg-031e">0.046392</td>
    </tr>
    <tr>
      <td class="tg-031e">525</td>
      <td class="tg-031e">24.778264</td>
      <td class="tg-031e">0.054124</td>
      <td class="tg-031e">0.054124</td>
    </tr>
    <tr>
      <td class="tg-031e">650</td>
      <td class="tg-031e">30.547859</td>
      <td class="tg-031e">0.067010</td>
      <td class="tg-031e">0.066726</td>
    </tr>
    <tr>
      <td class="tg-031e">660</td>
      <td class="tg-031e">31.149817</td>
      <td class="tg-031e">0.068041</td>
      <td class="tg-031e">0.068041</td>
    </tr>
    <tr class="warning">
      <td class="tg-031e">260</td>
      <td class="tg-031e">33.337779</td>
      <td class="tg-031e">0.026804</td>
      <td class="tg-031e">0.072820</td>
    </tr>
    <tr>
      <td class="tg-031e">1540</td>
      <td class="tg-031e">72.993517</td>
      <td class="tg-031e">0.158763</td>
      <td class="tg-031e">0.159441</td>
    </tr>
    <tr>
      <td class="tg-031e">2785</td>
      <td class="tg-031e">131.442789</td>
      <td class="tg-031e">0.287113</td>
      <td class="tg-031e">0.287113</td>
    </tr>
    <tr>
      <td class="tg-031e">2930</td>
      <td class="tg-031e">147.379967</td>
      <td class="tg-031e">0.302062</td>
      <td class="tg-031e">0.321925</td>
    </tr>
    <tr>
      <td class="tg-031e">3225</td>
      <td class="tg-031e">152.209334</td>
      <td class="tg-031e">0.332474</td>
      <td class="tg-031e">0.332474</td>
    </tr>
    <tr>
      <td class="tg-031e">9700</td>
      <td class="tg-031e">457.807919</td>
      <td class="tg-031e">1.000000</td>
      <td class="tg-031e">1.000000</td>
    </tr>
  </table>

There are only 2 rows for which this pattern does not apply (they are highlighted in the table).
These two rows appear to have higher than normal combat ratings based on their score.  So what makes these two players so special?

The real anomaly in this is why the 260 player was able to get a better combat rating than the other half of the players in the game.
His score is terrible, and his team lost.  So it's not like he got a boost from his team winning.
The only stat that I found that was higher was the *longestKillSpree* stat.  Sorting by combat rating doesn't give us a perfectly sorted longestKillSpree; however, this does give some indication that longestKillSpree still plays some sort of a roll.

The other thing that this shows us is that combat rating is done a game by game basis.  The top scorer of game 2 had a score of 5900 but a combat rating of 152.  The top scorer of game 1 had 9700 points but a combat rating of 457.8, but 5900/9700 does not equal 152/457.  And while this ratio is not always true, it seems to be true in a lot of cases.  So we need to find a way to make use of this ratio on a game by game basis.

We can calculate this ratio for each player in their game, but a value of .30 in one game might equate to a different combat rating than a value of .30 in another game.

The other problem is that this ratio is easy to calculate since we know the combat rating, but we are trying to predict combat rating, so we can't use combat rating in our predicitons.

One thing we can do to test this hypothesis is to calculate the ratios and use combat rating in our predictions, and then do a RMSE and R-squared test to see how accuarte we were.

In order to do this cacluation we simply run:
  >>> ratioPrediciton = (score/max(score))*max(combatRating)

But we do this for each game.

Doing this gives us a R-Squared value of 0.886743 and a variance score of 0.898677.  Using only 1 variable.
Again, this uses combat rating in the prediciton so it's cheating, but it does show that this score ratio has some validity for almost 90% of cases.

Another interesting case is one game in the dataset where the highest combat rating belonged to a player who had a score of 360.  This player earned a score of 368.0221 for their efforts.  This again shows that there is something about the relativity of score that plays a part in the calculation of combat rating.

It has been hard to find out exactly what the magic behind combat rating is.
But another place to look is why two players with a very similar *combat rating* might have very different scores.
I took all of the max scores in the each game and looked at their associated combat ratings.
I found several games where two players had very similar combat ratings, but their scores were drastically different.

