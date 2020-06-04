import { Meal } from './meal';

export class Menu {

  public id: number;
  public name: string;
  public date: string;
  public meals: Meal[];

  constructor(data: any = null) {
    if (data) {
      this.id = data.id;
      this.name = data.name;
      this.date = data.date;
      if (data.meals) {
        this.meals = data.meals.map(meal => new Meal(meal));
      } else {
        this.meals = [new Meal()];
      }
    }
  }

  public toJSON(): any {
    return {
      id: this.id,
      name: this.name,
      date: this.date
    }
  }
}