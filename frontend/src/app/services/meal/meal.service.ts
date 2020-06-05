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

  public getMeals(menuId: number): Observable<any> {
    const url_api = `${this.api}/menus/${menuId}/meals`;
    return this.http.get(url_api, { headers: this.headers });
  }

  public createMeal(menuId: number, meal: Meal): Observable<any> {
    const url_api = `${this.api}/menus/${menuId}/meals`;
    return this.http.post(url_api, meal, { headers: this.headers });
  }

  public editMeal(menuId: number, mealId: number, meal: Meal): Observable<any> {
    const url_api = `${this.api}/menus/${menuId}/meals/${mealId}`;
    return this.http.patch(url_api, meal, { headers: this.headers });
  }

  public deleteMeal(menuId: number, mealId: number): Observable<any> {
    const url_api = `${this.api}/menus/${menuId}/meals/${mealId}`;
    return this.http.delete(url_api, { headers: this.headers });
  }

}





