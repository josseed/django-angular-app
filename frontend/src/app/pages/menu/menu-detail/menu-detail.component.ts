import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { MenuService } from 'src/app/services/menu/menu.service';
import { Menu } from 'src/app/models/menu';
import { Meal } from 'src/app/models/meal';
import { MealService } from 'src/app/services/meal/meal.service';

@Component({
  selector: 'app-menu-detail',
  templateUrl: './menu-detail.component.html',
  styleUrls: ['./menu-detail.component.scss']
})
export class MenuDetailComponent implements OnInit {
  private routeSub: Subscription;
  private menuId: number;
  public newMeal: Meal;
  public menu: Menu;
  public isLoading: boolean = true;
  public isVisible: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private menuService: MenuService,
    private mealService: MealService
  ) { }

  public ngOnInit(): void {
    this.routeSub = this.route.params.subscribe(params => {
      this.menuId = params['id'];
      this.getMenu();
    });
  }

  private getMenu(): void {
    this.menuService.getMenu(this.menuId).subscribe(data => {
      this.menu = new Menu(data);
      console.log(this.menu);
      this.isLoading = false;
    });
  }

  public ngOnDestroy(): void {
    this.routeSub.unsubscribe();
  }

  public createMeal(): void {
    this.mealService.createMeal(this.menuId, this.newMeal).subscribe(data => {
      let meal = new Meal(data);
      this.menu.meals = [...this.menu.meals, meal];
      this.isVisible = false;
    });
    
  }

  public showModal(): void {
    this.newMeal = new Meal();
    this.isVisible = true;
  }

  public handleCancel(): void {
    console.log('Button cancel clicked!');
    this.isVisible = false;
  }

}
