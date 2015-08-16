Don't Hate the Game; Hate the Player
===============================================
:date: 2015-07-19
:modified: 2015-07-19
:tags: Crucible, Iron Banner, weapon, balancing 
:authors: Giovanni Briggs
:summary: Examining weapon balancing in Crucible.
:category: Stat Porn Sunday

See the `original post on reddit <https://www.reddit.com/r/DestinyTheGame/comments/3dur9n/stat_porn_sunday_dont_hate_the_game_hate_the/>`_

Introductory Statements
-------------------------
Welcome to Stat Porn Sunday where we look at completely-safe-for-work content still likely to get you riled (shoutout to `/u/obsidianchao <https://www.reddit.com/user/obsidianchao>`_ for the naming inspiration).
Last week's post was about `Weapon Pairings in Crucible <https://www.reddit.com/r/DestinyTheGame/comments/3d1hy0/stat_sunday_weapon_pairings/>`_.

Overview
--------------------
Given the interest taken in `the post <https://www.reddit.com/r/DestinyTheGame/comments/3dqkoi/bungies_numbers_dont_add_up/>`_ made by `/u/MKerrsive <https://www.reddit.com/user/MKerrsive>`_ yesterday, I thought it would be appropriate to make this Stat Porn Sunday about weapon usage in the Iron Banner.
Everyone cares deeply about their weapons, and I think the general outcry against the upcoming weapon tuning is reasonable.
`/u/MKerrsive <https://www.reddit.com/user/MKerrsive>`_ set out to analyze data in order to explain why the weapon tuning is being implemented. Bungie's explanation didn't sit right with him (`or me either <https://www.reddit.com/r/DestinyTheGame/comments/3dp0is/most_equipped_most_used/>`), and he's doing some awesome work, but there is still one metric that I don't think has been considered yet.

Before we dive in to the data, let me describe the dataset that I used and the potential biases in it. 
I grabbed over 8,000 games worth of data from the last Iron Banner. 
Unfortunately, due to the sampling method I used and the way the API is set up, most of these games are from the last 3 days of Iron Banner. 
While I don't think weapon usage changes significantly from day to day, it is a bias in the data. 
The other bias is that this data only covers Xbox One users, so there will be no mention of PSN exclusives here.

Let's take Power
---------------------
Now for the fun part. Here is a graph of the Top 20 Weapons By Kills in Iron Banner.

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/IronBanner/Top20WeaponsV2.html">Top 20 Killing Machines in Iron Banner</a></h4>
        <div id="Top20WeaponsV2">
            <svg></svg>
            <script src='../fullPlots/IronBanner/javascripts/Top20WeaponsV2.js'></script>
        </div>
    </div>

Surprise! The top weapon is Thorn. 
This differs from the graph Bungie posted in their weekly update because my graph looks at all weapon types, unlike Bungie's which only looked at primaries. 
Still the trend is obvious. 
Thorn kills almost twice as many people as the next weapon. 
Also worth noting is that only 8 of the top weapons are primary weapons (and there are 0 fusion rifles up there) and that the top 20 weapons account for 69.89% of all weapon kills.
So that probably wasn't actually surprising for anyone. 

This next part might be. 

**Just because Thorn is the most used, doesn't mean it's overpowered**. 
It is certainly an indication that Thorn is more powerful, but it is not definitive proof. 
What we really need to do is look at how effective the weapon is. 

