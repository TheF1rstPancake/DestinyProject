

        data_classCombosOverallVictoryRate=[{"values": [{"y": 0.057692307692307696, "x": "0 Hunters, 0 Titans, 3 Warlocks"}, {"y": 0.10291060291060292, "x": "0 Hunters, 1 Titans, 2 Warlocks"}, {"y": 0.059771309771309775, "x": "0 Hunters, 2 Titans, 1 Warlocks"}, {"y": 0.0075363825363825368, "x": "0 Hunters, 3 Titans, 0 Warlocks"}, {"y": 0.18451143451143451, "x": "1 Hunters, 0 Titans, 2 Warlocks"}, {"y": 0.19334719334719336, "x": "1 Hunters, 1 Titans, 1 Warlocks"}, {"y": 0.045478170478170481, "x": "1 Hunters, 2 Titans, 0 Warlocks"}, {"y": 0.18191268191268192, "x": "2 Hunters, 0 Titans, 1 Warlocks"}, {"y": 0.096153846153846159, "x": "2 Hunters, 1 Titans, 0 Warlocks"}, {"y": 0.07068607068607069, "x": "3 Hunters, 0 Titans, 0 Warlocks"}], "key": "Class Combinations", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_classCombosOverallVictoryRate;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-10)                .axisLabel('Class Combos');
            chart.yAxis
                .axisLabel('Victory Rate')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#classCombosOverallVictoryRate svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);


    chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
     });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
    });

    });



