import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AdminLayoutRoutes } from './admin-layout.routing';
import { DashboardComponent }       from '../../pages/dashboard/dashboard.component';
import { UserComponent }            from '../../pages/user/user.component';
import { TableComponent }           from '../../pages/table/table.component';
import { UpgradeComponent }         from '../../pages/upgrade/upgrade.component';

import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import {TrendComponent} from '../../pages/trend/trend.component';
import {PredictionTrendComponent} from '../../pages/predictiontrend/predictiontrend.component';
import {ComparisonComponent} from '../../pages/comparison/comparison.component';

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(AdminLayoutRoutes),
    FormsModule,
    NgbModule
  ],
  declarations: [
    DashboardComponent,
    TrendComponent,
    PredictionTrendComponent,
    ComparisonComponent,
    UserComponent,
    TableComponent,
    UpgradeComponent
  ]
})

export class AdminLayoutModule {}
