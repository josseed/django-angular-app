import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subscription } from 'rxjs';
import { MenuService } from 'src/app/services/menu/menu.service';
import { Menu } from 'src/app/models/menu';
import { Meal } from 'src/app/models/meal';
import { MealService } from 'src/app/services/meal/meal.service';
import { NzNotificationService } from 'ng-zorro-antd';

@Component({
  selector: 'app-menu-detail',
  templateUrl: './menu-detail.component.html',
  styleUrls: ['./menu-detail.component.scss']
})
export class MenuDetailComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private menuService: MenuService,
    private mealService: MealService,
    private notification: NzNotificationService
  ) { }
  
  private routeSub: Subscription;
  private menuId: number;
  public newMeal: Meal;
  public menu: Menu;
  public isLoading: boolean = true;
  public isVisible: boolean = false;
  public editId: number | null = null;

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
    this.isVisible = false;
  }

  public deleteRow(id: number): void {
    this.mealService.deleteMeal(this.menu.id, id).subscribe(data => {
      this.mealDeleted('success');
      this.menu.meals = this.menu.meals.filter(meal => meal.id !== id);
    });
  }

  public startEdit(id: number): void {
    this.editId = id;
  }

  public stopEdit(): void {
    let mealEdited = this.menu.meals.find(meal => meal.id === this.editId);
    this.mealService.editMeal(this.menu.id, this.editId, mealEdited).subscribe(data => {
      this.mealEditaded('success');
    })
    this.editId = null;
  }

  private mealEditaded(type: string): void {
    this.notification.create(
      type,
      'Success:',
      'Almuerzo editado correctamente.'
    );
  }

  private mealDeleted(type: string): void {
    this.notification.create(
      type,
      'Success:',
      'Almuerzo eliminado correctamente.'
    );
  }

}
