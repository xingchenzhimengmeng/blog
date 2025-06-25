const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

function sendData() {
    input = document.getElementById('input').value
    // console.log(input)
    post_data = {
        // input_data: 'sh600600',
        // bj920819
        input_data: input,
    }
    axios.post('/play/api/', post_data)
        .then(response => {
            // 处理成功响应
            // console.log('响应数据:', response.data);
            display1(response.data.data1);
            display2(response.data.data1);
            display3(response.data.data1);
            display4(response.data.data2);
            display5(response.data.data2);
            display6(response.data.data2);
            display7(response.data.leida);
            display8(response.data.pie);
            display9(response.data.new_data);
            // alert('数据发送成功！');
        })
        .catch(error => {
            // 处理错误
            console.error('发送失败:', error);
            alert('发送失败，请检查控制台。');
        });
}
//
// function display(data) {
//     let data1 = data.data1
//     let chartDom = document.getElementById('chart4');
//     let myChart = echarts.init(chartDom, 'dark');
//     let option;
//     let series2 = data1['年份'].map(() => ({type: 'bar'}));
//     console.log(series2)
//     option = {
//         title: {
//             text: '盈利能力可视化',
//             textStyle: {
//                 fontSize: 30,
//                 color: "rgba(255, 255, 255, 1)"
//             },
//         },
//         toolbox: {
//             show: true,
//             feature: {
//                 saveAsImage: {}
//             }
//         },
//         grid: {
//             left: '0%',
//             right: '0%',
//             bottom: '4%',
//             top: '10%',
//             containLabel: true
//         },
//         legend: {},
//         tooltip: {trigger: 'item'},
//         dataset: {
//             source: [
//                 ['product'].concat(data1['年份'].map(y => `${y}`)),
//                 ['毛利率'].concat(data1['毛利率']),
//                 ['营业利润率'].concat(data1['营业利润率']),
//                 ['净利率'].concat(data1['净利率']),
//             ]
//         },
//         xAxis: {type: 'category'},
//         yAxis: {},
//         // Declare several bar series, each will be mapped
//         // to a column of dataset.source by default.
//         // series: [{ type: 'bar' }, { type: 'bar' }, { type: 'bar' }]
//         series: data1['年份'].map(() => ({type: 'bar'})),
//     };
//     option && myChart.setOption(option);
// }

function display1(data1) {
    // let data1 = data.data1
    let chartDom = document.getElementById('chart1');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '毛利率',
            textStyle: {
                fontSize: 30,
                color: "rgba(255, 255, 255, 1)"
            },
        },
        color: ["gold"],
        legend: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: data1['年份'].map(y => `${y}`),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '毛利率(%)',
                type: 'bar',
                barWidth: '60%',
                data: data1['毛利率'],
            }
        ]
    };
    option && myChart.setOption(option);
}

function display2(data1) {
    let chartDom = document.getElementById('chart2');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '营业利润率',
            textStyle: {
                fontSize: 30,
                color: "rgba(255, 255, 255, 1)"
            },
        },
        color: ["green"],
        legend: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: data1['年份'].map(y => `${y}`),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '营业利润率(%)',
                type: 'bar',
                barWidth: '60%',
                data: data1['营业利润率'],
            }
        ]
    };
    option && myChart.setOption(option);
}


function display3(data1) {
    let chartDom = document.getElementById('chart3');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '净利率',
            textStyle: {
                fontSize: 30,
                color: "rgba(255, 255, 255, 1)"
            },
        },
        color: ["pink"],
        legend: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: data1['年份'].map(y => `${y}`),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '净利率(%)',
                type: 'bar',
                barWidth: '60%',
                data: data1['净利率'],
            }
        ]
    };
    option && myChart.setOption(option);
}


function display4(data1) {
    let chartDom = document.getElementById('chart4');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '流动比率',
            textStyle: {
                fontSize: 30,
                color: "rgba(255, 255, 255, 1)"
            },
        },
        color: ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFBE0B', '#FB5607', '#8338EC', '#3A86FF', '#FF006E'],
        legend: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: data1['年份'].map(y => `${y}`),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        series: [
            {
                name: '流动比率',
                type: 'bar',
                barWidth: '60%',
                data: data1['流动比率'],
            }
        ]
    };
    option && myChart.setOption(option);
}


