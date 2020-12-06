import {Routes} from '@angular/router';

import {DashboardComponent} from '../../pages/dashboard/dashboard.component';
import {TrendComponent} from '../../pages/trend/trend.component';
import {PredictionTrendComponent} from '../../pages/predictiontrend/predictiontrend.component';
import {ComparisonComponent} from '../../pages/comparison/comparison.component';
import {AuthGuard} from '../../_helpers';

export const AdminLayoutRoutes: Routes = [
    { path: 'dashboard',      component: DashboardComponent },
    { path: 'trend',      component: TrendComponent },
    { path: 'prediction-trend',      component: PredictionTrendComponent,     canActivate: [AuthGuard] },
    { path: 'comparison',      component: ComparisonComponent },
    // { path: 'user',           component: UserComponent },
    // { path: 'table',          component: TableComponent },
    //
    // { path: 'upgrade',        component: UpgradeComponent }
];
