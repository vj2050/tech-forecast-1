import { Component, OnInit } from '@angular/core';
import Chart from 'chart.js';


@Component({
    selector: 'app-dashboard-cmp',
    moduleId: module.id,
    templateUrl: 'dashboard.component.html'
    
})

export class DashboardComponent implements OnInit {

  public canvas: any;
  public ctx;
  public chartColor;
  public chartEmail;
  public chartHours;

    ngOnInit() {
    }
}