function display5(data1) {
    let chartDom = document.getElementById('chart5');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '速动比率',
            textStyle: {
                fontSize: 30,
                color: "rgba(255, 255, 255, 1)"
            },
        },
        color: ["orange"],
        legend: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [
            {
                type: 'category',
                data: data1['年份'].map(y => `${y}`),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '速动比率',
                type: 'bar',
                barWidth: '60%',
                data: data1['速动比率'],
            }
        ]
    };
    option && myChart.setOption(option);
}


function display6(data1) {
    let chartDom = document.getElementById('chart6');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '资产负债率',
            textStyle: {
                fontSize: 30,
                color: "rgba(255, 255, 255, 1)"
            },
        },
        color: ['#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE', '#3BA272', '#FC8452', '#9A60B4'],
        legend: {},
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: [
            {
                type: 'category',
                data: data1['年份'].map(y => `${y}`),
                axisTick: {
                    alignWithLabel: true
                }
            }
        ],
        yAxis: [
            {
                type: 'value'
            }
        ],
        series: [
            {
                name: '资产负债率(%)',
                type: 'bar',
                barWidth: '60%',
                data: data1['资产负债率'],
            }
        ]
    };
    option && myChart.setOption(option);
}

function display7(leida) {
    const chartDom = document.getElementById('chart7');
    const myChart = echarts.init(chartDom, 'dark');
    // 图表配置
    const option = {
        backgroundColor: '#161627',
        // title: {
        //     text: '企业核心能力评估',
        //     left: 'center'
        // },
        legend: {
            data: ['Allocated Budget', 'Actual Spending']
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: function (params) {
                return `${params.name}<br/>${params.seriesName}: ${params.value}%`;
            }
        },
        radar: {
            // shape: 'circle',
            indicator: [
                {
                    name: '盈利能力(加权净资产收益率)',
                    max: 30,
                    min: -30,
                    // detail: '加权ROE = 归母净利润 / 归母股东权益'
                },
                {
                    name: '成长能力(净利润增速)',
                    max: 100,
                    min: -100,
                    // detail: '净利润增速 = (当期净利 - 上年净利) / 上年净利'
                },
                {
                    name: '营运能力(总资产周转率)', max: 300,
                    min: 0,
                    // detail: '总资产周转率 = 营收 / 平均总资产'
                },
                {
                    name: '现金获取能力(销售现金比率)',
                    max: 200,
                    min: 0,
                    // detail: '销售现金比率 = 销售收现 / 营业收入'
                },
                {
                    name: '偿债能力', max: 100,
                    min: 0,
                    // detail: '偿债能力 = 100 - 资产负债率'
                }
            ]
        },
        series: [
            {
                name: '企业核心能力评估',
                type: 'radar',
                data: [
                    {
                        value: leida,
                        // name: '企业核心能力评估',
                        label: {
                            show: true,
                            formatter: function (params) {
                                return params.value.toFixed(1) + '%';
                            },
                            position: 'top'
                        }
                    },
                ]
            }
        ]
    };
    option && myChart.setOption(option);
}
function display8(pie) {
    let chartDom = document.getElementById('chart8');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '营业收入',
            fontSize: 25,
            subtext: '季度占比',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        series: [
            {
                // name: 'Access From',
                type: 'pie',
                radius: '50%',
                data: pie,
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    option && myChart.setOption(option);
}

function display9(new_data) {
    let chartDom = document.getElementById('chart9');
    let myChart = echarts.init(chartDom, 'dark');
    let option;
    option = {
        title: {
            text: '收支变化',
            fontSize: 30,
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            data: ['营业收入(亿元)', '营业成本(亿元)', ]
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: new_data['报告日'],
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: '营业收入(亿元)',
                type: 'line',
                // stack: 'Total',
                data: new_data['营业收入'],
            },
            {
                name: '营业成本(亿元)',
                type: 'line',
                // stack: 'Total',
                data: new_data['营业成本'],
            },
        ]
    };
    option && myChart.setOption(option);
}