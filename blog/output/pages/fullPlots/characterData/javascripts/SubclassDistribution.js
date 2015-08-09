

                data_SubclassDistribution=[{"values": [{"y": 0.1733694792103869, "x": "Bladedancer"}, {"y": 0.15885149686590475, "x": "Defender"}, {"y": 0.16949572373174071, "x": "Gunslinger"}, {"y": 0.16621025616326193, "x": "Striker"}, {"y": 0.20627575909782092, "x": "Sunsinger"}, {"y": 0.12579728493088477, "x": "Voidwalker"}], "key": "Subclass", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_SubclassDistribution;



                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Subclass');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){chart.update();});

        



            d3.select('#SubclassDistribution svg')
            .datum(datum)
            .transition().duration(500)
            .attr('height', 450)
            .call(chart);

    
        });


