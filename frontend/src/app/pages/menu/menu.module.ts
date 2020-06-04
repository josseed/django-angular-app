import { NgModule } from '@angular/core';

import { MenuRoutingModule } from './menu-routing.module';

import { MenuComponent } from './menu.component';
import { NzLayoutModule, NzMenuModule, NgZorroAntdModule } from 'ng-zorro-antd';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { CreateMenuComponent } from './create-menu/create-menu.component';
import { MenuDetailComponent } from './menu-detail/menu-detail.component';


@NgModule({
  imports: [
    MenuRoutingModule,
    NzLayoutModule,
    NzMenuModule,
    FormsModule,
    HttpClientModule,
    NgZorroAntdModule,
    CommonModule
  ],
  declarations: [MenuComponent, CreateMenuComponent, MenuDetailComponent],
  exports: [MenuComponent]
})
export class MenuModule { }
