

        data_IntellectDisciplineStrengthBySub=[{"values": [{"y": 201.1692264367567, "x": "Bladedancer"}, {"y": 211.71768409591215, "x": "Defender"}, {"y": 190.09240356221079, "x": "Gunslinger"}, {"y": 184.21949107211086, "x": "Striker"}, {"y": 153.45727206946455, "x": "Sunsinger"}, {"y": 176.50836926628867, "x": "Voidwalker"}], "key": "Intellect", "yAxis": "1"}, {"values": [{"y": 149.04891363212963, "x": "Bladedancer"}, {"y": 142.52427391294057, "x": "Defender"}, {"y": 163.47927081637872, "x": "Gunslinger"}, {"y": 174.58052930538221, "x": "Striker"}, {"y": 173.18570911722142, "x": "Sunsinger"}, {"y": 164.20670220351067, "x": "Voidwalker"}], "key": "Discipline", "yAxis": "1"}, {"values": [{"y": 171.26250460325369, "x": "Bladedancer"}, {"y": 174.49208227803157, "x": "Defender"}, {"y": 166.67186737042806, "x": "Gunslinger"}, {"y": 158.21839578185893, "x": "Striker"}, {"y": 201.74654486251808, "x": "Sunsinger"}, {"y": 176.70257698706413, "x": "Voidwalker"}], "key": "Strength", "yAxis": "1"}];


        nv.addGraph(function() {
            var chart = nv.models.multiBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_IntellectDisciplineStrengthBySub;



                var height = 450 - 30 - 20;
                chart.height(height);





            chart.xAxis
                .rotateLabels(-25)                .axisLabel('Class');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.1f'));




      chart.showLegend(true);


            nv.utils.windowResize(function(){chart.update();});

        


        d3.select('#IntellectDisciplineStrengthBySub svg')
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



