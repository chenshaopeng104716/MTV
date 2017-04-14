      function platform_dau_day(){

          // 基于准备好的dom，初始化echarts实例
          var myChart = echarts.init(document.getElementById('platform_dau_day'));
          myChart.showLoading();
          // 指定图表的配置项和数据
          option = {
                    tooltip: {
                      trigger: 'axis'
                    },
                    legend: {
                      data:['DAU', 'UV占比']
                    },
                    toolbox: {
                      show: true,
                      feature: {
                        dataView: {readOnly: false},
                        saveAsImage: {}
                      }
                    },
                    dataZoom: {
                      show: false,
                      start: 0,
                      end: 100
                    },
                    xAxis: [
                      {
                        type: 'category',
                        boundaryGap: true,
                        data:vv_day_date,
                        splitLine: {
                            show: false
                        }
                      },
                    ],
                    yAxis: [
                      {
                        type: 'value',
                        scale: true,
                        name: 'DAU',
                        max: 4000,
                        min: 0,
                        boundaryGap: [0.2, 0.2],
                        splitLine: {
                            show: false
                        }
                      },
                      {
                        type: 'value',
                        scale: true,
                        name: 'UV占比',
                        max: 1,
                        min: 0,
                        boundaryGap: [0.2, 0.2],
                        splitLine: {
                            show: false
                        }
                      }
                    ],
                    series: [
                      {
                        name:'DAU',
                        type:'bar',
                        data:dau_day_data

                      },
                      {
                        name:'UV占比',
                        type:'line',
                        yAxisIndex: 1,
                        label: {
                            normal: {
                                show: false,
                                position: 'top'
                            }
                        },
                        data:uv_ration_day_data

                      }
                    ]
                  };
          myChart.hideLoading();
          // 使用刚指定的配置项和数据显示图表。
          myChart.setOption(option);
          window.onresize = myChart.resize;
      }
      platform_dau_day();