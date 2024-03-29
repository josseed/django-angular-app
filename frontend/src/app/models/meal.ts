import { Order } from './order';

export class Meal {

  public id: number;
  public name: string;
  public orders: Order[];

  constructor(data: any = null) {
    if (data) {
      this.id = data.id;
      this.name = data.name;
      if (data.orders) {
        this.orders = data.orders.map(order => new Order(order));
      }
    }
  }

  public toJSON(): any {
    return {
      id: this.id,
      name: this.name
    }
  }
}