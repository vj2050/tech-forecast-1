import {Component, OnInit} from '@angular/core';
import Chart from 'chart.js';
import {environment} from '../../../environments/environment';
import {HttpClient} from '@angular/common/http';

@Component({
  selector: 'trend-cmp',
  moduleId: module.id,
  templateUrl: 'trend.component.html'
})

export class TrendComponent implements OnInit {

  public canvas: any;
  public ctx;
  public chartColor;
  public chartHours;
  public chartReputationA;
  public chartReputationU;


  // selected = {id: 5, name: 'Python'};
  private responseData: String;
  private labels: string[];
  private data: number[];
  categories: any;
  selected: any;

  constructor(
    private http: HttpClient
  ) {
  }

  getSelectedValue() {
    //var tag1 = ""

    //tag = this.selected.name
    //const params = {
    //  tags: this.selected.name
    //}

    /*Fix for JSON*/
    const a = 'eScore'
    var tag1 = this.selected.name
    console.log("tag", tag1)
    const response = this.http.get<string>(`http://localhost:5000/current-trends?name=` + tag1);
    
    response.toPromise().then(value => {
      this.responseData = value
      this.labels = Object.keys(this.responseData)

      let dateLabel = []
      this.labels.forEach(label => {
        dateLabel.push(new Date(+label))
      });

      this.data = []
      this.labels.forEach(key => {
        this.data.push(this.responseData[key][a])
      })
      this.chartColor = '#FFFFFF';

      this.canvas = document.getElementById('chartHours');
      this.ctx = this.canvas.getContext('2d');

      this.chartHours = new Chart(this.ctx, {
        type: 'line',
        hover: true,

        data: {
          labels: dateLabel,
          datasets: [{
            label: a,
            borderColor: '#5aad58',
            backgroundColor: '#5aad58',
            pointRadius: 0,
            pointHoverRadius: 0,
            borderWidth: 3,
            data: this.data
          }
          ]
        },
        options: {
          legend: {
            display: true,
            position: 'bottom'
          },

          tooltips: {
            enabled: false
          },

          scales: {
            yAxes: [{
              display : true,
              // scaleLabel:{
              //   display:true,
              //   labelString: 'Posts',
              // },

              ticks: {
                fontColor: '#9f9f9f',
                beginAtZero: false,
                maxTicksLimit: 5,
                padding: 10
              },
              gridLines: {
                drawBorder: false,
                zeroLineColor: '#ccc',
                color: 'rgba(255,255,255,0.05)'
              }

            }],

            xAxes: [{
              display : true,
              fontSize: 100,
              type: 'time',
            time: {
              unit: 'year'
            },
              scaleLabel:{
                display:true,
                labelString: 'Year',
                fontSize : 20,
              },
              
              barPercentage: 1.6,
              gridLines: {
                drawBorder: false,
                color: 'rgba(255,255,255,0.1)',
                zeroLineColor: 'transparent',
                display: false,
              },
              ticks: {
                padding: 10,
                fontColor: '#9f9f9f'
                
              }
            }]
          },
        }
      });

    });
    this.getReputation_answered();
    this.getReputation_unanswered();
  }

  getReputation_answered(){
    // const params = {
    //   tags: this.selected.name
    // }
    var tag2 = this.selected.name
    const b = "num"
    const response = this.http.get<string>(`http://localhost:5000/current-trends/rep/answered?name=`+tag2);
    response.toPromise().then(value => {
      this.responseData = value
      this.labels = Object.keys(this.responseData)
      this.data = []

      this.labels.forEach(key => {
        this.data.push(this.responseData[key][b])
      })

      this.chartColor = '#FFFFFF';
      this.canvas = document.getElementById('chartReputationA');
      this.ctx = this.canvas.getContext('2d');

      this.chartReputationA = new Chart(this.ctx, {
        type: 'pie',
        data: {
          labels: this.labels,
          fontSize: 10,
          datasets: [{
            label: 'Reputation Of Users making comments to Answered Questions',
            pointRadius: 0,
            pointHoverRadius: 0,
            backgroundColor: [
              dynamicColors(),
              dynamicColors(),
              dynamicColors(),
              dynamicColors()
            ],
            borderWidth: 0,
            data: this.data                                     // VJ 
          }]
        },

        options: {

          legend: {
            display: true,
            position: 'bottom'
          },

          pieceLabel: {
            render: 'percentage',
            fontColor: ['white'],
            precision: 2
          },

          tooltips: {
            enabled: false
          },

          scales: {
            yAxes: [{

              ticks: {
                display: false
              },
              gridLines: {
                drawBorder: false,
                zeroLineColor: 'transparent',
                color: 'rgba(255,255,255,0.05)'
              }

            }],

            xAxes: [{
              barPercentage: 1.6,
              gridLines: {
                drawBorder: false,
                color: 'rgba(255,255,255,0.1)',
                zeroLineColor: 'transparent'
              },
              ticks: {
                display: false,
              }
            }]
          },
        }
      });

    });
  }

  getReputation_unanswered(){
    // const params = {
    //   tags: this.selected.name
    // }
    const c = "num"
    var tag3 = this.selected.name
    const response = this.http.get<string>(`http://localhost:5000/current-trends/rep/unanswered?name=`+tag3);
    response.toPromise().then(value => {
      this.responseData = value
      this.labels = Object.keys(this.responseData)
      this.data = []

      this.labels.forEach(key => {
        this.data.push(this.responseData[key][c])
      })

      this.chartColor = '#FFFFFF';
      this.canvas = document.getElementById('chartReputationU');
      this.ctx = this.canvas.getContext('2d');

      this.chartReputationU = new Chart(this.ctx, {
        type: 'pie',
        data: {
          labels: this.labels,
          datasets: [{
            label: 'Reputation Of Users making comments to Unanswered Questions',
            pointRadius: 0,
            pointHoverRadius: 0,
            backgroundColor: [
              dynamicColors(),
              dynamicColors(),
              dynamicColors(),
              dynamicColors()
            ],
            borderWidth: 0,
            data: this.data                                     // VJ 
          }]
        },

        options: {

          legend: {
            display: true,
            position: 'bottom'
          },

          pieceLabel: {
            render: 'percentage',
            fontColor: ['white'],
            precision: 2
          },

          tooltips: {
            enabled: false
          },

          scales: {
            yAxes: [{

              ticks: {
                display: false
              },
              gridLines: {
                drawBorder: false,
                zeroLineColor: 'transparent',
                color: 'rgba(255,255,255,0.05)'
              }

            }],

            xAxes: [{
              barPercentage: 1.6,
              gridLines: {
                drawBorder: false,
                color: 'rgba(255,255,255,0.1)',
                zeroLineColor: 'transparent'
              },
              ticks: {
                display: false,
              }
            }]
          },
        }
      });

    });
  }

  ngOnInit() {
    const response = this.http.get<string[]>(`http://localhost:5000/tags`);
    response.toPromise().then(value => {
      this.categories = []
      value.forEach(value1 => {
        const abc: any = {
          name: value1,
          disabled: false,
        };
        this.categories.push(abc)
      })
    })
  }
}

function dynamicColors() {
  const r = Math.floor(Math.random() * 255);
  const g = Math.floor(Math.random() * 255);
  const b = Math.floor(Math.random() * 255);
  return 'rgb(' + r + ',' + g + ',' + b + ')';
}
