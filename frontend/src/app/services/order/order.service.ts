import { Injectable} from "@angular/core";
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable } from "rxjs";
import { Environment } from 'src/environments/environment';
import { Meal } from 'src/app/models/meal';

@Injectable({
  providedIn: "root"
})
export class MealService {

  private api: string;

  constructor( private http: HttpClient, private router: Router) {
    this.api = Environment.api;
  }

  headers: HttpHeaders = new HttpHeaders({
    "Content-Type": "application/json",
    "Authorization": "JWT " + localStorage.getItem("accessToken")
  });

  public getCurrentOrders(): Observable<any> {
    const url_api = `${this.api}/menus//meals`;
    return this.http.get(url_api, { headers: this.headers });
  }

}





