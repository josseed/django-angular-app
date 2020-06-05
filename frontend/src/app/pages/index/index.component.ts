import { Component } from '@angular/core';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'index-root',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.scss']
})
export class IndexComponent {
  isCollapsed = false;

  constructor(private authService: AuthService) {}

  public logOut(): void {
    this.authService.logoutUser();
  }
}
