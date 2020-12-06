import {Routes} from '@angular/router';

import {AdminLayoutComponent} from './layouts/admin-layout/admin-layout.component';

import {AuthGuard} from './_helpers';

const accountModule = () => import('./account/account.module').then(x => x.AccountModule);
const adminModule = () => import('./layouts/admin-layout/admin-layout.module').then(x => x.AdminLayoutModule);
const usersModule = () => import('./users/users.module').then(x => x.UsersModule);

export const AppRoutes: Routes = [
  {
    path: '',
    redirectTo: 'dashboard',
    pathMatch: 'full',
  },
  {
    path: '',
    component: AdminLayoutComponent,
    children: [
      {
        path: '',
        loadChildren: './layouts/admin-layout/admin-layout.module#AdminLayoutModule'
      }]
  },
  {
    path: 'account',
    loadChildren: accountModule
  },
  {
    path: '**',
    redirectTo: 'dashboard'
  }
]
