import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MenuService } from 'src/app/services/menu/menu.service';
import { Menu } from 'src/app/models/menu';

@Component({
  selector: 'app-daily-menu',
  templateUrl: './daily-menu.component.html',
  styleUrls: ['./daily-menu.component.scss']
})
export class DailyMenuComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private menuService: MenuService,
    private router: Router
  ) { }
  private uuid: string;
  public isLoading: boolean;
  public errorInGetMenu: boolean;
  public menu: Menu;

  public ngOnInit(): void {
    this.isLoading = true;
    this.errorInGetMenu = false;
    this.route.queryParams.subscribe(params => {
      this.uuid = params['uuid']; 
      console.log(this.uuid)
      this.getDailyMenu();
    });
  }

  private getDailyMenu(): void {
    this.menuService.getCurrentMenuByUUID(this.uuid).subscribe(data => {
      this.menu = new Menu(data);
      this.isLoading = false;
    }, error => {
      this.isLoading = false;
      this.errorInGetMenu = true;
    });
  }

  public login():void {
    this.router.navigate(['/home']);
  }

}
