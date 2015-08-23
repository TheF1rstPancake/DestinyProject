

        data_classCombos=[{"values": [{"y": 0.052977520704614173, "x": "0 Hunters, 0 Titans, 3 Warlocks"}, {"y": 0.094912580517944004, "x": "0 Hunters, 1 Titans, 2 Warlocks"}, {"y": 0.065071644537925591, "x": "0 Hunters, 2 Titans, 1 Warlocks"}, {"y": 0.0099907979492572623, "x": "0 Hunters, 3 Titans, 0 Warlocks"}, {"y": 0.17128960168266072, "x": "1 Hunters, 0 Titans, 2 Warlocks"}, {"y": 0.20323386354673328, "x": "1 Hunters, 1 Titans, 1 Warlocks"}, {"y": 0.053503352175627711, "x": "1 Hunters, 2 Titans, 0 Warlocks"}, {"y": 0.17970290521887736, "x": "2 Hunters, 0 Titans, 1 Warlocks"}, {"y": 0.10056526883133955, "x": "2 Hunters, 1 Titans, 0 Warlocks"}, {"y": 0.068752464835020372, "x": "3 Hunters, 0 Titans, 0 Warlocks"}], "key": "Class Combinations", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_classCombos;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-10)                .axisLabel('Class Combos');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#classCombos svg')
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



