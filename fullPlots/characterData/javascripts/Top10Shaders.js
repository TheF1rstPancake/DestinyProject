

                data_Top10Shaders=[{"values": [{"y": 0.17449445082807544, "x": "Default Shader"}, {"y": 0.086474882514431972, "x": "Thunderdevil"}, {"y": 0.080598883973110769, "x": "Chatterwhite"}, {"y": 0.06208673634380784, "x": "Glowhoo"}, {"y": 0.054593806119570376, "x": "Cryptographic"}, {"y": 0.053314021893943041, "x": "Million Million"}, {"y": 0.043846370848441896, "x": "The Queen's Web"}, {"y": 0.037034616099135116, "x": "Aaru's Passage"}, {"y": 0.032314551697090209, "x": "Sunsetting"}, {"y": 0.028382311455444932, "x": "God of War"}], "key": "Shaders", "yAxis": "1"}];


                nv.addGraph(function() {
            var chart = nv.models.discreteBarChart();

            chart.margin({top: 30, right: 60, bottom: 20, left: 60});

            var datum = data_Top10Shaders;



                var width = $('#Top10Shaders').width() - 60 - 60;
                chart.width(width);
                var height = 450 - 30 - 20;
                chart.height(height);




                    chart.xAxis
                .rotateLabels(-25)                .axisLabel('Shaders');
            chart.yAxis
                .axisLabel('Frequency')                .tickFormat(d3.format(',.2%'));

    
    
            nv.utils.windowResize(function(){ chart.update(); });

        



            d3.select('#Top10Shaders svg')
            .datum(datum)
            .transition().duration(500)
            .attr('width', $('#Top10Shaders').width())
            .attr('height', 450)
            .call(chart);

    
        });


