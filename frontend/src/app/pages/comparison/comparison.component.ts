import {Component, OnInit} from '@angular/core';
import * as Chart from 'chart.js';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../../environments/environment';
//import ChartDataLabels from 'chartjs-plugin-datalabels';

@Component({
  selector: 'app-comparison-cmp',
  moduleId: module.id,
  templateUrl: 'comparison.component.html'
})

export class ComparisonComponent implements OnInit {

  public canvas: any;
  public ctx;
  public chartColor;
  //public chartComparison;
  public chartHours;
  public chartReputationA;
  categories: any;
  selected: any;
  private labels: string[];
  private responseData: String;
  private data: {};
  private lineChart: any;

  private sidebarVisible: boolean;

  constructor(
    private http: HttpClient
  ) {
  }

  getSelectedValue() {
    const tags = []
    const encodedTags = []
    this.selected.forEach(val => {
      tags.push(val.name);
      encodedTags.push(encodeURIComponent(val.name));
    })

    console.log('selected tag', this.selected);
    const response = this.http.get<string>(`http://localhost:5000/comparison?name=` + encodedTags);

//////////////////// Vaish trial

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

      const chartComparison = document.getElementById('chartComparison');

      const chartData1 = {
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
            },
            scaleLabel: {
              display: true,
              labelString: 'Year',
              fontSize : 20,
            },
          }],

          yAxes: [{
            display: true,
            scaleLabel: {
              display: true,
              labelString: 'Effective Score',
              fontSize : 15,
            },
          }]
        }

      };

      this.lineChart = new Chart(chartComparison, {
        type: 'line',
        hover: true,
        data: chartData1,
        options: chartOptions
      });


////////////////////////////////////////////////////////////////////////

      
    });
  }

  ngOnInit() {
    const response = this.http.get<string[]>(`http://localhost:5000/tags`);
    response.toPromise().then(value => {
      console.log(value)
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
