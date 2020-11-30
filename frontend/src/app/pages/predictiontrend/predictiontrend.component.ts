import {Component, OnInit} from '@angular/core';
import Chart from 'chart.js';
import {HttpClient} from '@angular/common/http';


@Component({
  selector: 'app-predictiontrend-cmp',
  moduleId: module.id,
  templateUrl: 'predictiontrend.component.html'
})

export class PredictionTrendComponent implements OnInit {

  public canvas: any;
  public ctx;
  public chartColor;
  public chartEmail;
  public chartHours;
  public chartReputationA;
  private sidebarVisible: boolean;
  categories: any;
  selected: any;
  private responseData: String;
  private labels: string[];
  private data: {};
  private lineChart: any;

  constructor(
    private http: HttpClient
  ) {
  }


  getSelectedValue() {
    const tags = []

    this.selected.forEach(val => {
      tags.push(val.name);
    })

    const response = this.http.get<string>(`http://localhost:5000/future-trends?name=` + tags);

    response.toPromise().then(value => {
      this.lineChart = undefined
      this.responseData = value
      this.labels = Object.keys(this.responseData)

      let dateLabel = []

      this.labels.forEach(label => {
        dateLabel.push(new Date(+label))
      });


      this.data = {}
      tags.forEach(tag => {
        this.data[tag] = []
      })

      this.labels.forEach(key => {
        tags.forEach(tag => {
          this.data[tag].push(this.responseData[key][tag])
        })
      })

      let chartData = []

      tags.forEach(tag => {
        const color = dynamicColors();
        chartData.push({
          label: tag,
          data: this.data[tag],
          fill: false,
          borderColor: color,
          backgroundColor: 'transparent',
          pointRadius: 0
        })
      })

      this.chartColor = '#FFFFFF';

      const speedCanvas = document.getElementById('speedChart');

      const speedData = {
        labels: dateLabel,
        datasets: chartData
      };
      const chartOptions = {
        legend: {
          display: true,
          position: 'bottom'
        },
        scales: {
          xAxes: [{
            type: 'time',
            time: {
              unit: 'year'
            }
          }]
        }
      };

      this.lineChart = new Chart(speedCanvas, {
        type: 'line',
        hover: true,
        data: speedData,
        options: chartOptions
      });
    })
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
