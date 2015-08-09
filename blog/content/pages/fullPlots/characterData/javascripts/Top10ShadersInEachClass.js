

        data_Top10ShadersInEachClass=[{"values": [{"y": 0.098351463496691716, "x": "Chatterwhite"}, {"y": 0.083559493103061572, "x": "Thunderdevil"}, {"y": 0.071515083548278569, "x": "Glowhoo"}, {"y": 0.065885387462150946, "x": "Cryptographic"}, {"y": 0.065795671189862057, "x": "Million Million"}, {"y": 0.063395760906134344, "x": "Default Shader"}, {"y": 0.047504766176965349, "x": "Aaru's Passage"}, {"y": 0.037108893125490636, "x": "God of War"}, {"y": 0.034966917124593475, "x": "Bittersteel"}, {"y": 0.034585622967365705, "x": "The Queen's Web"}], "key": "Hunter", "yAxis": "1"}, {"values": [{"y": 0.14694623708684024, "x": "Thunderdevil"}, {"y": 0.082411110838465876, "x": "Chatterwhite"}, {"y": 0.065577994258091424, "x": "Glowhoo"}, {"y": 0.05959070497877457, "x": "Cryptographic"}, {"y": 0.054867126346526636, "x": "The Queen's Web"}, {"y": 0.052720045150050306, "x": "Sunsetting"}, {"y": 0.045309547763354843, "x": "Million Million"}, {"y": 0.044278948789046202, "x": "Default Shader"}, {"y": 0.036328613844379555, "x": "Polar Oak"}, {"y": 0.035224400657620294, "x": "Aaru's Passage"}], "key": "Titan", "yAxis": "1"}, {"values": [{"y": 0.093717913917836029, "x": "Chatterwhite"}, {"y": 0.074646241724003637, "x": "Glowhoo"}, {"y": 0.073100208891459059, "x": "Default Shader"}, {"y": 0.070067152113108239, "x": "Million Million"}, {"y": 0.06736454510049214, "x": "Thunderdevil"}, {"y": 0.06123942265705215, "x": "The Queen's Web"}, {"y": 0.060625730234973384, "x": "Cryptographic"}, {"y": 0.043170901537771589, "x": "Aaru's Passage"}, {"y": 0.039229107903650293, "x": "Provincial Royale"}, {"y": 0.034402180968453849, "x": "Sunsetting"}], "key": "Warlock", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top10ShadersInEachClass;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Shader');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#Top10ShadersInEachClass svg')
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



