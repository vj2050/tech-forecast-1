import { Component, OnInit } from '@angular/core';


export interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}

export const ROUTES: RouteInfo[] = [
    { path: '/dashboard',     title: 'Dashboard',         icon: 'nc-bank',       class: '' },
    { path: '/trend',     title: 'Current Trend',         icon: 'nc-chart-bar-32',       class: '' },
    { path: '/prediction-trend',     title: 'Demand Forecast',         icon: 'nc-atom',       class: '' },
    { path: '/comparison',     title: 'Comparison',         icon: 'nc-chart-pie-36',       class: '' },
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
