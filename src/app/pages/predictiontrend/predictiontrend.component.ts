import { Component, OnInit } from '@angular/core';
import Chart from 'chart.js';


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
  categories = [
    {id: 1, name: 'Laravel'},
    {id: 2, name: 'Codeigniter'},
    {id: 3, name: 'React'},
    {id: 4, name: 'PHP'},
    {id: 5, name: 'Flask'},
    {id: 6, name: 'Django'},
    {id: 7, name: 'JQuery', disabled: true},
    {id: 8, name: 'Javascript'},
  ];

  selected = [
    {id: 5, name: 'Flask'},
    {id: 6, name: 'Django'}
  ];

  getSelectedValue(){
    console.log(this.selected);
  }
    ngOnInit() {
      this.chartColor = '#FFFFFF';

      let speedCanvas = document.getElementById('speedChart');

      let dataFirst = {
        data: [0, 19, 15, 20, 30, 40, 40, 50, 25, 30, 50, 70],
        fill: false,
        borderColor: '#fbc658',
        backgroundColor: 'transparent',
        pointBorderColor: '#fbc658',
        pointRadius: 4,
        pointHoverRadius: 4,
        pointBorderWidth: 8,
      };

      let dataSecond = {
        data: [0, 5, 10, 12, 20, 27, 30, 34, 42, 45, 55, 63],
        fill: false,
        borderColor: '#51CACF',
        backgroundColor: 'transparent',
        pointBorderColor: '#51CACF',
        pointRadius: 4,
        pointHoverRadius: 4,
        pointBorderWidth: 8
      };

      let speedData = {
        labels: ['2010', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022'],
        datasets: [dataFirst, dataSecond]
      };

      let chartOptions = {
        legend: {
          display: false,
          position: 'top'
        }
      };

      let lineChart = new Chart(speedCanvas, {
        type: 'line',
        hover: false,
        data: speedData,
        options: chartOptions
      });
    }
}
