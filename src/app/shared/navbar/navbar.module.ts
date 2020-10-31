import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {RouterModule} from '@angular/router';
import {NavbarComponent} from './navbar.component';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import {NgSelectModule} from '@ng-select/ng-select';
import {FormsModule} from '@angular/forms';

@NgModule({
  imports: [RouterModule, CommonModule, NgbModule, NgSelectModule, FormsModule],
    declarations: [ NavbarComponent ],
    exports: [ NavbarComponent ],
})

export class NavbarModule {}
