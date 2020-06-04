import { Component, OnInit } from '@angular/core';
import { AuthService } from 'src/app/services/auth/auth.service';
import { Router } from '@angular/router';
import { NzNotificationService } from 'ng-zorro-antd/notification';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(
    private authService: AuthService,
    private router: Router,
    private notification: NzNotificationService
  ) { }

  ngOnInit(): void {
  }

  public submitForm(event: any, email: string, password: string): void {  
    this.authService.loginUser(email, password).subscribe(data => {
      this.authService.setUserFromJWT(data.token);
      this.authService.setToken(data.token);
      if (data) {
        this.router.navigate(['/menus']);
      }
    }, error => {
      this.errorLogin('error');
    });
  }

  private errorLogin(type: string): void {
    this.notification.create(
      type,
      'Error:',
      'Usuario o contraseña incorrecta'
    );
  }

}
