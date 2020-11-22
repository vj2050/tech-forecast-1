import {Component, OnInit} from '@angular/core';
import Chart from 'chart.js';
import {environment} from '../../../environments/environment';
import {HttpClient} from '@angular/common/http';
import {publish} from 'rxjs/operators';

@Component({
  selector: 'trend-cmp',
  moduleId: module.id,
  templateUrl: 'trend.component.html'
})

export class TrendComponent implements OnInit {

  public canvas: any;
  public ctx;
  public chartColor;
  public chartEmail;
  public chartHours;


  // selected = {id: 5, name: 'Python'};
  private responseData: String;
  private labels: string[];
  private data: number[];
  categories: any ;
  selected: any;

  constructor(
    private http: HttpClient
  ) {
  }

  getSelectedValue() {
    console.log(this.selected);
    const tagsArr = {
      tags: this.selected.name
    }
    const response = this.http.get<String>(`${environment.apiUrl}/current/trend/`, {params: tagsArr});
    response.toPromise().then(value => {
      this.responseData = value
      this.labels = Object.keys(this.responseData)
      this.data = []
      this.labels.forEach(key => {
        this.data.push(this.responseData[key].posts)
      })
      this.chartColor = '#FFFFFF';

      this.canvas = document.getElementById('chartHours');
      this.ctx = this.canvas.getContext('2d');

      this.chartHours = new Chart(this.ctx, {
        type: 'line',

        data: {
          labels: this.labels,
          datasets: [{
            borderColor: '#6bd098',
            backgroundColor: '#6bd098',
            pointRadius: 0,
            pointHoverRadius: 0,
            borderWidth: 3,
            data: this.data
          }
          ]
        },
        options: {
          legend: {
            display: false
          },

          tooltips: {
            enabled: false
          },

          scales: {
            yAxes: [{

              ticks: {
                fontColor: '#9f9f9f',
                beginAtZero: false,
                maxTicksLimit: 5,
                // padding: 20
              },
              gridLines: {
                drawBorder: false,
                zeroLineColor: '#ccc',
                color: 'rgba(255,255,255,0.05)'
              }

            }],

            xAxes: [{
              barPercentage: 1.6,
              gridLines: {
                drawBorder: false,
                color: 'rgba(255,255,255,0.1)',
                zeroLineColor: 'transparent',
                display: false,
              },
              ticks: {
                padding: 20,
                fontColor: '#9f9f9f'
              }
            }]
          },
        }
      });

    });
  }

  ngOnInit() {
    const response = this.http.get<string[]>(`${environment.apiUrl}/tags`);
    response.toPromise().then(value => {
      this.categories = []
      value.forEach(value1 => {
        // tslint:disable-next-line:prefer-const
        let abc: any = {
          name : value1,
          disabled : false,
        };
        this.categories.push(abc)
      })
      console.log(this.categories)
    })
  }
}
