import {Component, OnInit} from '@angular/core';


export interface RouteInfo {
  id: string
  path: string;
  title: string;
  icon: string;
  class: string;
  child: RouteInfo[]
}

export const ROUTES: RouteInfo[] = [
  {id: '', path: '/dashboard', title: 'Home', icon: 'nc-bank', class: '', child: null},
  {id: 'current', path: '/nopath', title: 'Current Trend', icon: 'nc-chart-bar-32', class: '', child: [
      {id: '', path: '/trend', title: 'Overview', icon: 'nc-chart-bar-32', class: 'pl-5', child: null},
      {id: '', path: '/comparison', title: 'Compare Technologies', icon: 'nc-chart-pie-36', class: 'pl-5', child: null},
    ]
  },
  {id: '', path: '/prediction-trend', title: 'Demand Forecast', icon: 'nc-atom', class: '', child: null},
];

@Component({
  moduleId: module.id,
  selector: 'app-sidebar-cmp',
  templateUrl: 'sidebar.component.html',
})

export class SidebarComponent implements OnInit {
  public menuItems: any[];

  ngOnInit() {
    this.menuItems = ROUTES.filter(menuItem => menuItem);
  }
}
