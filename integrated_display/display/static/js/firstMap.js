      function firstMap(){

        var myChart = echarts.init(document.getElementById('header_one'));
        option = {

          series : [
            {
              name: '速度',
              type: 'gauge',
              z: 3,
              min: 0,
              max: 120,
              splitNumber: 6,
              radius: '100%',
              axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                  width: 3
                }
              },
              axisTick: {            // 坐标轴小标记
                length: 5,        // 属性length控制线长
                lineStyle: {       // 属性lineStyle控制线条样式
                  color: 'auto'
                }
              },
              splitLine: {           // 分隔线
                length: 10,         // 属性length控制线长
                lineStyle: {       // 属性lineStyle（详见lineStyle）控制线条样式
                  color: 'auto'
                }
              },
              title : {
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                  fontWeight: 'bolder',
                  fontSize: 10,
                  fontStyle: 'italic'
                }
              },
              detail : {
		formatter:'{value}%',
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                  fontWeight: '10'
                }
              },
	                    
	     data:{value: kpi_ratio, name: '季度KPI\nVV达标率'}
            }
          ]
        };

        setInterval(function (){
          myChart.setOption(option,true);
        }.call(this),2000);
        window.onresize = myChart.resize;
      }
      firstMap();