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
  private data: number[];

  constructor(
    private http: HttpClient
  ) {
  }


  getSelectedValue() {
    const tags = []
    this.selected.forEach(val => {
      tags.push(val.name);
    })

    const tagsForTest = ['posts', 'posts_x', 'posts_y']

    const params = {
      tags: tags
    }

    const response = this.http.get<string>(`${environment.apiUrl}/prediction`, {params: params});
    response.toPromise().then(value => {
      this.responseData = value
      this.labels = Object.keys(this.responseData)
      this.data = []
      this.labels.forEach(key => {
        this.data.push(this.responseData[key].posts)
      })

      this.chartColor = '#FFFFFF';

      const speedCanvas = document.getElementById('speedChart');

      const dataFirst = {
        data: [0, 19, 15, 20, 30, 40, 40, 50, 25, 30, 50, 70],
        fill: false,
        borderColor: '#fbc658',
        backgroundColor: 'transparent',
        pointBorderColor: '#fbc658',
        pointRadius: 4,
        pointHoverRadius: 4,
        pointBorderWidth: 8,
      };

      const dataSecond = {
        data: [0, 5, 10, 12, 20, 27, 30, 34, 42, 45, 55, 63],
        fill: false,
        borderColor: '#51CACF',
        backgroundColor: 'transparent',
        pointBorderColor: '#51CACF',
        pointRadius: 4,
        pointHoverRadius: 4,
        pointBorderWidth: 8
      };

      const speedData = {
        labels: this.labels,
        datasets: [dataFirst, dataSecond]
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
