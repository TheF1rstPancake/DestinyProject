

                data_Top10Weapons=[{"values": [{"y": 0.18601714027965718, "x": "Thorn"}, {"y": 0.093459630130807395, "x": "The Last Word"}, {"y": 0.07308174209392071, "x": "Red Death"}, {"y": 0.059149000150353327, "x": "Matador 64"}, {"y": 0.055450308224327172, "x": "Party Crasher +1"}, {"y": 0.040304716082794567, "x": "Felwinter's Lie"}, {"y": 0.027504635894351728, "x": "Vex Mythoclast"}, {"y": 0.020949230692126498, "x": "Found Verdict"}, {"y": 0.020638500476118881, "x": "BTRD-345"}, {"y": 0.018643812960457074, "x": "MIDA Multi-Tool"}], "key": "Weapons", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top10Weapons;



                var width = $('#Top10Weapons').width() - 60 - 60;
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Weapon Name');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#Top10Weapons svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#Top10Weapons').width())
            .attr('height', 450)
            .call(chart);

    
        });