When I think of effectiveness, I think of the weapon's ability to kill players in relation to other weapons. 
Simply killing more is not enough. 
Another metric is needed.
There are probably several ways of doing this, but the stat that I created is *Kills-Per-Player (KPP)*. 
I took the total number of kills for each weapon and then divided that by the number of people using it. 
By "using it", I mean the number of players who had at least 1 kill with the weapon. 
Basically, it tries to removes the bias due to the majority of players using only a small subset of the weapon base.
Look at this graph (or read the table below if that's more your speed.) 

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/IronBanner/Top20KillsPerPlayer.html">Kills per Player for the top 20 Weapons Used</a></h4>
        <div id="Top20KillsPerPlayer">
            <svg></svg>
            <script src='../fullPlots/IronBanner/javascripts/Top20KillsPerPlayer.js'></script>
        </div>
    </div>

.. html::
    <table class="table table-bordered">
      <tr>
        <th class="tg-031e">Weapon Name</th>
        <th class="tg-031e">Players Using</th>
        <th class="tg-031e">Total Kills</th>
        <th class="tg-031e">Frequency</th>
        <th class="tg-031e">Kills Per Player</th>
      </tr>
      <tr>
        <td class="tg-031e">The Last Word</td>
        <td class="tg-031e">14532</td>
        <td class="tg-031e">72319</td>
        <td class="tg-031e">0.089612</td>
        <td class="tg-031e">4.976535</td>
      </tr>
      <tr>
        <td class="tg-031e">The Messenger (Adept)</td>
        <td class="tg-031e">1887</td>
        <td class="tg-031e">9292</td>
        <td class="tg-031e">0.011514</td>
        <td class="tg-031e">4.924218</td>
      </tr>
      <tr>
        <td class="tg-031e">Thorn</td>
        <td class="tg-031e">29062</td>
        <td class="tg-031e">137044</td>
        <td class="tg-031e">0.169815</td>
        <td class="tg-031e">4.715574</td>
      </tr>
      <tr>
        <td class="tg-031e">Vex Mythoclast</td>
        <td class="tg-031e">4067</td>
        <td class="tg-031e">18956</td>
        <td class="tg-031e">0.023489</td>
        <td class="tg-031e">4.660929</td>
      </tr>
      <tr>
        <td class="tg-031e">Red Death</td>
        <td class="tg-031e">11391</td>
        <td class="tg-031e">53000</td>
        <td class="tg-031e">0.065674</td>
        <td class="tg-031e">4.652796</td>
      </tr>
      <tr>
        <td class="tg-031e">Bad Juju</td>
        <td class="tg-031e">2241</td>
        <td class="tg-031e">9804</td>
        <td class="tg-031e">0.012148</td>
        <td class="tg-031e">4.374833</td>
      </tr>
      <tr>
        <td class="tg-031e">MIDA Multi-Tool</td>
        <td class="tg-031e">3153</td>
        <td class="tg-031e">13318</td>
        <td class="tg-031e">0.016503</td>
        <td class="tg-031e">4.223914</td>
      </tr>
      <tr>
        <td class="tg-031e">SUROS Regime</td>
        <td class="tg-031e">2264</td>
        <td class="tg-031e">9490</td>
        <td class="tg-031e">0.011759</td>
        <td class="tg-031e">4.191696</td>
      </tr>
      <tr>
        <td class="tg-031e">Invective</td>
        <td class="tg-031e">1984</td>
        <td class="tg-031e">8261</td>
        <td class="tg-031e">0.010236</td>
        <td class="tg-031e">4.16381</td>
      </tr>
      <tr>
        <td class="tg-031e">Ice Breaker</td>
        <td class="tg-031e">2369</td>
        <td class="tg-031e">9536</td>
        <td class="tg-031e">0.011816</td>
        <td class="tg-031e">4.025327</td>
      </tr>
      <tr>
        <td class="tg-031e">Felwinter's Lie</td>
        <td class="tg-031e">9222</td>
        <td class="tg-031e">36173</td>
        <td class="tg-031e">0.044823</td>
        <td class="tg-031e">3.922468</td>
      </tr>
      <tr>
        <td class="tg-031e">Matador 64</td>
        <td class="tg-031e">12816</td>
        <td class="tg-031e">49786</td>
        <td class="tg-031e">0.061691</td>
        <td class="tg-031e">3.884675</td>
      </tr>
      <tr>
        <td class="tg-031e">Judgment VI</td>
        <td class="tg-031e">2730</td>
        <td class="tg-031e">10364</td>
        <td class="tg-031e">0.012842</td>
        <td class="tg-031e">3.796337</td>
      </tr>
      <tr>
        <td class="tg-031e">Party Crasher +1</td>
        <td class="tg-031e">12147</td>
        <td class="tg-031e">45606</td>
        <td class="tg-031e">0.056512</td>
        <td class="tg-031e">3.754507</td>
      </tr>
      <tr>
        <td class="tg-031e">Her Courtesy</td>
        <td class="tg-031e">2584</td>
        <td class="tg-031e">8343</td>
        <td class="tg-031e">0.010338</td>
        <td class="tg-031e">3.228715</td>
      </tr>
      <tr>
        <td class="tg-031e">BTRD-345</td>
        <td class="tg-031e">7273</td>
        <td class="tg-031e">22582</td>
        <td class="tg-031e">0.027982</td>
        <td class="tg-031e">3.104909</td>
      </tr>
      <tr>
        <td class="tg-031e">Jolder's Hammer</td>
        <td class="tg-031e">4831</td>
        <td class="tg-031e">14411</td>
        <td class="tg-031e">0.017857</td>
        <td class="tg-031e">2.983026</td>
      </tr>
      <tr>
        <td class="tg-031e">Found Verdict</td>
        <td class="tg-031e">6101</td>
        <td class="tg-031e">18081</td>
        <td class="tg-031e">0.022405</td>
        <td class="tg-031e">2.963613</td>
      </tr>
      <tr>
        <td class="tg-031e">Praedyth's Revenge</td>
        <td class="tg-031e">2980</td>
        <td class="tg-031e">8777</td>
        <td class="tg-031e">0.010876</td>
        <td class="tg-031e">2.945302</td>
      </tr>
      <tr>
        <td class="tg-031e">Radegast's Fury</td>
        <td class="tg-031e">3564</td>
        <td class="tg-031e">8910</td>
        <td class="tg-031e">0.011041</td>
        <td class="tg-031e">2.5</td>
      </tr>
    </table>


That's right. 
Thorn does not have the highest Kills Per Player, because Thorn isn't the beast we *perceive* it to be. 
What we expect from a well balanced game is not that there is the same number of kills for each weapon, but that the Kills Per Player is the same. 
The fact is that Destiny is more balanced than we believe. 
Sorting them by decreasing KPP actually clusters the weapons by primary and secondary. 
The top 8 are primaries, followed by 7 secondaries and then a cluster of secondaries and heavies. 
You can see that the KPP is actually fairly balanced within each cluster.

Now that graph only shows the KPP for the top 20 most used weapons, not the weapons with the top KPP. 
That's because KPP suffers as a metric when there isn't enough data. 
Strange Suspect actually has the highest KPP (according to my data) because it has 90 kills across 14 players giving it a KPP of about 6.6. 
Almost 40% greater than Thorn, but no one is complaining about Strange Suspect.

The point is, we have a *perception* problem, and the graph that Bungie posted in the weekly update didn't exactly help matters (it is literally the causation of /u/MKerssive's post). I have made graphs that fed the perception and others have too, but Thorn isn't the monster we make it out to be. That's probably why Bungie isn't doing a Thorn specific nerf. There doesn't need to be one. Bungie is using their own metrics to evaluate weapons and are making changes accordingly.

One last graph that I think seals the deal.

.. html::
    <div class="plotContainer">
        <h4 class="text-center"><a href="/DestinyProject/blog/output/fullPlots/IronBanner/Top20Victory.html">Victory Rate by Weapons</a></h4>
        <div id="Top20Victory">
            <svg></svg>
            <script src='../fullPlots/IronBanner/javascripts/Top20Vcitory.js'></script>
        </div>
    </div>

People who use Thorn win 50% of their games. People who use MIDA win 50% of their games. Guess what? Doesn't matter. 
The spikes on heavy weapons is actually interesting. I think this has more to do with the general statement that player's who get heavy kills are more likely to win than those who don't. But even the victory rate with the heavy weapons is pretty much the same.

So if you're rocking Thorn, maybe it's time to branch out. You aren't doing any better than the rest of us.

TL;DR
--------
There's a different way of looking at weapon usage and it shows that Thorn isn't the horribly unbalanced weapon we think it is. In fact, Destiny actually appears to be fairly balanced when we start looking at and comparing different metrics.