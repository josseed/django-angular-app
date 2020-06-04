import { Component, OnInit } from '@angular/core';
import { Menu } from 'src/app/models/menu';
import { MenuService } from 'src/app/services/menu/menu.service';
import { Router } from '@angular/router';
import { NzNotificationService } from 'ng-zorro-antd';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnInit {

  constructor(
    private menuService: MenuService,
    private router: Router,
    private notification: NzNotificationService,
    private datePipe: DatePipe
  ) { }
  
  public menus: Menu[];
  public isLoading: boolean = true;
  private today = this.datePipe.transform(Date.now(), 'yyyy-MM-dd');

  ngOnInit() {
    this.getMenus();
  }

  private getMenus(): void {
    this.menuService.getMenus().subscribe(data => {
      this.menus = data.map(menu => new Menu(menu));
      this.isLoading = false;
    })
  }

  public goToMenu(id: number): void {
    this.router.navigate([`menus/${id}/detail`]);
  }

  public sendMenu(id: number): void {
    let menu = this.menus.find(menu => menu.id === id);
    if (menu.date !== this.today) {
      this.errorDateMenu('error');
      return;
    }

    this.menuService.sendMenu(id).subscribe(data => {
      this.MenuSended('success');
    });
  }

  private MenuSended(type: string): void {
    this.notification.create(
      type,
      'Success:',
      'A comenzado el envio del menu a slack.'
    );
  }

  private errorDateMenu(type: string): void {
    this.notification.create(
      type,
      'Error:',
      'Solo se puede enviar el menu correspondiende al día de hoy.'
    );
  }
}
