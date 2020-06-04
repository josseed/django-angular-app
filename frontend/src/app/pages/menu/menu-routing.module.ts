import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MenuComponent } from './menu.component';
import { CreateMenuComponent } from './create-menu/create-menu.component';
import { MenuDetailComponent } from './menu-detail/menu-detail.component';

const routes: Routes = [
  { path: '', component: MenuComponent },
  { path: 'create-menu', component: CreateMenuComponent },
  { path: ':id/detail', component: MenuDetailComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MenuRoutingModule { }
