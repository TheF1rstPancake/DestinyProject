

                data_Top20Victory=[{"values": [{"y": 0.51214644553024569, "x": "Thorn"}, {"y": 0.50639966969446737, "x": "The Last Word"}, {"y": 0.4919673426389255, "x": "Red Death"}, {"y": 0.50538389513108617, "x": "Matador 64"}, {"y": 0.51485963612414587, "x": "Party Crasher +1"}, {"y": 0.52689221427022337, "x": "Felwinter's Lie"}, {"y": 0.58957789082909384, "x": "BTRD-345"}, {"y": 0.49077944430784359, "x": "Vex Mythoclast"}, {"y": 0.50663825602360268, "x": "Found Verdict"}, {"y": 0.59076795694473194, "x": "Jolder's Hammer"}, {"y": 0.50428163653663183, "x": "MIDA Multi-Tool"}, {"y": 0.50256410256410255, "x": "Judgment VI"}, {"y": 0.50022311468094594, "x": "Bad Juju"}, {"y": 0.49176867876741237, "x": "Ice Breaker"}, {"y": 0.47614840989399299, "x": "SUROS Regime"}, {"y": 0.52517223105458399, "x": "The Messenger (Adept)"}, {"y": 0.6195286195286196, "x": "Radegast's Fury"}, {"y": 0.49798657718120809, "x": "Praedyth's Revenge"}, {"y": 0.49419504643962853, "x": "Her Courtesy"}, {"y": 0.4994959677419355, "x": "Invective"}], "key": "Weapons", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top20Victory;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Weapon Name');
            chart.yAxis
                .axisLabel('Victory Rate')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#Top20Victory svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


