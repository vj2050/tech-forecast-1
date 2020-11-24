import {Component, OnInit} from '@angular/core';
import Chart from 'chart.js';
import {environment} from '../../../environments/environment';
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
  private sidebarVisible: boolean;
  categories: any;
  selected: any;
  private responseData: String;
  private labels: string[];
  private data: {};

  constructor(
    private http: HttpClient
  ) {
  }


  getSelectedValue() {
    const tags = []
    this.selected.forEach(val => {
      tags.push(val.name);
    })


    const params = {
      tags: tags
    }

    const response = this.http.get<string>(`${environment.apiUrl}/prediction`, {params: params});
    const tagsForTest = ['posts', 'posts_x', 'posts_y']

    response.toPromise().then(value => {
      this.responseData = value
      this.labels = Object.keys(this.responseData)
      this.data = {}
      tagsForTest.forEach(tag => {
        this.data[tag] = []
      })

      this.labels.forEach(key => {
        tagsForTest.forEach(tag => {
          this.data[tag].push(this.responseData[key][tag])
        })
      })

      let chartData = []

      // tagsForTest.forEach(tag => {
      //   chartData[tag] = []
      // })

      tagsForTest.forEach(tag => {
        const color = dynamicColors();
        chartData.push({
          data: this.data[tag],
          fill: false,
          borderColor: color,
          backgroundColor: 'transparent',
          pointBorderColor: color,
          pointRadius: 4,
          pointHoverRadius: 4,
          pointBorderWidth: 8,
        })
      })

      this.chartColor = '#FFFFFF';

      const speedCanvas = document.getElementById('speedChart');

      console.log(chartData)

      const speedData = {
        labels: this.labels,
        datasets: chartData
      };

      const chartOptions = {
        legend: {
          display: false,
          position: 'top'
        }
      };

      const lineChart = new Chart(speedCanvas, {
        type: 'line',
        hover: false,
        data: speedData,
        options: chartOptions
      });
    })
  }

  ngOnInit() {
    const response = this.http.get<string[]>(`${environment.apiUrl}/tags`);
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
