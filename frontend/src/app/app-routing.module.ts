import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { IndexComponent } from './pages/index/index.component';
import { DailyMenuComponent } from './pages/daily-menu/daily-menu.component';
import { OrdersComponent } from './pages/orders/orders.component';

const routes: Routes = [

  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'menus'
  },
  { 
    path: '',
    component: IndexComponent,
    canActivate: [AuthGuard],
    children: [
      { 
        path: 'menus',
        loadChildren: () => import('./pages/menu/menu.module').then(m => m.MenuModule)
      },
      {
        path:'orders',
        component: OrdersComponent
      }
    ]
  },
  {
    path: 'login',
    component: LoginComponent,  
  },
  {
    path: 'daily-menu',
    component: DailyMenuComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
