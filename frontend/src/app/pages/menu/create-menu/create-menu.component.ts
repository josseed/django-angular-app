import { Component, OnInit } from '@angular/core';
import { Menu } from 'src/app/models/menu';
import { MenuService } from 'src/app/services/menu/menu.service';
import {Location, DatePipe} from '@angular/common';

@Component({
  selector: 'app-create-menu',
  templateUrl: './create-menu.component.html',
  styleUrls: ['./create-menu.component.scss']
})
export class CreateMenuComponent implements OnInit {
  
  constructor(
    private menuService: MenuService,
    private _location: Location,
    private datePipe: DatePipe
  ) { }
  
  public dateFormat = 'yyyy-MM-dd';
  public menu: Menu;


  public ngOnInit(): void {
    this.menu = new Menu();
  }

  public createMenu(): void {

    let tempDate = this.menu.date;
    this.menu.date = this.datePipe.transform(tempDate, 'yyyy-MM-dd');
    this.menuService.createMenu(this.menu).subscribe(data => {
      this._location.back();
    })
  }

}
