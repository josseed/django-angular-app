import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';
import { LoginComponent } from './pages/login/login.component';
import { IndexComponent } from './pages/index/index.component';

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
      }
    ]
  },
  {
    path: 'login',
    component: LoginComponent,  
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
