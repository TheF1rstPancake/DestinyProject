I am the Prettiest Guardian There Ever Was
===============================================
:date: 2015-07-26
:modified: 2015-07-26
:tags: Shaders, Character
:authors: Giovanni Briggs
:summary: Examining shader usage.
:category: Stat Porn Sunday

See the `original post on reddit <https://www.reddit.com/r/DestinyTheGame/comments/3eol7l/stat_porn_sunday_i_am_the_prettiest_guardian/>`_

Welcome
-----------
Welcome to Stat Porn Sunday where I make colorful graphs with fun facts that you can use to impress other Guardians.
Here's the obligatory link to last week's `Stat Porn Sunday: Don't hate the game; hate the player <https://www.reddit.com/r/DestinyTheGame/comments/3dur9n/stat_porn_sunday_dont_hate_the_game_hate_the/>`_.

For those of you were involved in last week's post, I haven't forgotten about you. 
I've been re-examining the data and working all sorts of black magic to find new ways to re-engage the conversation. 
There may even be a midweek post (foreshadowing!).


Beautifying My Guardian
-------------------------
I'm on vacation this week so this stat is going to be pretty basic. 
I created a dataset full of 300,000 different characters. A
ll of the data was collected two Wednesdays ago so it's a snapshot in time. 
The game is a pretty static state right now (no major updates or content releases) so I expect this data to be usable today. 
The set includes everything from what armor they are wearing to what sparrow they have equipped. 

Today's topic is shaders. 
Whose rocking the hippest shaders and which Guardians are being hipsters straying away from the normal trends?
Well now you can know for sure.

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/characterData/Top10Shaders.html">Top 10 Shaders</a></h4>
        <div id="Top10Shaders">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/Top10Shaders.js'></script>
        </div>
    </div>

Default shader is the most used. 
This shouldn't be surprising when you consider the fact that character's can't equip shaders until level 20.
So now lets look at the top 10 shaders grouped by character level. 
The character level spread isn't normally distributed. About 46% of the characters in this sample set are at level 34. 
Note that the percentages for this graph are the frequency of that shader in that bin not the frequency overall. Also, just to make the plotting easier, this plot shows how the top 10 shaders overall are distributed within each bin. 
These are not necessarily the same as the top 10 shaders in each bin (my graphing library got made at me when I tried to do it that way). 
Also, because you can't equip a shader until level 20, this only looks at characters with a level of 20 or higher.

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/characterData/Top10ShadersByLevel.html">Top 10 Shaders by Level</a></h4>
        <div id="Top10ShadersByLevel">
            <svg></svg>
            <script src='../fullPlots/characterData/javascripts/Top10ShadersByLevel.js'></script>
        </div>
    </div>


I'm not sure if people know this, but you can click on any of the items in the legend to make it disappear. You can also double click it to make it the only thing in the graph.