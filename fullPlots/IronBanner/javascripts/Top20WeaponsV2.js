

                data_Top20WeaponsV2=[{"values": [{"y": 0.16981466405459089, "x": "Thorn"}, {"y": 0.089612290138670489, "x": "The Last Word"}, {"y": 0.065673631789011686, "x": "Red Death"}, {"y": 0.061691083627315769, "x": "Matador 64"}, {"y": 0.056511540591880509, "x": "Party Crasher +1"}, {"y": 0.044822873258564523, "x": "Felwinter's Lie"}, {"y": 0.027981923642631357, "x": "BTRD-345"}, {"y": 0.023488855928160482, "x": "Vex Mythoclast"}, {"y": 0.02240462144107774, "x": "Found Verdict"}, {"y": 0.017857032220970705, "x": "Jolder's Hammer"}, {"y": 0.016502668455963352, "x": "MIDA Multi-Tool"}, {"y": 0.012842292827572021, "x": "Judgment VI"}, {"y": 0.012148382755839068, "x": "Bad Juju"}, {"y": 0.011816297221509725, "x": "Ice Breaker"}, {"y": 0.011759297465617375, "x": "SUROS Regime"}, {"y": 0.011513950690254652, "x": "The Messenger (Adept)"}, {"y": 0.01104060489132253, "x": "Radegast's Fury"}, {"y": 0.010875801249285954, "x": "Praedyth's Revenge"}, {"y": 0.010338020943692915, "x": "Her Courtesy"}, {"y": 0.010236412683189162, "x": "Invective"}], "key": "Weapons", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top20WeaponsV2;



                var width = $('#Top20WeaponsV2').width() - 60 - 60;
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Weapon Name');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#Top20WeaponsV2 svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#Top20WeaponsV2').width())
            .attr('height', 450)
            .call(chart);

    
        });


