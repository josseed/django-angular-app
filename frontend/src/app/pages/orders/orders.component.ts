import { Component, OnInit } from '@angular/core';
import { MenuService } from 'src/app/services/menu/menu.service';
import { Menu } from 'src/app/models/menu';
import { Order } from 'src/app/models/order';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss']
})
export class OrdersComponent implements OnInit {

  constructor(
    private menuService: MenuService
  ) { }
  public isLoading: boolean = true;
  public errorInGetMenu: boolean = false;
  public isVisible: boolean = false;
  public menu: Menu;
  public orders: Order[];

  public ngOnInit(): void {
    this.getCurrentMenu();
  }

  private getCurrentMenu(): void {
    this.menuService.getCurrentMenu().subscribe(data => {
      this.menu = new Menu(data);
      console.log(data);
      this.isLoading = false;
    }, error => {
      this.isLoading = false;
      this.errorInGetMenu = true;
    })
  }

  public showOrders(id: number): void {
    console.log("show orders");
    this.orders = this.menu.meals.find(
      meal => meal.id == id
    ).orders;
    this.isVisible = true;
  }

  public handleOk(): void {
    this.isVisible = false;
  }

}
