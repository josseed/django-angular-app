import { Injectable} from "@angular/core";
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from "rxjs";
import { Environment } from 'src/environments/environment';
import { Menu } from 'src/app/models/menu';

@Injectable({
  providedIn: "root"
})
export class MenuService {

  private api: string;

  constructor( private http: HttpClient, private router: Router) {
    this.api = Environment.api;
  }

  headers: HttpHeaders = new HttpHeaders({
    "Content-Type": "application/json",
    "Authorization": "JWT " + localStorage.getItem("accessToken")
  });

  public getMenus(): Observable<any> {
    const url_api = `${this.api}/menus`;
    return this.http.get(url_api, { headers: this.headers });
  }

  public createMenu(menu: Menu): Observable<any> {
    const url_api = `${this.api}/menus`;
    return this.http.post(url_api, menu, { headers: this.headers });
  }

  public getMenu(id: number): Observable<any> {
    const url_api = `${this.api}/menus/${id}`;
    return this.http.get(url_api, { headers: this.headers });
  }

  public sendMenu(id: number ): Observable<any> {
    const url_api = `${this.api}/menus/${id}/send-menu`;
    return this.http.post(url_api, {}, { headers: this.headers });
  }
}





