

                data_MostUsedShipsOverall=[{"values": [{"y": 0.01865319911653605, "x": "\"Ketch Me If You Can\""}, {"y": 0.01887681732800319, "x": "Kestrel Class EX"}, {"y": 0.021567116425961732, "x": "\"Little Light\""}, {"y": 0.032675781115614054, "x": "\"Bane of Dark Gods\""}, {"y": 0.03723415234936733, "x": "Ceres Galliot"}, {"y": 0.03983156388256259, "x": "\"Light in the Abyss\""}, {"y": 0.04053338103855178, "x": "\"Draught of Nectar\""}, {"y": 0.07221492118318115, "x": "\"Aspect of Glass\""}, {"y": 0.10464644240626957, "x": "Arcadia Class Jumpship"}, {"y": 0.13977514328766935, "x": "Hildian Seeker"}], "key": "Most Used Ships", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_MostUsedShipsOverall;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Ship');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#MostUsedShipsOverall svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


