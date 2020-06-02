import { Injectable, Inject } from "@angular/core";
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from "rxjs";
import { User } from "src/app/models/user";
import decode from 'jwt-decode';
import { Environment } from 'src/environments/environment';

@Injectable({
  providedIn: "root"
})
export class AuthService {

  public user_role: number;
  public user: User = new User();
  private api: string;

  constructor(@Inject(HttpClient) private http: HttpClient, @Inject(Router) private router: Router) {
    this.api = Environment.api;
  }

  headers: HttpHeaders = new HttpHeaders({
    "Content-Type": "application/json"
  });

  public loginUser(email: string, password: string): Observable<any> {
    const url_api = `${this.api}auth/login`;
    return this.http
      .post(url_api,{ email, password }, { headers: this.headers });
  }

  public setUserFromJWT(token: string): void {
    let token_data = decode(token);
    this.user.id = token_data.user_id;
    this.user.first_name = token_data.first_name;
    this.user.email = token_data.email;
  }

  public setToken(token: string): void {
    localStorage.setItem("accessToken", token);
  }

  public getToken(): string {
    return localStorage.getItem("accessToken");
  }

  public isLogged(): boolean {
    if (this.user.id) {
      return true
    } else {
      return false
    }  
  } 

  public getMyUser(): User {
    return this.user;
  }

  public logoutUser(): void {
    localStorage.removeItem("accessToken");
    this.router.navigate(['login']);
  }

  public getMyId(): number {
    return this.user.id;
  }

}





