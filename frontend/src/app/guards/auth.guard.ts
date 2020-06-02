import { Injectable, Inject } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(@Inject(AuthService) private authService: AuthService, 
              @Inject(Router) private router: Router ) {}

  canActivate(@Inject(ActivatedRouteSnapshot) route: ActivatedRouteSnapshot,@Inject(RouterStateSnapshot) state: RouterStateSnapshot) {
  
    if (this.authService.isLogged()) {
      return true;
    } else {
      this.router.navigate(['/login']);
      return false;
    }
}
  
}
