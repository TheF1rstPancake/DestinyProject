

        data_classCombosVictoryRate=[{"values": [{"y": 0.5508684863523573, "x": "0 Hunters, 0 Titans, 3 Warlocks"}, {"y": 0.54847645429362879, "x": "0 Hunters, 1 Titans, 2 Warlocks"}, {"y": 0.46464646464646464, "x": "0 Hunters, 2 Titans, 1 Warlocks"}, {"y": 0.38157894736842102, "x": "0 Hunters, 3 Titans, 0 Warlocks"}, {"y": 0.54489639293937064, "x": "1 Hunters, 0 Titans, 2 Warlocks"}, {"y": 0.48124191461836996, "x": "1 Hunters, 1 Titans, 1 Warlocks"}, {"y": 0.42997542997542992, "x": "1 Hunters, 2 Titans, 0 Warlocks"}, {"y": 0.51207022677395764, "x": "2 Hunters, 0 Titans, 1 Warlocks"}, {"y": 0.4836601307189542, "x": "2 Hunters, 1 Titans, 0 Warlocks"}, {"y": 0.5200764818355641, "x": "3 Hunters, 0 Titans, 0 Warlocks"}], "key": "Class Combinations", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_classCombosVictoryRate;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-10)                .axisLabel('Class Combos');
            chart.yAxis
                .axisLabel('Victory Rate')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#classCombosVictoryRate svg')
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



