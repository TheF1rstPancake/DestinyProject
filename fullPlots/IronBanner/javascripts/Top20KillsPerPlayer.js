

                data_Top20KillsPerPlayer=[{"values": [{"y": 4.97653454445362, "x": "The Last Word"}, {"y": 4.924218335983042, "x": "The Messenger (Adept)"}, {"y": 4.7155736012662581, "x": "Thorn"}, {"y": 4.6609294320137691, "x": "Vex Mythoclast"}, {"y": 4.6527960670704944, "x": "Red Death"}, {"y": 4.3748326639892907, "x": "Bad Juju"}, {"y": 4.2239137329527434, "x": "MIDA Multi-Tool"}, {"y": 4.1916961130742045, "x": "SUROS Regime"}, {"y": 4.163810483870968, "x": "Invective"}, {"y": 4.0253271422541159, "x": "Ice Breaker"}, {"y": 3.9224680112773802, "x": "Felwinter's Lie"}, {"y": 3.8846754057428217, "x": "Matador 64"}, {"y": 3.7963369963369962, "x": "Judgment VI"}, {"y": 3.7545072857495678, "x": "Party Crasher +1"}, {"y": 3.2287151702786376, "x": "Her Courtesy"}, {"y": 3.1049085659287776, "x": "BTRD-345"}, {"y": 2.9830262885530945, "x": "Jolder's Hammer"}, {"y": 2.9636125225372889, "x": "Found Verdict"}, {"y": 2.9453020134228187, "x": "Praedyth's Revenge"}, {"y": 2.5, "x": "Radegast's Fury"}], "key": "Weapons", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top20KillsPerPlayer;



                //var width = $('#Top20KillsPerPlayer').width() - 60 - 60;
                //chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Weapon Name');
            chart.yAxis
                .axisLabel('Kills Per Player')                .tickFormat(d3.format(',.2f'));

    
    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#Top20KillsPerPlayer svg')
            .datum(datum)
            .transition().duration(500)
            //.attr('width', $('#Top20KillsPerPlayer').width())
            .attr('height', 450)
            .call(chart);

    
        });


